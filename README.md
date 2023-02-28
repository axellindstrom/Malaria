All genome data was retieved from the server.

# Filter out bird scaffolds
To filter out the bird scaffold the script **scaffold.py** was used.
The maximum GC content was set to 33 % since this allowed for filtering out most of the bird scaffolds while keeping a lot of the tartakovskyi scaffolds. Sequences shorter than 3000 bp were discarded.

The **scaffold.py** script takes an input file with sequence data in FASTA format, filter out sequences with a lenght less than the specifed lenght and a GC content less than the specifed GC content and returns a file in FASTA format with the remaining sequences.

    Example usage: python3 scaffold.py -i Haemoproteus_tartakovskyi.raw.genome -o H_tartakovskyi.fasta -l 3000 -g 33

    -i      --input     name of input file.
    -o      --output    name of output file (default is set to output.fasta).
    -l      --lenght    Minimum length of sequences to keep (default is set to 3000 bp).
    -g      --GCcontent Maximum GC content of the sequences to be kept (default is set to 50%).

# Gene prediction of *H.tartakovskyi*
For the gene prediction of *H.tartakovskyi* **GeneMark** was used. The minimum contig lenght was set to 3000 bp instead of the default 5000.

    gmes_petap.pl --ES --min_contig 3000 --sequence H_t33_scaffold.fasta

# Convert gff and genome file to fasta sequence
To convert the gff and genome file to fasta files the gffParse.pl was used. The parser take the filtered genome file as an input and the gtf file with gene prediction. -p was added as a flag to output an amino acid fasta file and -c specify that the reading fram should be shifted if internal stop codons are found.
    
    gffParse.pl -i ./H_t33_scaffold.fasta -g genemark.gtf -p -c

# Classify origin of genes
In order to find genes that belong to the host and is not of intresst the nucloteide file from the previus step was used to do a blastx seach against SwissProt.

    blastx -query gffParse.fna -out blastx_output -db SwissProt -num_threads 10

# Parse queries with non avian origin
To exclude all queries with a top match of avian origin the output from the blastx search was matched against taxonomy information information from uniprot.

    example usage: python3 datPars.py -b blastx_output -o blast_pars.fasta -u uniprot_sprot.dat -f gffParse.fna

    -b      --blast_file    Blast file containing matches from a blast search.
    -o      --output        Name of output file.
    -u      --uniprot       File containing information about gene ID and origin.
    -f      --fasta_file    Fasta file with contigs to sort.



