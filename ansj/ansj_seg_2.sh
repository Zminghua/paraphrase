#!/bin/bash
set -u
set -x

date +'%Y.%m.%d %H:%M:%S'
infile=$1
outfile=$2
config=$3

find src -name \*.java > jfile
javac -d bin/ -cp .:./lib/* @jfile
if [ $? -ne 0 ]; then
    echo "compile error"
    exit 1
else
    echo "compile complete"
fi

rm jfile ${outfile}
cd bin
java -cp .:../lib/* zmh.Seg ${infile} ${outfile} ${config}
if [ $? -ne 0 ]; then
    echo "ansj error"
    exit 1
else
    echo "ansj complete"
fi

date +'%Y.%m.%d %H:%M:%S'

