#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# This scripts defines the batched processing pipeline for use on GCP.

set -eou pipefail
set -x

# Parameters that are read through the environment
: ${N_DATA?}
: ${BATCH_ID?}

: ${SERVER_ID}
: ${SHARED_SECRET?}
: ${PRIVATE_KEY_HEX?}
: ${PUBLIC_KEY_HEX_INTERNAL?}
: ${PUBLIC_KEY_HEX_EXTERNAL?}

: ${BUCKET_INTERNAL_PRIVATE}
: ${BUCKET_INTERNAL_SHARED?}
: ${BUCKET_EXTERNAL_SHARED?}


function create_folders() {
    mkdir -p raw
    mkdir -p intermediate/internal/verify1
    mkdir -p intermediate/internal/verify2
    mkdir -p intermediate/internal/aggregate
    mkdir -p processed
}


# Wait for a completed batch of data, signaled by the appearance of a _SUCCESS
# file.
#
# Arguments:
#   $1 - Absolute path to a file
function poll_for_data() {
    set +e
    max_retries=5
    retries=0
    backoff=2
    while ! gsutil -q stat $1 &>/dev/null; do
        sleep $backoff;
        ((backoff *= 2))
        ((retries++))
        if [[ "$retries" -gt "$max_retries" ]]; then
            echo "Reached the maximum number of retries."
            exit 1
        fi
    done
    set -e
}


# Poll for a success file and then copy the appropriate files locally
#
# Arguments:
#   $1 - Input bucket
#   $2 - Path relative to the input bucket
function fetch_input_blocked() {
    local bucket=$1
    local input=$2
    local path="gs://$bucket/$input"
    poll_for_data $path/_SUCCESS
    gsutil cp --recursive $path/ $input/
}


# Wait for data to be written to the internal private bucket before copying.
#
# Arguments:
#   $1 - The path relative to the internal private bucket
#
# Environment:
#   BUCKET_INTERNAL_PRIVATE
function fetch_input_private() {
    local input=$1
    fetch_input_blocked ${BUCKET_INTERNAL_PRIVATE} $input
}


# Wait for data to be written to the internal shared bucket before copying.
#
# Arguments:
#   $1 - The path relative to the internal shared bucket
#
# Environment:
#   BUCKET_INTERNAL_SHARED
function fetch_input_shared() {
    local input=$1
    fetch_input_blocked ${BUCKET_INTERNAL_SHARED} $input
}


# Copy data generated by a processing step into the receiving bucket of the
# co-processing server. A _SUCCESS file is generated on a successful copy.
#
# Arguments:
#   $1 - relative path to output for a processing stage
#   $2 - relative path to the external bucket of the external server
#
# Environment:
#   BUCKET_EXTERNAL_SHARED - The bucket of the external server
function send_output_external() {
    local output_internal=$1
    local output_external=$2
    local path="gs://${BUCKET_EXTERNAL_SHARED}/$output_external"
    gsutil cp --recursive $output_internal/ $path/
    touch _SUCCESS
    gsutil cp _SUCCESS $path/
}


# Copy local data to a remote bucket that is accessible to the current server.
#
# Arguments:
#   $1 - relative path to a folder containing data
#
# Environment:
#   TARGET - The minio host
#   BUCKET_INTERNAL_PRIVATE - The bucket pointing to this server's data
function send_output_internal() {
    local output=$1
    local path="gs://${BUCKET_INTERNAL_PRIVATE}/$output"
    gsutil cp --recursive $output/ $path/
    touch _SUCCESS
    gsutil cp _SUCCESS $path/
}


# List partitions that are ready for processing.
#
# Arguments:
#   $1 - relative path to a folder containing data
function list_partitions() {
    local input=$1
    find $input -type f -not -name "_SUCCESS" -printf "%f\n"
}


function verify1() {
    local input="raw"
    local output_internal="intermediate/internal/verify1"
    local output_external="intermediate/external/verify1"

    fetch_input_private $input

    for filename in $(list_partitions $input); do
        prio verify1 \
            --input $input/$filename \
            --output $output_internal
    done

    send_output_external $output_internal $output_external
}


function verify2() {
    local input_internal="intermediate/internal/verify1"
    local input_external="intermediate/external/verify1"
    local output_internal="intermediate/internal/verify2"
    local output_external="intermediate/external/verify2"

    fetch_input_shared $input_external

    for filename in $(list_partitions $input_internal); do
        prio verify2 \
            --input $input/$filename \
            --input-internal $input_internal/$filename \
            --input-external $input_external/$filename \
            --output $output_internal
    done

    send_output_external $output_internal $output_external
}


function aggregate() {
    local input_internal="intermediate/internal/verify2"
    local input_external="intermediate/external/verify2"
    local output_internal="intermediate/internal/aggregate"
    local output_external="intermediate/external/aggregate"

    fetch_input_shared $input_external

    for filename in $(list_partitions $input_internal); do
        prio aggregate \
            --input $input/$filename \
            --input-internal $input_internal/$filename \
            --input-external $input_external/$filename \
            --output $output_internal
    done

    send_output_external $output_internal $output_external
}


function publish() {
    local input_internal="intermediate/internal/aggregate"
    local input_external="intermediate/external/aggregate"
    local output="processed"

    fetch_input_shared $input_external

    for filename in $(list_partitions $input_internal); do
        prio publish \
            --input-internal $input_internal/$filename \
            --input-external $input_external/$filename \
            --output $output
    done

    jq -c '.' $output/*.ndjson

    send_output_internal $output
}


function main() {
    cd /tmp && create_folders

    verify1
    verify2
    aggregate
    publish
}

main "$@"
