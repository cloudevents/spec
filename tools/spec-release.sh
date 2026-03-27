#!/usr/bin/env bash

# Copyright 2022 The CDEvents Authors.
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
#

function usage() {
    cat <<EOF
spec-release.sh is tool to manage spec releases

Usage:
  spec-release.sh -s
  spec-release.sh -m
  spec-release.sh -e
  spec-release.sh -p
  spec-release.sh -v Major.minor.patch

-s  Start a new release on the main branch by incrementing the minor version by one.

-m  Start a new release on the main branch by incrementing the major version by one.

-e  End the current draft release.

-p  Patch the release on a spec-vM.m branch by increasing the latest patch available by one.

-v  Set the version to Major.minor.patch

Examples:
  spec-release.sh -s -> updates all release references on main fom from M.m.0 to M.m+1.0-draft
  spec-release.sh -m -> updates all release references on main from from M.m.0 to M+1.0.0-draft
  spec-release.sh -e -> updates all release references on main from M.m.0-draft to M.m.0
  spec-release.sh -p -> updates all release references on spec-vM.m from M.m.p to M.m.p+1
  spec-release.sh -v 1.2.3 -> updates all release references to 1.2.3
EOF
}

set -o errexit
set -o nounset
set -o pipefail

declare COMMAND INCREMENT VERSION NEW_VERSION
declare VERSION_FILE=version.txt

START_COMMAND=start
END_COMMAND=end
PATCH_COMMAND=patch
VERSION_COMMAND=version

# cd to the root path
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
cd "${ROOT}" 

while getopts ":smepv:" o; do
    case "${o}" in
        s)
            COMMAND="${START_COMMAND}"
            INCREMENT="minor"
            ;;
        m)
            COMMAND="${START_COMMAND}"
            INCREMENT="major"
            ;;
        e)
            COMMAND="${END_COMMAND}"
            ;;
        p)
            COMMAND="${PATCH_COMMAND}"
            ;;
        v)  COMMAND="${VERSION_COMMAND}"
            NEW_VERSION=${OPTARG}
            ;;
        *)
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${COMMAND}" ]; then
    usage
fi

if [ ! -f "$VERSION_FILE" ]; then
    echo "Version file $VERSION_FILE not found"
    exit 1
fi

OLD_VERSION=$(cat ${VERSION_FILE})
VERSION="${NEW_VERSION:-$OLD_VERSION}"
SPLIT_VERSION=(${VERSION//./ })
MAJOR_VERSION=${SPLIT_VERSION[0]}
MINOR_VERSION=${SPLIT_VERSION[1]}
PATCH_VERSION_DRAFT=${SPLIT_VERSION[2]}
SPLIT_PATCH=(${PATCH_VERSION_DRAFT//-/ })
PATCH_VERSION=${SPLIT_PATCH[0]}
DRAFT_VERSION=""
if [[ ${#SPLIT_PATCH[@]} > 1 ]]; then
    DRAFT_VERSION="-${SPLIT_PATCH[1]}"
fi

if [[ "${COMMAND}" == "${END_COMMAND}" ]]; then
    if [[ -z ${DRAFT_VERSION} ]]; then
        echo "Cannot end release ${VERSION}, must be in draft to end"
        exit 1
    fi
    DRAFT_VERSION=""
fi

if [[ "${COMMAND}" == "${START_COMMAND}" ]]; then
    if [[ -n ${DRAFT_VERSION} ]]; then
        echo "Cannot start release ${VERSION}, already in ${DRAFT_VERSION}"
        exit 1
    fi
    PATCH_VERSION=0
    DRAFT_VERSION="-draft"
    if [[ "${INCREMENT}" == "minor" ]]; then
        MINOR_VERSION=$(( MINOR_VERSION + 1 ))
    else
        MAJOR_VERSION=$(( MAJOR_VERSION + 1 ))
        MINOR_VERSION=0
    fi
fi

if [[ "${COMMAND}" == "${PATCH_COMMAND}" ]]; then
    if [[ -n ${DRAFT_VERSION} ]]; then
        echo "Cannot start release ${VERSION}, already in ${DRAFT_VERSION}"
        exit 1
    fi
    PATCH_VERSION=$(( PATCH_VERSION + 1 ))
fi

VERSION="${MAJOR_VERSION}.${MINOR_VERSION}.${PATCH_VERSION}${DRAFT_VERSION}"

# Replace the version in the schema IDs
find schemas -name '*json' | \
    xargs sed -i ".backup" -e 's,https://cdevents.dev/'${OLD_VERSION}'/schema/,https://cdevents.dev/'${VERSION}'/schema/,g'

# Replace the version in the conformance files
find conformance -name '*json' | \
    xargs sed -i ".backup" -e 's,"specversion": "'${OLD_VERSION}'","specversion": "'${VERSION}'",g'

# Replace the version in the custom events schema ID
find custom -name '*json' | \
    xargs sed -i ".backup" -e 's,https://cdevents.dev/'${OLD_VERSION}'/schema/,https://cdevents.dev/'${VERSION}'/schema/,g'

# Replace the version in the custom events conformance file
find custom -name '*json' | \
    xargs sed -i ".backup" -e 's,"specversion": "'${OLD_VERSION}'","specversion": "'${VERSION}'",g'

# Update examples in docs
for doc in cloudevents-binding spec links; do
    sed -i ".backup" -e 's;"specversion": "'${OLD_VERSION}'",;"specversion": "'${VERSION}'",;g' "${doc}.md"
done

# Do not set the release in the main README for in progress releases
if [[ "${COMMAND}" != "${START_COMMAND}" ]]; then
    sed -i ".backup" -e 's;v'${OLD_VERSION}';v'${VERSION}';g' "README.md"
fi

# Cleanup backup files
find . -name '*.backup' | xargs rm

# Set the new version in the version file
echo "${VERSION}" > "${VERSION_FILE}"
