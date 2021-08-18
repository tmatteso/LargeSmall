import sys


# import the vcf with vaex
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
            if counter == 10000:
                break

    return sample_dict, ref_dict, col_list


def sample_type(sample):
    if sample == "L|L":
        return 1
    elif sample == "S|S":
        return 2
    elif sample == "L|S" or sample == "S|L":
        return 3
    else:
        return 0


def in_acceptable_matches(sample_pair):
    acceptable_matches = [[1, 2], [2,1], [1,3], [3,1], [2,3], [3,2]]
    if sample_pair in acceptable_matches:
        return True
    return False


# for one sample, multiple positions
def analyze_samples(sample_dict, col_list):
    # struct: { SAMPLE :{"L|L":[position_1, position_2, ...]}}
    new_dict = {}
    # this indexing is not right
    for sample_index in range(len(col_list)):
        if sample_index >= 9:
            for position in sample_dict.keys():
                if new_dict.get(col_list[sample_index]) is None:
                    new_dict[col_list[sample_index]] = {}
                if (new_dict[col_list[sample_index]]).get(sample_dict[position][sample_index-9]) is None:
                    new_dict[col_list[sample_index]][sample_dict[position][sample_index-9]] = []
                new_dict[col_list[sample_index]][sample_dict[position][sample_index-9]].append(position)

    # now go through new_dict
    # stay within each sample
    output_ls = []
    for sample_name in new_dict.keys():
        for sample_1 in new_dict[sample_name].keys():
            for sample_2 in new_dict[sample_name].keys():
                if in_acceptable_matches([sample_type(sample_1), sample_type(sample_2)]):
                    # report all combos
                    for i in new_dict[sample_name][sample_1]:
                        for j in new_dict[sample_name][sample_2]:
                            temp_ls = [sample_name, sample_1, sample_2, str(i), str(j)]
                            output_ls.append(temp_ls)
    return output_ls


def write_output(filename, output_ls):
    new_col_names = ["Sample", "Alleles_at_P1", "Alleles_at_P2", "Pos_1", "Pos_2"]
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
    # access the df on sample columns (index:)
    sample_output = analyze_samples(sample_dict, col_list)
    print("sample pairs complete")
    # write output
    write_output(sys.argv[2], sample_output)
    print("export complete")


if __name__ == "__main__":
    main()


