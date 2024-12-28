import subprocess

# Path to the input file
input_file = "/home/padma/summer/test/ng_cricos/gdtools_annotate/annotate.gd"

# List of scripts to run
scripts = [
    "mob.py",
        "inv.py"
]

# Run each script with the input file as an argument
for script in scripts:
    print(f"Running {script} with input file {input_file}...")
    subprocess.run(["python", script, input_file])
