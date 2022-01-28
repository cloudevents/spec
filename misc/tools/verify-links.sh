#!/bin/bash

# Copyright 2017 The Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script will scan all md (markdown) files for bad references.
# It will look for strings of the form [...](...) and make sure that
# the (...) points to either a valid file in the source tree or, in the
# case of it being an http url, it'll make sure we don't get a 404.
#
# Usage: verify-links.sh [ dir | file ... ]
# default arg is root of our source tree

set -o errexit
set -o nounset
set -o pipefail

REPO_ROOT=$(dirname "${BASH_SOURCE}")/..

verbose=""
debugFlag=""
maxRetries="1"
skipExternal=""
skips=""
stop=""
tmp=/tmp/out${RANDOM}

trap clean EXIT
seenFiles=( ":" )   # just to prevent "undefined" errors

# findPrevious will search for a file to see if we've seen it before.
# If we have then return the matching "anchorFile". If we haven't
# seen it then add it to "seenFiles" and create a new "anchorFile".
# $1 == search file
# Note we can't use a map because bash on a mac doesn't support it.
foundAnchor=""
function findPreviousFile() {
  for f in "${seenFiles[@]}" ; do
    orig=${f%%:*}
    if [[ "${orig}" == "$1" ]]; then
      foundAnchor=${f#*:}
      return 0
    fi
  done

  # Didn't it so create a new anchorFile and save it for next time
  foundAnchor="${tmp}-anchors-${RANDOM}-${RANDOM}"
  seenFiles+=("$1:${foundAnchor}")
  return 1
}

function debug {
  if [[ "$debugFlag" != "" ]]; then
    (>&2 echo $*)
  fi
}

function clean {
  rm -f ${tmp}*
}

while [[ "$#" != "0" && "$1" == "-"* ]]; do
  opts="${1:1}"
  while [[ "$opts" != "" ]]; do
    case "${opts:0:1}" in
      d) debugFlag="1" ; verbose="1" ;;
      s) word=${opts:1}
         if [[ "${word}" == "" && "$2" != "" && "$2" != "-"* ]]; then
           word=$2
           shift
         fi
         if [[ "${word}" == "" ]]; then
           echo "Missing arg for -s flag"
           exit 1
         fi
         skips="${skips} ${word}"
         opts="" ;;
      t) maxRetries="5" ;;
      v) verbose="1" ;;
      x) skipExternal="1" ;;
      -) stop="1" ;;
      ?) echo "Usage: $0 [OPTION]... [DIR|FILE]..."
         echo "Verify all links in markdown files."
         echo
         echo "  -d         show each href as it is found"
         echo "  -sWORD     skip files with 'WORD' in them"
         echo "  -t         retry GETs to http(s) URLs 5 times"
         echo "  -v         show each file as it is checked"
         echo "  -x         skip checking non-local hrefs"
         echo "  -?         show this help text"
         echo "  --         treat remainder of args as dir/files"
         exit 0 ;;
      *) echo "Unknown option '${opts:0:1}'"
         exit 1 ;;
    esac
    opts="${opts:1}"
  done
  shift
  if [[ "$stop" == "1" ]]; then
    break
  fi
done

# echo verbose:$verbose
# echo debugFlag:$debugFlag
# echo args:$*

arg=""

if [ "$*" == "" ]; then
  arg="${REPO_ROOT}"
fi

# Default to skipping some well-known golang dirs
SKIPS="${SKIPS:=vendor glide} ${skips}"

mdFiles=$(find $* $arg -name "*.md" | sort | (
  while read line ; do
    skip=false
    for pattern in ${SKIPS:=}; do
      if [[ "${line}" == *"${pattern}"* ]]; then
        skip=true
        break
      fi
    done
    [[ "${skip}" == "true" ]] && continue
    echo $line
  done
))

