#!/bin/sh

### this is a shell script
#$ -S /bin/sh

### use the current working directory for inputs and outputs
#$ -cwd

### minimise clutter by merging stdout and stderr to one file
#$ -j y

### email me upon (b)egin, (a)bort or (e)nd of this job
#$ -M viet.vo@monash.edu -m abe

### wall time requirement, format: hh:mm:ss (48 hours)
#$ -l h_rt=24:00:00

### memory requirements (upper bound)
#$ -l h_vmem=8G

### ask for four CPU cores
#$ -pe short 4

### body of the job

module load python/3.4.3
python3 demo.py
