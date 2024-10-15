#!/bin/bash

output_file="reads_scf.txt"

find ../data/set3 -type f -name "*.scf" > "$output_file"

cp config.bak config

pregap4 -config config -fofn "$output_file" -nowin

if [ -d "output" ]; then
    rm -rf output/*
else
    mkdir output
fi

mv *scf output/
mv *exp output/
mv "$output_file".* output/
