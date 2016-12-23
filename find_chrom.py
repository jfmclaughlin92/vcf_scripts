#!/usr/bin/env python
# encoding: utf-8

"""
File: find_chrom.py
Author: Jessica McLaughlin
Last update: 4 October 2016
Info: Given BLASTn output (in .xml format), find the loci mapped to a given chromosome
"""  

import os
import sys
import argparse
import re
import vcf
from Bio.Blast import NCBIXML
from phyluce.helpers import FullPaths, is_file, is_dir
from phyluce.log import setup_logging

def get_args():
	"""Get arguments from user"""
	parser = argparse.ArgumentParser(
		description="Given BLASTn output (in .xml format), find the loci mapped to a given chromosome"
		)
	parser.add_argument(
		'--input_xml',
		required=True,
		action=FullPaths,
		type=is_file,
		help='the input BLASTn xml files'
	)
	parser.add_argument(
		'--input_vcf',
		required=True,
		action=FullPaths,
		type=is_file,
		help='the input BLASTn xml files'
	)
	parser.add_argument(
		'--chromosome',
		required=True,
		type=str,
		help='the chromosome of interest to filter by'
	)	
	parser.add_argument(
		'--log-path',
		action=FullPaths,
		type=is_dir,
		default=None,
		help='Directory in which to store log file'
	)
	parser.add_argument(
		'--output_vcf',
		required=True,
		action=FullPaths,
		type=is_file,
		help='the input BLASTn xml files'
	)
	parser.add_argument(
        "--verbosity",
        type=str,
        choices=["INFO", "WARN", "CRITICAL"],
        default="INFO",
        help="""The logging level to use."""
    )
	return parser.parse_args()


def get_match_records(log,input,chromosome): # parse the blast_records and create dict of matched/unmatched uces
	result_handle = open(input)
	blast_records = NCBIXML.parse(result_handle)
	chrom = 'chromosome '+chromosome
	matched_records = []
	match_count = 0
	for blast_record in blast_records:
		for alignment in blast_record.alignments:
			for hsps in alignment.hsps:
				if chrom in alignment.title:
					print blast_record.query	
					matched_records.append(blast_record.query) # store matching chromosomes w/ key
					match_count+=1
					log.info(blast_record.query+" is a match!")
				else:
					pass
					log.info(blast_record.query+" is NOT a match!")
	log.info(str(match_count)+" records for "+ chrom)
	return matched_records
	
def fix_labels(loci_list,log): # fix labels to match vcf NOTE: SPECIFIC LABELS USED
	log.info("fixing labels.....")
	new_labels = []
	for locus in loci_list:
		nospace_locus = re.sub(r'\s?','',locus)
		#print nospace_locus
		short_locus = re.sub(r'\|uce-?[0123456789]{1,4}','',nospace_locus)
		print short_locus
		new_labels.append(short_locus)
	return new_labels
	
#def get_names(vcf_reader, loci_list):
	vcf_loci = []
	
#	for record in vcf_reader:
#		vcf_loci.append(record.CHROM)

#	newvcf_loci = list(set(vcf_loci)-set(loci_list))
		
#	for locus in vcf_loci:
#		for name in loci_list:
#			if locus == name: #and name in vcf_loci:
#				if locus not in vcf_loci:
#					pass
#				else:
#					vcf_loci.remove(locus)
#				vcf_loci.remove(locus)
#				print "YAY!!!!"
#			else:
#				print "FML"
	
#	return newvcf_loci
	
def create_vcf(log,input_vcf,output_vcf,use_loci):
	try:
		reader = vcf.Reader(open(input_vcf, 'r'))
		log.info("Reading vcf....")
	except:
			log.critical("Could not open vcf file")
			raise IOError("vcf file "+input_vcf+" could not be opened")
	try:
		writer = vcf.Writer(open(output_vcf, 'w'), reader) 
		log.info('Output vcf created')
	except:
			log.critical('Could not create output vcf file')
			raise IOError('Could not create output vcf file')
			
#	names = get_names(reader,use_loci) # get inverse loci list

	vcf_loci = []
	
	for record in reader:
		vcf_loci.append(record.CHROM)

	newvcf_loci = list(set(vcf_loci)-set(use_loci))
	
	try:
		reader = vcf.Reader(open(input_vcf, 'r'))
		log.info("Reading vcf....")
	except:
			log.critical("Could not open vcf file")
			raise IOError("vcf file "+input_vcf+" could not be opened")
	
	locus_count = 0		
	for record in reader: # for each record
		for locus in newvcf_loci:
			if record.CHROM in locus: # write record to new vcf if not on chrom to be excluded
				writer.write_record(record)	
				locus_count+=1
			else:
				pass
	log.info("Printed "+str(locus_count)+" loci to vcf.")
	return output_vcf

def main():
	# get args
	args = get_args()
    # setup logging
	log, my_name = setup_logging(args) 
	log.info("Logging set-up")
	
	matches = get_match_records(log,args.input_xml,args.chromosome)
	matches_names = fix_labels(matches, log)
	vcf.output = create_vcf(log,args.input_vcf,args.output_vcf,matches_names)
	log.info("Done!")

if __name__ == '__main__':
	main()		


