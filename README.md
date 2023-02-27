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
