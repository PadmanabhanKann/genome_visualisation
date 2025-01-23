import subprocess
import argparse
# Parse the arguments
parser = argparse.ArgumentParser(description="prepare the input file")
parser.add_argument("--out", type=str, help="path to output.gd file")
parser.add_argument("--ref", type=str, help="path to reference file")
parser.add_argument("--ann", type=str, help="path to annotated.gd file")
args = parser.parse_args()

if args.out and args.ref:
    output_gd=args.out
    reference_gd=args.ref
    subprocess.run('gdtools annotate -o annotated.gd -r '+ reference_gd + ' ' + output_gd + '-f GD', shell=True)
    input_file = 'annotated.gd'
elif args.ann:
    input_file = args.ann


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
    print(f"Running {script} with input file {input_file}...")
    subprocess.run(["python", script, input_file])
