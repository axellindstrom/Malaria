All genome data was retieved from the server.
# Processing of Haemoproteus tartakovskyi data
## Filter out bird scaffolds
To filter out the bird scaffold the script **scaffold.py** was used.
The maximum GC content was set to 33 % since this allowed for filtering out most of the bird scaffolds while keeping a lot of the tartakovskyi scaffolds. Sequences shorter than 3000 bp were discarded.

The **scaffold.py** script takes an input file with sequence data in FASTA format, filter out sequences with a lenght less than the specifed lenght and a GC content less than the specifed GC content and returns a file in FASTA format with the remaining sequences.

    Example usage: python3 scaffold.py -i Haemoproteus_tartakovskyi.raw.genome -o H_t33_scaffold.fasta -l 3000 -g 33

    -i      --input     name of input file.
    -o      --output    name of output file (default is set to output.fasta).
    -l      --lenght    Minimum length of sequences to keep (default is set to 3000 bp).
    -g      --GCcontent Maximum GC content of the sequences to be kept (default is set to 50%).

## Gene prediction of *H.tartakovskyi*
For the gene prediction of *H.tartakovskyi* **GeneMark** was used. The minimum contig lenght was set to 3000 bp instead of the default 5000.

    gmes_petap.pl --ES --min_contig 3000 --sequence H_t33_scaffold.fasta

## Convert gff and genome file to fasta sequence
To convert the gff and genome file to fasta files the gffParse.pl was used. The parser take the filtered genome file as an input and the gtf file with gene prediction. -p was added as a flag to output an amino acid fasta file and -c specify that the reading fram should be shifted if internal stop codons are found.
    
    gffParse.pl -i ./H_t33_scaffold.fasta -g genemark.gtf -p -c

## Classify origin of genes
In order to find genes that belong to the host and is not of intresst the nucloteide file from the previus step was used to do a blastx seach against SwissProt.

    blastx -query gffParse.fna -out blastx_output -db SwissProt -num_threads 10

## Parse queries with non avian origin
To exclude all queries with a top match of avian origin the output from the blastx search was matched against taxonomy information information from uniprot.

    example usage: python3 Scripts/datPars.py -b 3_Blastx/blastx_output -o 4_filter_out_host/Ht_genome.fasta -u 3_Blastx/uniprot_sprot.dat -f 2_filtered/Unfiltered/Ht.fna

    -b      --blast_file    Blast file containing matches from a blast search.
    -o      --output        Name of output file.
    -u      --uniprot       File containing information about gene ID and origin.
    -f      --fasta_file    Fasta file with contigs to sort.


## Gene predictiopn of **H.tartakovskyi**
A new gene prediction was performed with the filtered geneome of H.Tartakovskyi. 

    gmes_petap.pl --ES --min_contig 3000 --sequence Ht_filtered.fasta


## Calculating geneome size, number of genes and GC content

### Genome size
For calculating the genome size of each species the following bash command was used.

    for file in *.genome; do echo $file; cat $file | grep -v ">" | tr -d '\n' | wc -c; done

### GC content
For calculating the GC content for the **plasmodium** species and **toxoplasma** the following bash command was used.

    for file in *.genome; do GC=$(cat $file | grep -v ">" | grep -o [CGcg] | wc -c); All=$(cat $file | grep -v ">" | grep -o [aAtTcCgG] | wc -c); echo $file; echo "scale=2;$GC/$All*100" | bc -l; done

### Number of genes

#### gtf files
To calculate the number of genes for the **plasmodium** species the following bash command was used.    

    for file in *.gtf; do echo $file; cat $file | cut -f3 | grep -w gene | wc -l; done

#### gff file 
To calculate the number of genes for the **toxoplasma** the following bash command was used.

    cat Tg.gff | grep -w -c "start_codon"

#### Tartakovskyi
To calculate the number of genes 

    cat 4_filter_out_host/Ht_filtered.fasta | grep ">" | tr -d ">" | tr -d "\n" | cut -f1 | wc -l