clean
for file in ${mdFiles}; do
  # echo scanning $file
  dir=$(dirname $file)

  [[ -n "$verbose" ]] && echo "> $file"

  # Replace ) with )\n so that each possible href is on its own line.
  # Then only grab lines that have [..](..) in them - put results in tmp file.
  # If the file doesn't have any lines with [..](..) then skip this file
  # Steps:
  #  tr   - convert all \n to a space since newlines shouldn't change anything
  #  sed  - add a \n after each ) since ) ends what we're looking for.
  #         This makes it so that each href is on a line by itself
  #  sed  - prefix each line with a space so the grep can do [^\\]
  #  grep - find all lines that match [...](...)
  # Macs require this funky newline stuff
  cat $file | \
    tr '\n' ' ' | \
    sed 's/)/)\
/g' | \
    sed "s/^/ /g" | \
    grep "[^\\]\[.*\](.*)" > ${tmp}1 || true

  # This sed will extract the href portion of the [..](..) - meaning
  # the stuff in the parens.
  sed "s/.*\[*\]\([^()]*\)/\1/" < ${tmp}1 > ${tmp}2 || true

  # Look for bookmark URLs
  cat $file | sed -n "s/^ *\[.*\]: .*/&/p" > ${tmp}bks || true

  # Look for bookmarks
  cat $file | \
    tr '\n' ' ' | \
    sed -e 's/\[[^][]*\]\[[^][]*\]/&\
/g' | \
    sed -n -e 's/^.*\[.*\[\(.*\)\]$/\1/p' > "${tmp}links" || true

  cat ${tmp}links | while read bk ; do
    grep -q "^ *\\[${bk}\\]: " ${tmp}bks ||
      echo "$file: Can't find bookmark '[$bk]'" | \
        tee -a ${tmp}3
  done

  # Skip file if there are no matches
  [ ! -s ${tmp}2 ] && continue

  cat ${tmp}2 | while read line ; do
    # Strip off the leading and trailing parens
    ref=${line#*(}
    ref=${ref%)*}

    # Strip off any "title" associated with the href
    ref=$(echo $ref | sed 's/ ".*//')

    # Strip off leading and trailing spaces
    ref=$(echo $ref | sed "s/^ *//" | sed "s/ *$//")

    # Show all hrefs - mainly for verifying in our tests
    debug "Checking: '$ref'"

    # An external href (ie. starts with http(s): )
    if [ "${ref:0:5}" == "http:" ] || [ "${ref:0:6}" == "https:" ]; then
      if [ "$skipExternal" == "1" ]; then
        continue
      fi

      try=0
      while true ; do
        if curl -f -s -k --connect-timeout 10 ${ref} > /dev/null 2>&1 ; then
          break
        fi
        sleep 3
        let try=try+1
        if [ ${try} -eq ${maxRetries} ]; then
          extra=""
          if [ ${try} -gt 1 ]; then
            extra="(tried ${try} times) "
          fi
          echo $file: Can\'t load url: ${ref} ${extra} | tee -a ${tmp}3
          break
        fi
        sleep 1
      done
      continue
    fi

    # Skip "mailto:" refs
    if [ "${ref:0:7}" == "mailto:" ]; then
      continue
    fi

    # Local file link (i.e. ref contains a #)
    if [[ "${ref/\#}" != "${ref}" ]]; then

      # If ref doesn't start with "#" then update filepath
      if [ "${ref:0:1}" != "#" ]; then
        # Split ref into filepath and the section link
        reffile=$(echo ${ref} | awk -F"#" '{print $1}')
        fullpath=${dir}/${reffile}
        ref=$(echo ${ref} | awk -F"#" '{$1=""; print $0}')
      else
        fullpath=${file}
        ref=${ref:1}
      fi

      if [[ ! -e "${fullpath}" ]]; then
        echo "$file: Can't find referenced file '${fullpath}'" | \
          tee -a ${tmp}3
        continue
      fi

      # Remove leading and trailing spaces
      ref=$(echo ${ref} | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')

      # If we've seen this file before then grab its processed tmp file
      if findPreviousFile "${fullpath}" ; then
        anchorFile="${foundAnchor}"
      else
        anchorFile="${foundAnchor}"

        # Search file for sections
        used="" # anchors used, seen+twiddled ones

        # Find all section headers in the file.
        # Remove leading & trailing spaces.
        # Lower case it.
        # Convert spaces to "-".
        # Drop all non alphanumeric chars.
        # Twiddle section anchor if we've seen it before.
        grep "^[[:space:]]*#" < ${fullpath} | \
          sed 's/[[:space:]]*##*[[:space:]]*//' | \
          sed 's/[[:space:]]*$//' | \
          tr '[:upper:]' '[:lower:]' | \
          sed 's/\[\([^\[]*\)\](\([^()]*\))/\1/' | \
          sed "s/  */-/g" | \
          sed "s/[^-a-zA-Z0-9]//g" | while read section ; do
            # If we haven't used this exact anchor before just use it now
            if [[ "${used}" != *" ${section} "* ]]; then
              anchor=${section}
            else
              # We've used this anchor before so add "-#" to the end.
              # Keep adding 1 to "#" until we find a free spot.
              let num=1
              while true; do
                anchor="${section}-${num}"
                if [[ "${used}" != *" ${anchor} "* ]]; then
                  break
                fi
                let num+=1
              done
            fi

            echo "${anchor}"
            used="${used} ${anchor} "

            debug "Mapped section '${section}' to '${anchor}'"

          done > ${anchorFile} || true

        # Add sections of the form <a name="xxx">
        # Macs require this funky newline stuff
        grep "<a name=" <${fullpath} | \
          sed 's/<a name="/\
<a name="/g' | \
          sed 's/^.*<a name="\(.*\)">.*$/\1/' | \
          sort | uniq >> ${anchorFile} || true

        # echo sections ; cat ${tmp}sections1
      fi

      # Skip refs of the form #L<num> and assume its pointing to a line
      # number of a file and those don't have anchors
      if [[ "${ref}" =~ ^L([0-9])+$ ]]; then
        continue
      fi

      # Finally, look for the ref in the list of sections/anchors
      debug "Anchor file(${fullpath}): ${anchorFile}"
      if ! grep "^${ref}$" ${anchorFile} > /dev/null 2>&1 ; then
        echo $file: Can\'t find section \'\#${ref}\' in ${fullpath} | \
          tee -a ${tmp}3
      fi

      continue

    fi

    newPath=${dir}/${ref}

    # And finally make sure the file is there
    # debug line: echo ref: $ref "->" $newPath
    if [[ ! -e "${newPath}" ]]; then
      echo $file: Can\'t find: ${newPath} | tee -a ${tmp}3
    fi

  done
done
rc=0
if [ -a ${tmp}3 ]; then
  rc=1
fi
exit $rc
