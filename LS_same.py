import sys


def dic_of_ls_vcf_import(fName):
    with open(fName, 'r') as f:
        # skip a number of comment lines, varies by vcf file
        sample_dict, ref_dict, col_list = {}, {}, {}
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
            #if counter == 1000:
                #break

    return sample_dict, ref_dict, col_list


def write_output(filename, output_ls):
    new_col_names = ["Position", "Identical_Allele"]
    # parse the output ls
    filename = open(filename, "w")
    join = "\t".join(new_col_names)
    filename.write(join + "\n")
    for sub_ls in output_ls:
        join = "\t".join(sub_ls)
        filename.write(join + "\n")
    filename.close()


def main():
    assert len(sys.argv) == 3, "Did you specify a vcf input filepath and output file name?"
    sample_dict, ref_dict, col_list = dic_of_ls_vcf_import(sys.argv[1])
    output_ls = []
    # go through every alt entry, if [1] == [2] -> say are same
    for position in ref_dict.keys():
        alt_index = col_list.index("ALT")
        alt_list = ref_dict[position][alt_index].split(",")
        if alt_list[1] == alt_list[2]:
            output_ls.append([position, alt_list[1]])
    write_output(sys.argv[2], output_ls)


if __name__ == "__main__":
    main()