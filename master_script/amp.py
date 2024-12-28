import sys

# Function to parse AMP data from a file
def parse_amp_data(file_path):
    amp_data = []
    amparc_data = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            # Skip lines that do not start with "AMP"
            if not line.startswith("AMP"):
                continue

            try:
                fields_list = line.strip().split('\t')

                # Ensure the line has enough fields
                if len(fields_list) < 4:
                    print(f"Line {line_num} skipped: Not enough fields")
                    continue

                # Extract chr name and noc
                chr_name = fields_list[3]
                noc = int(fields_list[6]) 

                # Extract relevant fields using regular expressions
                fields = dict(item.split('=') for item in line.strip().split('\t') if '=' in item)

                start = fields.get("position_start", "")
                end = fields.get("position_end", "")
                name = fields.get("gene_name", "")
                genep = fields.get("gene_product", "")
                codon_ref_seq = fields.get("codon_ref_seq", "")
                codon_new_seq = fields.get("codon_new_seq", "")
                mutation_category = fields.get("mutation_category", "")

                # Calculate length
                if start.isdigit() and end.isdigit():
                    length = int(end) - int(start)
                else:
                    print(f"Line {line_num} skipped: Invalid start/end positions")
                    continue

                # Notes
                additional_notes = mutation_category.split('_', 1)[-1] if '_' in mutation_category else ""
                notes = f'{additional_notes}, {codon_ref_seq}->{codon_new_seq}'.strip(", ")

                # Build the AMP entry
                amp_entry = {
                    "chr": chr_name,
                    "start": start,
                    "end": end,
                    "name": name,
                    "genep": genep,
                    "type": "AMP",
                    "noc": noc,
                    "notes": notes
                }

                # Categorize data based on length
                if length <= 5000:
                    amp_data.append(amp_entry)
                else:
                    amparc_data.append(amp_entry)

            except Exception as e:
                print(f"Error parsing line {line_num}: {line.strip()}")
                print(f"Error details: {e}")
    return amp_data, amparc_data

# Function to format data into the SCATTER01 structure
def format_scatter01(amp_data):
    scatter_template = """
    
var SCATTER03 = [ "SCATTER03" , {{
  SCATTERRadius: 300,
  innerCircleSize: 1,
  outerCircleSize: 3,
  innerCircleColor: "blue",
  outerCircleColor: "#0000FF",
  innerPointType: "rect", //circle,rect
  outerPointType: "circle", //circle,rect
  innerrectWidth: 2,
  innerrectHeight: 2,
  outerrectWidth: 10,
  outerrectHeight: 10,
  outerCircleOpacity: 1,
  random_data: 0,

}} ,[
{}
]
];
"""
    scatter_items = [
        f'  {{chr: "{data["chr"]}", start: "{data["start"]}", end:"{data["end"]}", '
        f'name: "{data["name"]}", genep: "{data["genep"]}", '
        f'noc: "{data["noc"]}", type: "AMP", notes: "{data["notes"]}"}}'
        for data in amp_data
    ]
    return scatter_template.format(",\n".join(scatter_items))

# Function to format data into the ARC02 structure
def format_amparc02(amparc_data):
    amparc_template = """
var ARC02 = [ "ARC02" , {{
  innerRadius: 294,
  outerRadius: 307,
}} , [
{}
]];
"""
    amparc_items = [
        f'  {{chr: "{data["chr"]}", start: "{data["start"]}", end:"{data["end"]}", '
        f'name: "{data["name"]}", genep: "{data["genep"]}", '
        f'noc: "{data["noc"]}", type: "AMP", notes: "{data["notes"]}" , color: "rgb(0, 255, 0)"}}'
        for data in amparc_data
    ]
    return amparc_template.format(",\n".join(amparc_items))

# Main execution
if __name__ == "__main__":
    # Check if the input file argument was provided
    if len(sys.argv) < 2:
        print("Usage: python script1.py <input_file>")
        sys.exit(1)
 # Get the input file from the command-line argument
    input_file = sys.argv[1]

    # Parse the data using the input file
    amp_data , amparc_data = parse_amp_data(input_file)
    # Process SCATTER01 data
    if amp_data:
        scatter01_output = format_scatter01(amp_data)
    else:
        scatter01_output = """
var SCATTER03= [ "SCATTER03" , {
  SCATTERRadius: 300,
  innerCircleSize: 1,
  outerCircleSize: 3,
  innerCircleColor: "red",
  outerCircleColor: "#CC3399"
  innerPointType: "circle", //circle,rect
  outerPointType: "circle", //circle,rect
  innerrectWidth: 2,
  innerrectHeight: 2,
  outerrectWidth: 10,
  outerrectHeight: 10,
  outerCircleOpacity: 1,
  random_data: 0,
} ,[
]
];
"""
    with open("amp.js", "w") as scatter_file:
        scatter_file.write(scatter01_output)
    print(f"SCATTER data saved to amp.js with {len(amp_data)} entries (length ≤ 5000).")

    # Process ARC02 data
    if amparc_data:
        amparc02_output = format_amparc02(amparc_data)
    else:
        amparc02_output = """

var ARC02 = [ "ARC02" , {
  innerRadius: 294,
  outerRadius: 307,
} , []];
"""
    with open("amparc.js", "w") as amparc_file:
        amparc_file.write(amparc02_output)
    print(f"ARC data saved to amparc.js with {len(amparc_data)} entries (length > 5000).")
