#!/bin/bash
set -u
set -x

date +'%Y.%m.%d %H:%M:%S'
insource=$1
intarget=$2
outfile=$3
config=$4

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
java -cp .:../lib/* Parser ${insource} ${intarget} ${outfile} ${config}
if [ $? -ne 0 ]; then
    echo "parser error"
    exit 1
else
    echo "parser complete"
fi

date +'%Y.%m.%d %H:%M:%S'

