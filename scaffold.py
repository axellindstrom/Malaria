#!/usr/bin/env python3
'''
Usage: python3 scaffold.py -i [input file] -l [minimum sequence lenght] -g [maximum GC content] -o [output file]
'''
import argparse

parser = argparse.ArgumentParser(description= 'Filter out contigs of specified length and specified GC content.')
parser.add_argument('-i', '--input', type = str, metavar='',required=True, help='Input file')
parser.add_argument('-o', '--output', type = str, metavar='',required=False, help='Name of output file', default='output.fasta')
parser.add_argument('-l', '--length', type = int, metavar='',required=False, help='Minimum lenght of the scaffold', default=3000)
parser.add_argument('-g', '--GCcontent', type = int, metavar='',required=False, help='Maximum GC content', default=50)

args = parser.parse_args()


input_file = args.input
output_file = args.output


GC = args.GCcontent
length = args.length

with open(input_file, 'r') as in_file, open(output_file, 'w') as output:
    scaffold_id = {}
    seq = ''
    id = in_file.readline().rstrip().split(' ')[0]
    for line in in_file:
        if line.startswith('>'):
            scaffold_id[id] = seq
            GC_content = seq.count('C') + seq.count('G')
            AT_content = seq.count('A') + seq.count('T')
            
            if round(GC_content/(GC_content + AT_content)*100) > GC or len(scaffold_id[id]) <= length:
                del scaffold_id[id]
            
            try:
                if len(scaffold_id[id]) <= length:
                    del scaffold_id[id]
                else:
                    pass
            except:
                pass

            for key, item in scaffold_id.items():
                output.write(f'{key}\n')
                seq_row = [item[i:i + 60] for i in range(0, len(item), 60)]
                for row in seq_row:
                    output.write(f'{row}\n')

            scaffold_id = {}
            id = line.split(' ')[0]
            seq = ''
        else:
            seq += line.rstrip().upper()   

    scaffold_id[id] = seq
    if round(((seq.count('C') + seq.count('G'))/len(seq)*100)) < GC or len(scaffold_id[id]) <= length:
        del scaffold_id[id]

    else:
        for key, item in scaffold_id.items():
            output.write(f'{key}\n')
            seq_row = [item[i:i + 60] for i in range(0, len(item), 60)]
            for row in seq_row:
                output.write(f'{row}\n')
