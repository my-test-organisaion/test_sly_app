#!/bin/bash

if (( ${#SUBAPP_PATHS[@]} == 0 )); then
    supervisely release --release-version "${{ github.event.release.tag_name }}" --release-description "${{ github.event.release.name }}" --slug "${{ github.repository }}" -y
else
    for i in "${SUBAPP_PATHS[@]}"
    do
        if $i == "__ROOT_APP__"
        then
            supervisely release --release-version "${{ github.event.release.tag_name }}" --release-description "${{ github.event.release.name }}" --slug "${{ github.repository }}" -y
        else
            supervisely release --release-version "${{ github.event.release.tag_name }}" --release-description "${{ github.event.release.name }}" --slug "${{ github.repository }}" -y -a $i
        fi
    done
fi