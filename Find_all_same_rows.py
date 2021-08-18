import sys
def dic_of_ls_vcf_import(fName):
    with open(fName, 'r') as f:
        # skip a number of comment lines, varies by vcf file
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


def check_samples(first_sample, sample_ls):
    for sample in sample_ls:
        if sample != first_sample:
            return False
    return True


def write_output(filename, output_ls):
    new_col_names = ["Position", "Sample"]
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
    print("import complete")
    output_ls = []
    for position in sample_dict.keys():
        first_sample = sample_dict[position][0]
        if check_samples(first_sample, sample_dict[position]):
            output_ls.append([position, first_sample])
    print("samples checked")
    # write output
    write_output(sys.argv[2], output_ls)
    print("export complete")


if __name__ == "__main__":
    main()