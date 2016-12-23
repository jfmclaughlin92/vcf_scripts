#!/usr/bin/env python
# encoding: utf-8

"""
File: randomSNP.py
Author: Jessica McLaughlin
Last update: 22 Dec 2016
Info: Thin an input .vcf file to a single random SNP per locus.
"""  

import argparse
import vcf
from random import sample

def get_args():
	"""Get arguments from user"""
	parser = argparse.ArgumentParser(
		description="Thin an input .vcf file to a single random SNP per locus"
		)
	parser.add_argument(
		'--input_vcf',
		required=True,
		#action=FullPaths,
		#type=is_file,
		help='the input vcf file'
	)
	parser.add_argument(
		'--output_vcf',
		required=True,
		#action=FullPaths,
		#type=is_file,
		help='the output vcf file name'
	)
	return parser.parse_args()
	
def get_locus_list(input_vcf):
	try:
		reader = vcf.Reader(open(input_vcf, 'r')) # open input vcf for reading
		print("Reading vcf....")
	except:
			print("Could not open vcf file")
			raise IOError("vcf file "+input_vcf+" could not be opened") # crash and burn if can't open
			
	vcf_loci = [] # create empty list to iterate over
	
	for record in reader:
		vcf_loci.append(record.CHROM) # append loci names to list
	
	loci_list = list(set(vcf_loci)) # remove duplicates
#	print loci_list

	print("Using "+ str(len(loci_list))+" unique loci")	
	return loci_list

def map_records(input_vcf):
	try:
		reader = vcf.Reader(open(input_vcf, 'r')) # open input vcf for reading
		print("Reading vcf....")
	except:
			print("Could not open vcf file")
			raise IOError("vcf file "+input_vcf+" could not be opened") # crash and burn if can't open
			
	vcf_map = [] # create empty list to iterate over
	map_count = 0
	for record in reader:
		vcf_map.append([record.CHROM,record.POS]) # append loci names to list
		map_count+=1
		
	print("records mapped!")
	print(map_count)
	return vcf_map

def get_snp_list(locus,map):
#	try:
#		reader = vcf.Reader(open(input_vcf, 'r'))
#		print("Reading vcf....")
#	except:
#			print("Could not open vcf file")
#			raise IOError("vcf file "+input_vcf+" could not be opened")

	
	SNP_records = []
	for record in map: # for each record
				
		if record[0] == locus:
			SNP_records.append(record)
#			print("RECORD: "+record[0])
		else:
				pass
	return SNP_records


def sample_snps(locus_list, input_vcf, output_vcf,map):

	use_snp_list = []
	use_snp_count = 0
	for locus in locus_list:
		snps_for_locus = get_snp_list(locus,map)
		random_record=sample(snps_for_locus, 1)
		use_snp_list.append(random_record)
		use_snp_count+=1
	print("Using "+str(use_snp_count)+" snps")
	
	
	try:
		reader = vcf.Reader(open(input_vcf, 'r'))
		print("Reading vcf....")
	except:
			print("Could not open vcf file")
			raise IOError("vcf file "+input_vcf+" could not be opened")
#	record_list = []
#	for record in reader:
# 		record_list.append(record)
	
	try:
		writer = vcf.Writer(open(output_vcf, 'w'), reader) 
		print('Output vcf created')
	except:
			print('Could not create output vcf file')
			raise IOError('Could not create output vcf file')
				
	locus_count = 0		# count how many loci we're keeping
	
	#print locus_list
	
	

		
	for record in reader:	
		for snp in use_snp_list:
			snp_data= snp[0]
			if record.CHROM == snp_data[0] and record.POS == snp_data[1]:		
				writer.write_record(record)	
				print("Selected record: "+record.CHROM)
				locus_count+=1
			else:
					pass
					
		
		
	print("Printed "+str(locus_count)+" loci to vcf.")
	return output_vcf

def main():
	# get args
	args = get_args()
	
	print("Getting locus list..........")
	locus_list = get_locus_list(args.input_vcf)
	record_map = map_records(args.input_vcf)
	print("Sampling SNPs..........")
	new_vcf = sample_snps(locus_list,args.input_vcf, args.output_vcf,record_map)
	print("Done!")

if __name__ == '__main__':
	main()	