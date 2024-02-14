# Sequenza Pyclone parser

## About
A parser to convert the output of the [Sequenza](https://bitbucket.org/sequenzatools/sequenza/src/master/) algorithm 
as an input for the [Pyclone](https://github.com/Roth-Lab/pyclone-vi) algorithm.

This script is based on the [Sequenze2Pyclone](https://github.com/ElizabethBorden/Run_fastclone_pipeline/blob/master/sequenza2pyclone.py) script.
The original script was erroneous, probably due to compatibility issues among different versions of the packages.
The script has been edited for use, and has been tested functional as of February 14, 2024.

## Getting Started

First clone the repository using the command

```bash
$ git clone 
```

To use the program, simply use

```bash
$ python3 convert.py -m <mutation_file> -s <segment_file> -n <sample_name> -o <out_filepath>
```

here, the input parameters represent:

- **mutation_file**: The file path of the [Mutect2](https://gatk.broadinstitute.org/hc/en-us/articles/360037593851-Mutect2) output, additionally filtered using the **filter function** and the **variant selection** of the [gatk](https://gatk.broadinstitute.org/hc/en-us) package.
- **segment_file**: The file path of the segment output of the [Sequenza](https://bitbucket.org/sequenzatools/sequenza/src/master/) output.
- **sample_name**: The name of the sample in string format. Can be selected arbitrarily
- **out_filepath**: The output file path.


Please read the [Input files](#input-files) section for the guide to generate each files.

## Input files

### Mutation file

The mutation file is generated using the pipeline in this [Mutect2 tutorial](https://gatk.broadinstitute.org/hc/en-us/articles/360035531132--How-to-Call-somatic-mutations-using-GATK4-Mutect2) to call somatic mutations, followed by the [SelectVariant](https://gatk.broadinstitute.org/hc/en-us/articles/360037055952-SelectVariants) tutorial to only select the filtered results. 

Note that for an error-free run of the program, it is very important to **filter the variants after the Mutect2 run**.

### Segment file

The segment file is part of the [Sequenza](https://bitbucket.org/sequenzatools/sequenza/src/master/) outputs.
(The list of the output files can be seen in the Sequenza repository.)

The input file is the **<sample_name>_segments.txt** of the outputs.

## References

Favero F, Joshi T, Marquard AM, Birkbak NJ, Krzystanek M, Li Q, Szallasi Z, Eklund AC. Sequenza: allele-specific copy number and mutation profiles from tumor sequencing data. Ann Oncol. 2015 Jan;26(1):64-70. doi: 10.1093/annonc/mdu479. Epub 2014 Oct 15. PMID: 25319062; PMCID: PMC4269342.

Roth A, Khattra J, Yap D, Wan A, Laks E, Biele J, Ha G, Aparicio S, Bouchard-Côté A, Shah SP. PyClone: statistical inference of clonal population structure in cancer. Nat Methods. 2014 Apr;11(4):396-8. doi: 10.1038/nmeth.2883. Epub 2014 Mar 16. PMID: 24633410; PMCID: PMC4864026.

McKenna A, Hanna M, Banks E, Sivachenko A, Cibulskis K, Kernytsky A, Garimella K, Altshuler D, Gabriel S, Daly M, DePristo MA. The Genome Analysis Toolkit: a MapReduce framework for analyzing next-generation DNA sequencing data. Genome Res. 2010 Sep;20(9):1297-303. doi: 10.1101/gr.107524.110. Epub 2010 Jul 19. PMID: 20644199; PMCID: PMC2928508.

