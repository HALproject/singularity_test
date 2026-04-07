#!/bin/bash
#PBS -N singularity_array
#PBS -l select=1:ncpus=1
#PBS -l walltime=00:05:00
#PBS -J 1-5
#PBS -j oe

cd $PBS_O_WORKDIR

mkdir -p output_array

FILE=$(printf "sample_data/data_%02d.csv" ${PBS_ARRAY_INDEX})

echo "===== PBS ARRAY JOB START ====="
echo "ARRAY INDEX: ${PBS_ARRAY_INDEX}"
echo "HOSTNAME   : $(hostname)"
echo "WORKDIR    : $(pwd)"
echo "TARGET FILE: ${FILE}"
echo "DATE       : $(date)"

singularity exec python_env.sif \
    python analyze.py ${FILE} output_array

echo "===== PBS ARRAY JOB END ====="
