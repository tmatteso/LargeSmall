
def dic_of_ls_founders_import(fName):
    with open(fName, 'r') as f:
        # skip the first line, it's just a comment
        next(f)
        line = f.readline()
        entries = {}
        # col_list is here for debugging purposes
        col_list = line.strip("\n").split("\t")
        if len(col_list) == 1:
            # the last ESM has strange structure that necessitates this if statement
            col_list = (" ".join(col_list[0].split())).split(" ")

        for line in f:
            if line:
                line_in = (line.strip("\n")).split("\t")
                # read in each line, saving the position of the locus as the key and ref and alt alleles as values
                entries[line_in[1]] = line_in[2:]
    return entries


def dic_of_ls_vcf_import(fName):
    with open(fName, 'r') as f:
        # skip a number of comment lines, varies by vcf file

        line = f.readline()
        sample_dict, ref_dict = {}, {}
        counter = 0
        for line in f:
            if line.startswith("#CHROM"):
                # read in the first non-skipped line as the column names
                col_list = line.strip("\n").split("\t")
                counter += 1
                continue
            if counter >= 1 and line:
                counter += 1
                line_in = (line.strip("\n")).split("\t")
                # put each line into 2 dictionaries, where the keys in both are the position of the locus
                # sample_dict contains the "0|0" type allele mapping for each sample at this locus
                sample_dict[line_in[1]] = line_in[9:]
                # ref_dict contains all other entries for the locus from the imported vcf
                ref_dict[line_in[1]] = line_in[:9]

            # counter is here to check that the program runs with a subset of the input, where memory is not an issue
            #if counter == 10000:
                #break

    return sample_dict, ref_dict, col_list


def write_output(ref_dict, sample_dict, col_list, filename):
    filename = open(filename, "w")
    join = "\t".join(col_list[1:])
    filename.write(join + "\n")
    for pos_number in ref_dict.keys():
        # this stitches the ls of ls for the alternative alleles in the ref_dict into a str for better output parsing
        alt = ""
        #print(ref_dict[pos_number][4])
        for entry in ref_dict[pos_number][4]:
            alt = alt + "".join(entry) + ", "
        ref_dict[pos_number][4] = alt[:-2]

        # put the ref_dict and sample_dict back together again at each position
        row = ref_dict[pos_number]+sample_dict[pos_number]
        #print(row)
        join = "\t".join(row)
        filename.write(join + "\n")
    filename.close()
