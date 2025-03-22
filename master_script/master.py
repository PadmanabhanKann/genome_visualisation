import subprocess
import os
import argparse
from Bio import SeqIO
from BCBio import GFF


# Parse the arguments
parser = argparse.ArgumentParser(description="prepare the input file")
parser.add_argument("--out", type=str, help="path to output.gd file")
parser.add_argument("--ref", type=str, help="path to reference file")
parser.add_argument("--ann", type=str, help="path to annotated.gd file")
args = parser.parse_args()


output_gd=args.out
reference_gd=args.ref


if args.out:
   
    subprocess.run('gdtools annotate -o annotated.gd -r '+ reference_gd + ' ' + output_gd + ' -f GD', shell=True)
    input_file = 'annotated.gd'
elif args.ann:
    input_file = args.ann

def parse_genome_file(filename):
    ext = os.path.splitext(filename)[1].lower()  # Get file extension
    seq_id = None  # Placeholder for sequence ID

    if ext in [".gb", ".gbk", ".genbank"]:  # GenBank format
        record = SeqIO.read(filename, "genbank")
        seq_id = record.name  # Extract strain name (usually in LOCUS)

    elif ext in [".fa", ".fasta"]:  # FASTA format
        record = SeqIO.read(filename, "fasta")
        seq_id = record.id  # Extract sequence ID from header

    elif ext in [".gff", ".gff3"]:  # GFF3 format (needs special parsing)
        with open(filename) as gff_file:
            records = list(GFF.parse(gff_file))
            if not records or not records[0].seq:
                raise ValueError("No sequence data found in the GFF3 file!")
            record = records[0]  # Take the first sequence record
            seq_id = record.id  # Extract sequence ID

    return record, seq_id

def get_genome_length_and_id(filename):
    record, seq_id = parse_genome_file(filename)  # Unpack values
    return len(record.seq), seq_id

genome_length, seq_id = get_genome_length_and_id(reference_gd)
# List of scripts to run
scripts = [
    "html.py",
    "mob.py",
        "inv.py",
        "amp.py",
        "del.py",
        "snp.py",
        "ins.py",
]

# Run each script with the input file as an argument
for script in scripts:
    print(f"Running {script} with input file {input_file}, genome length {genome_length}, and sequence ID {seq_id}...")
    subprocess.run(["python", script, input_file, str(genome_length), seq_id])
