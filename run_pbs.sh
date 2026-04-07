#!/bin/bash
#PBS -N singularity_one
#PBS -l select=1:ncpus=1
#PBS -l walltime=00:05:00
#PBS -j oe

cd $PBS_O_WORKDIR

mkdir -p output_pbs

echo "===== PBS JOB START ====="
echo "HOSTNAME: $(hostname)"
echo "WORKDIR : $(pwd)"
echo "DATE    : $(date)"

singularity exec python_env.sif \
    python analyze.py sample_data/data_02.csv output_pbs

echo "===== PBS JOB END ====="
