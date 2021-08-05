def map_alleles_from_chromosomes(chromosomes, ref_dict_row):
    alleles = chromosomes.split("|")
    allele_list = []
    for allele in alleles:
        # 0 means map from ref
        if allele == "0":
            allele_list.append(ref_dict_row[3])
        # 1 means map from alt
        else:
            # because the first vcf always had one alt allele at each position, we have the strange indexing here
            # this can be changed for different vcfs if need be
            allele_list.append(ref_dict_row[4][0][0])
    return allele_list


# input is variants: 0 is original alt from vcf, 1 is L, 2 is S
# remember that all of these can themselves be lists
def translate_extra_symbols(allele_list):
    allele_set = []
    for founder_allele_index in range(len(allele_list)):
        allele_set= set()
        # purine
        if allele_list[founder_allele_index] == "R":
            allele_set.add("G")
            allele_set.add("A")

        # pyrimidine
        elif allele_list[founder_allele_index] == "Y":
            allele_set.add("C")
            allele_set.add("T")
        # G or T
        elif allele_list[founder_allele_index] == "K":
            allele_set.add("G")
            allele_set.add("T")
        # A or C
        elif allele_list[founder_allele_index] == "M":
            allele_set.add("A")
            allele_set.add("C")
        # G or C
        elif allele_list[founder_allele_index] == "S":
            allele_set.add("G")
            allele_set.add("C")
        # A or T
        elif allele_list[founder_allele_index] == "W":
            allele_set.add("A")
            allele_set.add("T")
        # G, T, or C
        elif allele_list[founder_allele_index] == "B":
            allele_set.add("G")
            allele_set.add("T")
            allele_set.add("C")
        # G, A, or T
        elif allele_list[founder_allele_index] == "D":
            allele_set.add("G")
            allele_set.add("A")
            allele_set.add("T")
        # A, C, or T
        elif allele_list[founder_allele_index] == "H":
            allele_set.add("A")
            allele_set.add("C")
            allele_set.add("T")
        # G, C, or A
        elif allele_list[founder_allele_index] == "V":
            allele_set.add("G")
            allele_set.add("C")
            allele_set.add("A")
        # A, G, C, or T
        elif allele_list[founder_allele_index] == "N":
            allele_set.add("A")
            allele_set.add("G")
            allele_set.add("C")
            allele_set.add("T")
        else:
            allele_set.add(allele_list[founder_allele_index])
    return allele_set


# simply checks if this particular allele exists in the lg founder
# must account for extra encoding
def allele_in_large(allele, alleles):
    if allele in translate_extra_symbols(alleles[4][1]):
        return True
    return False


# simply checks if this particular allele exists in the sm founder
def allele_in_small(allele, alleles):
    if allele in translate_extra_symbols(alleles[4][2]):
        return True
    return False


# 1 -> LG -> L, 2 -> SM -> S, if in 1 and 2 -> B, if in neither 1 or 2 -> O
def generate_new_allele_map(alleles, allele_list):
    new_chrom_list = []
    for allele in allele_list:
        if allele_in_large(allele, alleles) and allele_in_small(allele, alleles):
            new_chrom_list.append("B")
        elif allele_in_large(allele, alleles):
            new_chrom_list.append("L")
        elif allele_in_small(allele, alleles):
            new_chrom_list.append("S")
        else:  # if in neither
            new_chrom_list.append("O")
    # now get it into output form, L|O etc.
    return "|".join(new_chrom_list)


#
def declare_allele_class(ref_dict_row, sample_dict_row):
    # update each sample to translate 0|1 to L|S, etc.
    for sample in range(len(sample_dict_row)):
        # first add the lg and small alleles to the alt alleles in the reference dict
        allele_list = map_alleles_from_chromosomes(sample_dict_row[sample], ref_dict_row)
        # then translate the allele mapping from ref or alt to lg/sm
        new_chrom_map = generate_new_allele_map(ref_dict_row, allele_list)
        sample_dict_row[sample] = new_chrom_map
    return sample_dict_row
