def map_alleles_from_chromosomes(chromosomes, ref_dict_row):
    alleles = chromosomes.split("|")
    allele_list = []
    for allele in alleles:
        # 0 means map from ref
        if allele == "0":
            allele_list.append(ref_dict_row[4])
        # 1 means map from alt
        else:
            # because the first vcf always had one alt allele at each position, we have the strange indexing here
            # this can be changed for different vcfs if need be
            allele_list.append(ref_dict_row[5][0][0])
    return allele_list


# simply checks if this particular allele exists in the lg founder
def allele_in_large(allele, alleles):
    if allele in alleles[5][1]:
        return True
    return False


# simply checks if this particular allele exists in the sm founder
def allele_in_small(allele, alleles):
    if allele in alleles[5][2]:
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
        # first add the lg and small allels to the alt alleles in the reference dict
        allele_list = map_alleles_from_chromosomes(sample_dict_row[sample], ref_dict_row)
        # then translate the allele mapping from ref or alt to lg/sm
        new_chrom_map = generate_new_allele_map(ref_dict_row, allele_list)
        sample_dict_row[sample] = new_chrom_map
    return sample_dict_row
