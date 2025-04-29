
# GenomeDiff-to-NGCircos Visualization Pipeline

**📈 Interactive Visualization of Breseq Mutation Predictions with NG-Circos.js**

This repository provides a streamlined, end-to-end pipeline for converting mutation predictions from Breseq’s `.gd` (GenomeDiff) files into rich, interactive circular genome visualizations using **[NG-Circos.js](https://github.com/dugongjs/NG-Circos)** (modified).

It bridges mutation annotation parsing, reference genome interpretation, and D3.js-powered visual rendering into a single, easy-to-use framework.


## Prerequisites

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or Anaconda
- Python = 3.11
- Breseq `annotated.gd` or `output.gd` 
- Reference genome in `.gbk/.gff3/.fa` format (it should be of the same strain as in `annotated.gd` or `output.gd` )

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/PadmanabhanKann/genome_visualisation
cd genome_visualisation/master_script
```

### 2. Set Up Conda Environment

```bash
conda env create -f environment.yml -n gd-viz
conda activate gd-viz
```


## Workflow Execution

### Step 1: Process Breseq Output

```bash
python master.py \
  --ref reference.gbk \
  --out output.gd \
  --ann breseq_output/output.gd
```

**Arguments**:

- `--ref`: Path to the reference genome in GenBank format
- `--out`: `output.gd` (generates`annotated.gd` if not provided)
- `--ann`: Path to the annotated `.gd` file (Breseq output)

📎 To view all arguments, run:

```bash
python master.py -h
```

---

## Visualization Output

Once the script completes, open `Genome.html` in your browser to interactively explore the visualized genome.

---

## Example Output

The `example/` folder includes:

- Sample `.gd` and `.gbk` input files
- Pre-generated JSON outputs
- A demo HTML (`Genome.html`) showing how the circular genome visualization should look

This is a great starting point to understand the expected output and customize your own plots.

---

## Repository Structure

```
genome_visualisation/
├── master_script/
│   ├── amp.py
│   ├── del.py
│   ├── html.py
│   ├── ins.py
│   ├── inv.py
│   ├── master.py
│   ├── mob.py
│   ├── snp.py
│   ├── lib/
│   │   ├── NGCircos_.js
│   │   ├── d3.js
│   │   ├── jquery.js
│   │   └── saveSvgAsPng.js
│   └── css/
│       ├── bootstrap.min.css
│       ├── font-awesome.min.css
│       └── sb-admin-2.css
├── example/
│   ├── REL606.gbk (sample reference file)
│   ├── REL606.gff3(sample reference file)
│   ├── annotated.gd(sample annotated.gd)
│   └── genome.html
├── environment.yml
└── requirements.txt

```

---

