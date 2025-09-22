#!/bin/sh

set -u
# Function to check if a Git tag exists
tag_exists() {
    local tag=$1
    git rev-parse --quiet --verify "refs/tags/$tag" >/dev/null
}

# Check if the tag exists
tag="${CZ_PRE_NEW_TAG_VERSION}"
if tag_exists "$tag"; then
    echo "Tag '$tag' exists. Deleting..."
    git tag -d "$tag"
    git push origin --delete "$tag"
    echo "Tag '$tag' deleted."
else
    echo "Tag '$tag' does not exist."
    exit 0
fi