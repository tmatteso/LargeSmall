#!/bin/bash
# take command line arg input
input=$1
# pipe the count out as a couple echos
# needs a loop for all *|*, then execute each statement inside the loop
echo "Number of O|O genotypes" 
grep -o -i "O[|]O" ${input} | wc -l
echo "Number of B|B genotypes" 
grep -o -i "B[|]B" ${input} | wc -l
echo "Number of all other genotypes" 
grep -E -o -i "[OB][|][^OB]|[^OB][|][OB]|[^OB][|][^OB]|[B][|][O]|[O][|][B]" ${input} | wc -l

