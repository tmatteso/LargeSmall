How to run the script: \n
Simply call the script via python in the same working directory as the "data" folder. The script takes two command line arguments: the filepath to vcf file that you seek to analyze, and the desired file name for the output.

Files in data folder: \n
The data folder contains the founder genotypes ESM3-6, which tell the script which indels and SNPs belong to which founder and where. You can also place the vcf file you seek to analyze in the data folder to have all the inputs in one place.

Tips on running: \n
The script will periodically return print statements at the command line telling you of its progress, if you don't see one of these for more than 5 mintues either the program has crashed or run out of memory. The output file will be stored in whatever working directory you started the file in, hopefully keeping it separate from the input. 

The grep_script: \n
grep_script.sh returns as std out the number of "O|O", "B|B", and all other allele pairs combined there are in the file.

Downstream Analysis Python Scripts: \n
Each script takes two command line arguments: the filepath to vcf file that you seek to analyze, and the desired file name for the output.
LS_same.py returns an output file that contains every chromosome position where the large allele is the small allele and the allele that is shared. This includes positions where neither founder has a reference allele.
Find_all_same_rows.py returns an output file that contains every chromosome position where all samples have the same pair of alleles ("O|O", etc.) and the pair of alleles shared at that position. 
Position_pairs.py should return the positions for each sample that has one of the pairs we're looking for ((L|L,S|S) and reverse, (L|L,L|S) and reverse, and (S|S,S|L) and reverse. This script is not ready yet, see update email for details.
