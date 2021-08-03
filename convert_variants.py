import helper_functions.add_large_small_alleles as add_alleles
import helper_functions.remap_chromosomes as remap
import helper_functions.parse_dicts as parse_dicts
import sys


def main():
    # import the ESMs
    lg_snp = parse_dicts.dic_of_ls_founders_import("data/12864_2015_1592_MOESM3_ESM")
    lg_indel = parse_dicts.dic_of_ls_founders_import("data/12864_2015_1592_MOESM4_ESM")
    sm_snp = parse_dicts.dic_of_ls_founders_import("data/12864_2015_1592_MOESM5_ESM")
    sm_indel = parse_dicts.dic_of_ls_founders_import("data/12864_2015_1592_MOESM6_ESM")
    print("import complete")

    # import the vcf
    sample_dict, ref_dict, col_list = parse_dicts.dic_of_ls_vcf_import(sys.argv[1])
    print("vcf done")

    # merge dicts
    lg_indel.update(lg_snp)
    sm_indel.update(sm_snp)
    founder_dicts = {"lg": lg_indel, "sm": sm_indel}
    print("founder dict conversion complete")

    # go through the vcf, if a position matches one in lg or small, append the allele
    for pos_number in ref_dict.keys():
        # for all positions in vcf that are in a founder
        lg_row = add_alleles.find_founder_row(pos_number, "lg", founder_dicts)
        sm_row = add_alleles.find_founder_row(pos_number, "sm", founder_dicts)
        founder_rows = [lg_row, sm_row]
        # add the lg and sm alleles to the reference dict
        ref_dict[pos_number] = add_alleles.produce_new_alt_allele_entries(founder_rows, ref_dict[pos_number])
        # translate the allele mapping for each sample
        sample_dict[pos_number] = remap.declare_allele_class(ref_dict[pos_number], sample_dict[pos_number])
    print("allele processing done")

    # write the output file
    parse_dicts.write_output(ref_dict, sample_dict, col_list, "modifiedLS.vcf")
    print("export done")


if __name__ == "__main__":
    main()
