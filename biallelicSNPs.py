#!/usr/bin/env python
# encoding: utf-8

"""
File: biallelicSNP.py
Author: Jessica McLaughlin
Last update: 23 Dec 2016
Info: count and remove SNPs that are not biallelic in a given vcf file
"""  

import argparse
import vcf

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

def count_ALTalleles(input_vcf,output_vcf):
	try:
		reader = vcf.Reader(open(input_vcf, 'r')) #open input
		print("Reading vcf....")
	except:
			print("Could not open vcf file")
			raise IOError("vcf file "+input_vcf+" could not be opened")
	
	try:
		writer = vcf.Writer(open(output_vcf, 'w'), reader) 
		print('Output vcf created')
	except:
			print('Could not create output vcf file')
			raise IOError('Could not create output vcf file')
			
	biallelic_SNPs = 0
	pass_SNPs = 0
	record_count = 0
						
	for record in reader:
		record_count+=1
		if len(record.ALT) == 1:
			writer.write_record(record)	
			biallelic_SNPs+=1
		else:
			pass_SNPs+=1
	
	print("From "+str(record_count)+" input SNPs, "+str(biallelic_SNPs)+" printed to output, "+str(pass_SNPs)+" removed")
	
	return output_vcf		
	

def main():
	# get args
	args = get_args()

	new_file = count_ALTalleles(args.input_vcf,args.output_vcf)
	print("Done!")
	
if __name__ == '__main__':
	main()	
