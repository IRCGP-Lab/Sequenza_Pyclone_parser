from collections import defaultdict
import pandas as pd
import gzip
import argparse


def convert(mutation_file, segment_copynumber_file, sample_name, out_dir):
    mutation_list, chr_list, pos_list, ref_allele, var_allele, ref_reads, alt_reads, snp_chr_pos, VAF =\
        [], [], [], [], [], [], [], [], []
    with gzip.open(mutation_file, 'r') as f_mutation:
        for ele in f_mutation.readlines():
            ele = ele.decode()
            if (not ele.startswith('#')) and (not ele.startswith("chrM")):
                line = ele.strip().split('\t')
                chro_pos = line[0] + ':' + line[1]
                chr_name = line[0]
                pos_loc = line[1]
                ref_n = line[3]
                alt_n = line[4]
                mut_id = sample_name + ":" + chro_pos
                tumor_read_info = line[10].split(':')
                alt_count = int(tumor_read_info[1].split(',')[1])
                ref_count = int(tumor_read_info[1].split(',')[0])
                vaf = float(tumor_read_info[2])
                chr_list.append(chr_name)
                pos_list.append(pos_loc)
                ref_allele.append(ref_n)
                var_allele.append(alt_n)
                ref_reads.append(ref_count)
                alt_reads.append(alt_count)
                snp_chr_pos.append(chro_pos)
                mutation_list.append(mut_id)
                VAF.append(vaf)

    data_snp = pd.DataFrame()
    data_snp["mutation_id"] = mutation_list
    data_snp['chrom'] = chr_list
    data_snp['position'] = pos_list
    data_snp['ref_counts'] = ref_reads
    data_snp['var_counts'] = alt_reads

    data_copynumber = pd.read_csv(segment_copynumber_file, header=0, sep='\t')
    data_cn_count = data_copynumber[['chromosome', 'start.pos', 'end.pos', 'CNt', 'A', 'B']]
    range_dic = defaultdict(list)
    for i in range(len(data_cn_count.chromosome)):
        range_dic[data_cn_count.chromosome[i]].append(
            [data_cn_count['start.pos'][i], data_cn_count['end.pos'][i], data_cn_count.CNt[i], data_cn_count.A[i],
             data_cn_count.B[i]])

    CNT_list = []
    CNA_list = []
    CNB_list = []
    # print(chr_list)
    for i in range(len(data_snp.chrom)):
        chr_str = data_snp.chrom[i]
        # print(data_snp)
        pos = pos_list[i]
        flag = 0
        for ele in range_dic[chr_str]:
            start_pos, end_pos, CNT, CNA, CNB = ele[0:5]
            if int(start_pos) <= int(pos) <= int(end_pos):
                CNT_list.append(CNT)
                CNA_list.append(CNA)
                CNB_list.append(CNB)
                flag = 1
                break
        if flag == 0:
            CNT_list.append(2)
            CNA_list.append(2)
            CNB_list.append(0)

    data_snp['normal_cn'] = 2
    data_snp['minor_cn'] = CNB_list
    data_snp['major_cn'] = CNA_list
    data_snp['variant_case'] = "test"
    data_snp["variant_freq"] = VAF

    genotype_list = []

    for i in range(len(data_snp.chrom)):
        if int(data_snp.minor_cn[i]) == int(data_snp.major_cn[i]):
            genotype = "AB"
        else:
            genotype = "BB"
        genotype_list.append(genotype)
    data_snp["genotype"] = genotype_list

    del data_snp["chrom"]
    del data_snp["position"]

    data_snp.to_csv(out_dir + "/" + sample_name + "_sequenza2pyclone.txt", header=True, sep="\t", index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sequenza_Pyclone_parser")

    parser.add_argument("-m", "--mutation", required=True, help="Mutation file")
    parser.add_argument("-s", "--segment", required=True, help="Segment file")
    parser.add_argument("-n", "--name", required=True, help="Sample name")
    parser.add_argument("-o", "--out", required=True, help="Output directory")

    args = parser.parse_args()

    convert(args.mutation, args.segment, args.name, args.out)
