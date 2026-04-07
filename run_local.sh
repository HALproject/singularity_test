#!/bin/bash

set -e

mkdir -p output

echo "Running locally with Singularity..."

singularity exec python_env.sif \
    python analyze.py sample_data/data_01.csv output

echo "Done."
