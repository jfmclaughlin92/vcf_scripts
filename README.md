# vcf_scripts
Various scripts for filtering and manipulating vcf files for genomic analyses. All scripts require PyVCF; additional modules required listed where applicable.

find_chrom.py
Using BLASTn output (as an .xml), find loci mapped to a specific locus (user-specified) and create an output file excluding them.
Initially written to remove Z-linked loci from UCE datasets.
Requirements: BioPython, phyluce

biallelicSNPs.py
Find non-biallelic SNPs and create a new vcf file without them. Necessary for preparing files for analyses limited to biallelic data.

randomSNP.py
When thinning to 1 SNP per locus, select a random SNP (rather than just the first SNP listed).
