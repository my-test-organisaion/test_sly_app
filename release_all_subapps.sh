#!/bin/bash

if (( ${#SUBAPP_PATHS[@]} == 0 )); then
    supervisely release --release-version "$RELEASE_VERSION" --release-description "$RELEASE_DESCRIPTION" --slug "$SLUG" -y
else
    for i in "${SUBAPP_PATHS[@]}"
    do
        if [[ "$i" == "__ROOT_APP__" ]]
        then
            supervisely release --release-version "$RELEASE_VERSION" --release-description "$RELEASE_DESCRIPTION" --slug "$SLUG" -y
        else
            supervisely release --release-version "$RELEASE_VERSION" --release-description "$RELEASE_DESCRIPTION" --slug "$SLUG" -y -a $i
        fi
    done
fi