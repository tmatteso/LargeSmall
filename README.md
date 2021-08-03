How to run the script:
Simply call the script via python in the same working directory as the "data" folder. The script takes two command line arguments: the filepath to vcf file that you seek to analyze, and the desired file name for the output.

Files in data folder:
The data folder contains the founder genotypes ESM3-6, which tell the script which indels and SNPs belong to which founder and where. You can also place the vcf file you seek to analyze in the data folder to have all the inputs in one place.

Tips on running:
The script will periodically return print statements at the command line telling you of its progress, if you don't see one of these for more than 5 mintues either the program has crashed or run out of memory. The output file will be stored in whatever working directory you started the file in, hopefully keeping it separate from the input. 
