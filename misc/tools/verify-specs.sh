#!/bin/bash

# Copyright 2017 The authors
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

# This script will scan all md (markdown) files for bad keyword usages.
#
# Usage: verify-phrases.sh [ dir | file ... ]
# default arg is root of our source tree

set -o errexit
set -o nounset
set -o pipefail

casePhrases=(   # case matters
MUST
"MUST NOT"
REQUIRED
SHALL
"SHALL NOT"
SHOULD
"SHOULD NOT"
RECOMMENDED
MAY
OPTIONAL
)
casePhrases=${casePhrases:=""}  # just to avoid a bash error if undefined

bannedPhrases=(  # case does not matter
"Cloud Event"
"Cloud Events"
)
bannedPhrases=${bannedPhrases:=""}  # just to avoid a bash error if undefined

REPO_ROOT=$( cd $(dirname "${BASH_SOURCE}")/.. && pwd)

verbose=""
debug=""
stop=""

# Error file processing
err=tmpCC-$RANDOM
trap clean EXIT
function clean {
  rm -f ${err}*
}

while [[ "$#" != "0" && "$1" == "-"* ]]; do
  opts="${1:1}"
  while [[ "$opts" != "" ]]; do
    case "${opts:0:1}" in
      v) verbose="1" ;;
      d) debug="1" ; verbose="1" ;;
      -) stop="1" ;;
      ?) echo "Usage: $0 [OPTION]... [DIR|FILE]..."
         echo "Verify all terms defined in spec are cased correctly."
         echo
         echo "  -v   show each file as it is checked"
         echo "  -?   show this help text"
         echo "  --   treat remainder of args as dir/files"
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
# echo debug:$debug
# echo args:$*

arg=""

if [ "$*" == "" ]; then
  arg="${REPO_ROOT}"
fi

Files=$(find -L $* $arg \( -name "*.md" -o -name "*.htm*" \) | sort)

function checkFile {
  # Determine the max # of words we need to look for
  maxWords=1
  for phrase in "${casePhrases[@]}"; do
    words=( ${phrase[@]} )
    if (( ${#words[@]} > $maxWords )); then
      maxWords=${#words[@]}
    fi
  done

  for phrase in "${bannedPhrases[@]}"; do
    words=( ${phrase[@]} )
    if (( ${#words[@]} > $maxWords )); then
      maxWords=${#words[@]}
    fi
  done

  lines=( "" )
  words=( "" )

  if grep -i "<!-- *no verify-specs" $1 > /dev/null 2>&1 ; then
    return
  fi

  # Prepend each line of the file with its line number
  cat -n $1 | while read num line ; do
    # Put each word on its own line with its line number before it.
    echo "$line" | \
    # Split on whitespace
    # Macs require this funky newline stuff
    sed 's/[[:space:]]/\
&\
/g' | \
    # Put a \n before any http... word so they're easy to find
    sed 's/http.*[^[[:space:]]]*/\
&\
/g' | \
    ( while read line ; do
        # Lines that start with http are special, just echo them
        if [[ "$line" == "http"* ]]; then
          echo $line
          continue
        fi
        # Now split on words
        echo "$line" | sed 's/[a-zA-Z_\-]+/\
&\
/g'
      done
    ) | \
    while read word ; do
      # Now put the line number before each word
      echo $num $word
    done
  done | while read line word ; do
    if [[ "$word" == "" ]]; then
      continue
    fi

    # echo $line $word

    # Shift our arrays of lineNums and words
    if (( ${#words[@]} >= $maxWords )); then
      lines=( "${lines[@]:1}" "$line" )
      words=( "${words[@]:1}" "$word" )
    else
      lines=( "${lines[@]}" "$line" )
      words=( "${words[@]}" "$word" )
    fi

    # echo Lines: "${lines[@]}"
    # echo Words: "${words[@]}"

    # For each of our "casePhrases" check to see if its in "words" with
    # the wrong case
    upperWords="${words[@]^^}"
    for phrase in "${casePhrases[@]}"; do
      # echo upperWords:${upperWords}
      # echo upperPhrase:${upperPhrase}
      if [[ "${upperWords} " == "${phrase^^} "* && \
            "${words[@]} " != "${phrase} "* ]]; then
        ll=${words[*]}
        echo line ${lines[0]}: \'${ll:0:${#phrase}}\' should be \'${phrase}\'
      fi
    done

    # For each of our "bannedPhrases" check to see if its in "words". Note
    # that the case of the phrase does not matter.
    [ -z "${bannedPhrases}" ] || for phrase in "${bannedPhrases[@]}"; do
      if [[ "${upperWords} " == "${phrase^^} "* ]]; then
        ll=${words[*]}
        echo line ${lines[0]}: \'${ll:0:${#phrase}}\' is banned
      fi
    done


  done
}

for file in ${Files}; do
  # echo scanning $file
  dir=$(dirname $file)

  [[ -n "$verbose" ]] && echo "> $file"

  checkFile $file | tee -a $err
done

if [ -s ${err} ]; then exit 1 ; fi
