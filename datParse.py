#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description= 'Filter out host specific contigs')
parser.add_argument('-b', '--blast_file', type = str, metavar='',required=True, help='BLAST file with Queries and matches')
parser.add_argument('-o', '--output', type = str, metavar='',required=True, help='Name of output file', default='output.fasta')
parser.add_argument('-u', '--uniprot', type = str, metavar='',required=True, help='Uniprot database')
parser.add_argument('-f', '--fasta_file', type = str, metavar='',required=True, help='Fasta file with contigs')

args = parser.parse_args()

blastx = args.blast_file
uniprot = args.uniprot
output_file = args.output
contig_file = args.fasta_file
Query_dict = {}

with open(blastx, 'r') as blast:
    for line in blast:
        if line.startswith('Query='):
            Query = line.rstrip().split(' ')[1]
            for skip in range(6):
                line = blast.readline()
            
            if '|' in line:
                id = line.split('|')[1].upper()
                Query_dict[Query] = id


bird_list = []
with open(uniprot, 'r') as unip:
    for line in unip:
        if line.startswith('AC'):
            id = line.upper().rstrip('\n').replace('AC  ','').replace(' ','').rstrip(';').split(';')
            animal_class = []
        if line.startswith('OC'):
            class_list = line.upper().rstrip('\n').replace('OC','').replace(' ','').rstrip(';').split(';')
            
            for i in class_list:
                animal_class.append(i)

        if line.startswith('OX'):
            if 'AVES' in animal_class:
                for uniq_id in id:
                    bird_list.append(uniq_id)


bird_contigs = []
for Query, id in Query_dict.items():
        if id in bird_list:
           bird_contigs.append(Query)


scaffold_list = set()
with open(contig_file, 'r') as contigs:
    for line in contigs:
        if line.startswith('>'):
            contig = line.split('\t')[0].replace('>','')
            if contig in bird_contigs:
                scaffold = line.split('\t')[2]
                scaffold_list.add(scaffold)


contig_dict = {}
with open(output_file, 'w') as output, open(contig_file, 'r') as contigs:
    for line in contigs:
        if line.startswith('>'):
            contig = line.split('\t')[2].split('=')[1]

            if contig in scaffold_list:
                pass

            else:
                if contig not in contig_dict and len(contig_dict) > 0:
                    for key, item in contig_dict.items():
                        output.write(f'>{key}\n{item}\n')
                    contig_dict = {}
                    contig_dict[contig] = ''
                

                if contig not in contig_dict and len(contig_dict) == 0:

                    contig_dict[contig] = ''

                else:
                    seq_line = contigs.readline().rstrip()
                    contig_dict[contig] += seq_line

        else:
            pass
    for key, item in contig_dict.items():
        output.write(f'>{key}\n{item}\n')

            

