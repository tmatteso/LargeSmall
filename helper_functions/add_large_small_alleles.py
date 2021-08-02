

# function to check if a locus exists in a founder ESM
def find_founder_row(pos_number, founder, founder_dicts):
    # return the row in the founder where the position matches
    if founder_dicts[founder].get(pos_number) is not None:
        return founder_dicts[founder][pos_number]
    # if nothing for a founder at this position, return an empty ls
    return []


# split the allele string on the /, turn into set to eliminate duplicate alleles, then back to list
def process_alleles(variant_str):
    # this if statement is here for SNPs
    if "/" not in variant_str:
        return list(variant_str)
    # this eliminates the excess in duplicate homozygous alleles (for indels)
    alleles = list(set(variant_str.split("/")))
    return alleles


def produce_new_alt_allele_entries(founder_rows, ref_dict_row):
    # turn the ALT into a list, add the founder alleles at this locus to the list
    ref_dict_row[5] = [[ref_dict_row[5]]]
    for founder_row in founder_rows:
        if founder_row != []:
            alleles = process_alleles(founder_row[1])
            ref_dict_row[5].append(alleles)
        # if no founder allele at this locus, append an empty list
        elif founder_row == []:
            ref_dict_row[5].append([])
        else:
            raise ValueError("Founder Error detected")
    return ref_dict_row
