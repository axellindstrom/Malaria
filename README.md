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



# Calculating geneome size, number of genes and GC content

## Genome size
For calculating the genome size of each species the following bash command was used.

    for file in *.genome; do echo $file; cat $file | grep -v ">" | tr -d '\n' | wc -c; done

## GC content
For calculating the GC content for the **plasmodium** species and **toxoplasma** the following bash command was used.

    for file in *.genome; do GC=$(cat $file | grep -v ">" | grep -o [CGcg] | wc -c); All=$(cat $file | grep -v ">" | grep -o [aAtTcCgG] | wc -c); echo $file; echo "scale=2;$GC/$All*100" | bc -l; done

## Number of genes

### gtf files
To calculate the number of genes for the **plasmodium** species the following bash command was used.    

    for file in *.gtf; do echo $file; cat $file | cut -f3 | grep -w gene | wc -l; done

### gff file 
To calculate the number of genes for the **toxoplasma** the following bash command was used.

    cat Tg.gff | grep -w -c "start_codon"

### Tartakovskyi
To calculate the number of genes 

    cat 4_filter_out_host/blast_pars.fasta | grep ">" | tr -d ">" | tr -d "\n" | cut -f1 | wc -l

### Results
| | Species |  Host  |  Genome size  |  Genes  |  Genomic GC (%)|
|-|---------|--------|---------------|---------|----------------|
|1|Plasmodium berghei|rodents|17954629|7235|23.71|
|2|	Plasmodium cynomolgi    | macaques  | 26181343  |5787   |40.37|
|3|	Plasmodium falciparum   | humans  | 23270305   | 5207    | 19.36|
|4|	Plasmodium knowlesi | lemures   | 23462346  | 4953  | 38.83|
|5|	Plasmodium vivax    | humans   | 27007701    | 5682    | 42.27|
|6|	Plasmodium yoelii   | rodents   | 22222369  | 4919  | 21.77|
|7|	Haemoproteus tartakovskyi   | birds   | 8381238 | 3718    | 28.66|
|8|	Toxoplasma gondii | humans | 128105889  | 15564 | 52.35|