#### Results
| | Species |  Host  |  Genome size  |  Genes  |  Genomic GC (%)|
|-|---------|--------|---------------|---------|----------------|
|1|Plasmodium berghei|rodents|17954629|7235|23.71|
|2|	Plasmodium cynomolgi    | macaques  | 26181343  |5787   |40.37|
|3|	Plasmodium falciparum   | humans  | 23270305   | 5207    | 19.36|
|4|	Plasmodium knowlesi | lemures   | 23462346  | 4953  | 38.83|
|5|	Plasmodium vivax    | humans   | 27007701    | 5682    | 42.27|
|6|	Plasmodium yoelii   | rodents   | 22222369  | 4919  | 21.77|
|7|	Haemoproteus tartakovskyi   | birds   | 8607918 | 2431    | 28.65|
|8|	Toxoplasma gondii | humans | 128105889  | 15564 | 52.35|


## gffParse gff and geneome files
For all genes in each genome fasta files containing nucleotide and amino acid sequences were created using gffParse.pl.

    gffParse.pl -i Toxoplasma_gondii.genome -g Tg.gff -b Tg -c -p

## Installing proteinortho
Proteinortho v6.0.33 was installed by:

    conda install -c conda-forge proteinortho=6.0.33 --yes


## Identify orthologs with proteinortho
To identify orthologs in the species proteinortho was used by running the following command:

    nohup proteinortho6.pl {Ht,Pb,Pc,Pf,Pk,Pv,Py,Tg}.faa &

Output is a binary file.


## Busco
busco v5.4.4 was installed

    conda install -c conda-forge -c bioconda busco=5.4.4

A busco analysis was performed with the faa file from all species by running the command:

    for file in ../5_gff_fasta/FAA/*.faa; do short=$(echo $file | cut -d "/" -f4 | cut -d "." -f1); busco -i $file -o $short -m prot -l apicomplexa; done

To get information of complete, missing and fragmented buscos for each species:

    for file in [HPT]*; do echo $file; cat $file/run_apicomplexa_odb10/full_table.tsv | grep -v "#" | cut -f2 | sort | uniq -c; totaldup=$(cat $file/run_apicomplexa_odb10/full_table.tsv | grep -w Duplicated | cut -f1 | sort | uniq -c | wc -l); echo $totaldup 'number of total dublicated BUSCOs'; done

### Results
Busco did run for all except Toxoplasma.

|Species|Complete|Duplicated|Fragmented|Missing|
|-------|--------|----------|----------|-------|
|Ht|279|0|14|153|
|Pb|353|10|50|33|
|Pc|435|1|1|9|
|Pk|322|1|3|120|
|Pv|435|2|0|9|
|Py|433|1|3|9|
|Tg|4|762|24|38|

To get all completed and duplicated genes:

    for file in [HPT]*; do cat $file/run_apicomplexa_odb10/full_table.tsv | grep -v "#" | grep -v -w Fragmented | grep -v -w Missing | cut -f1 | sort | uniq >> all_BUSCOs.txt; done

To get all BUSCOs that are present in all species:

    cat all_BUSCOs.txt | sort | uniq -c | grep -w 7 | cut -d " " -f8

To get the number:

    cat all_BUSCOs.txt | sort | uniq -c | grep -w 7 | cut -d " " -f8 | wc -l

181 BUSCOs are present in all the species (Toxoplasma excluded).


## Compile all ortholog genes found in all species
BUSCO2faa.py was used.


## Alignment
clustalo was used to align the 181 common amino acid sequences.

    for file in ../6_Busco/output/*; do id=$(echo ${file} | cut -d '/' -f4 | tr -d '.faa'); echo $id; clustalo -i $file -o ${id}_aligned.faa -v; done

## Trees
12345 was set as a seed. 

    for file in ../7_Alignment/*; do id=$(echo $file | cut -d "/" -f3 | cut -d _ -f1); raxmlHPC -s $file -n ${id}.tre -o Tg -m PROTGAMMABLOSUM62 -p 12345; done

All result files were concatinated:

    for file in ./*result*; do cat $file >> res.tre; done

All parsimony files were concatinated:

    for file in ./*parsi*; do cat $file >> pars.tre; done

All bestTree files were concatinated:

    for file in ./*bestT*; do cat $file >> best.tre; done


the res.tre best.tre and pars.tre file was then used in *phylip consense*, Tg was set as an outgroup and 2 trees from each file was produced. One unrooted tree and one rooted tree. 