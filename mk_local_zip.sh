#!/bin/bash
# Construct the archive
zip local.zip local/cache/*/*.ant local/cache/*/*.csv local/cache/*/*.xml local/cache/*/*.sedml
# Remove the manifest files
zip -d local.zip "local/cache/*/manifest.xml"
# Document what's in the archive
unzip -l local.zip
