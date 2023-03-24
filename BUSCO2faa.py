#!/usr/bin/env python3

'''This script takes a list of common BUSCO ids and extracts the corresponding gene id from each species.
The gene id is then used to extract the gene sequence from the corresponding faa file.
The gene sequence is then written to a new file with the BUSCO id as the file name.
The script assumes that the BUSCO output folder is in the working directory and that the faa files are in a folder called "FAA" in the working directory.
The script also assumes that the BUSCO output folder is named "6_Busco" and that the faa files are in a folder called "5_gff_fasta" in the working directory.
usage: python3 BUSCO2faa.py
date: 2022-03-14
author: Axel Lindström'''


from collections import defaultdict

# Path to file with all common BUSCO ids (one per line)
BUSCOs_in_all_species = './6_Busco/BUSCOs_in_alla_species.txt'

# Short name of all species to include (name of result folder)
species = ('Ht','Pb','Pc','Pf','Pk','Pv','Py','Tg')

# Empty dictionary to store gene ids for each species in
genes = defaultdict(list)

# Open list of common species
with open(BUSCOs_in_all_species, 'r') as BUSCO_ids:
    # Read in all line in file
    ids = BUSCO_ids.readlines()
    
    # Remove new line character (unnecessary??)
    ids = [id.replace('\n', '') for id in ids]
    
    # For each species (key) in the set of species creat a key in the gene dictionary
    for spec in species:
        genes[spec] = []
        
        # For every common BUSCO id open path to "initial_run_results" in busco output folder of each species
        for id in ids:
            # Example path: Ht/run_apicomplexa_odb10/hmmer_output/initial_run_results/{1234at1234.out
            # This path should be from the workingdirectory to 
            # the result folder of busco and down to each *.out file 
            with open(f'./6_Busco/{spec}/run_apicomplexa_odb10/hmmer_output/initial_run_results/{id}.out') as gene_key:
                # Append gene id for each busco id for each species
                genes[spec].append(gene_key.readlines()[3].split()[0])
                

# For gene print sequence from each species to a new file
for key, item in genes.items():
    # Get index of gene 
    for gene_num in range(len(item)):
        # Open faa file for each genome, extract correct gene and write to output file
        # A folder called "output" must be in the working directory. All output files will be saved here
        with open(f'./5_gff_fasta/FAA/{key}.faa') as seq, open(f'./output/{ids[gene_num]}.faa', 'a') as out_faa:
            for line in seq:
                if line.startswith(f">{item[gene_num]}"):
                    line = line.rstrip()
                    seq_line = seq.readline()
                    # Header should be ">Ht"
                    out_faa.write(f'>{key}\n{seq_line}')
