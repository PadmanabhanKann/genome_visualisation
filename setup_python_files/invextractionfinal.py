import re

# Function to parse INV data from a file
def parse_inv_data(file_path):
    inv_data = []
    invarc_data = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            # Skip lines that do not start with "INV"
            if not line.startswith("INV"):
                continue

            try:
                fields_list = line.strip().split('\t')

                # Ensure the line has enough fields
                if len(fields_list) < 4:
                    print(f"Line {line_num} skipped: Not enough fields")
                    continue

                # Extract chr name and noc
                chr_name = fields_list[3]

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

                # Build the INV entry
                inv_entry = {
                    "chr": chr_name,
                    "start": start,
                    "end": end,
                    "name": name,
                    "genep": genep,
                    "type": "INV",
                    "notes": notes,
                    "length":length
                }

                # Categorize data based on length
                if length <= 5000:
                    inv_data.append(inv_entry)
                else:
                    invarc_data.append(inv_entry)

            except Exception as e:
                print(f"Error parsing line {line_num}: {line.strip()}")
                print(f"Error details: {e}")
    return inv_data, invarc_data

# Function to format data into the SCATTER01 structure
def format_scatter01(inv_data):
    scatter_template = """
var SCATTER05 = [ "SCATTER05" , {{
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
        f'  {{chr: "{data["chr"]}", start: "{data["start"]}", end:"{data["end"]}",change:"{data["length"]}", '
        f'name: "{data["name"]}", genep: "{data["genep"]}",type: "INV", notes: "{data["notes"]}"}}'
        for data in inv_data
    ]
    return scatter_template.format(",\n".join(scatter_items))

# Function to format data into the ARC02 structure
def format_invarc02(invarc_data):
    invarc_template = """
var ARC03 = [ "ARC03" , {{
  innerRadius: 294,
  outerRadius: 307,
}} , [
{}
]];
"""
    invarc_items = [
        f'  {{chr: "{data["chr"]}", start: "{data["start"]}", end:"{data["end"]}", '
        f'name: "{data["name"]}", genep: "{data["genep"]}",type: "INV", notes: "{data["notes"]}",color: "rgb(128, 128, 128)"}}'
        for data in invarc_data
    ]
    return invarc_template.format(",\n".join(invarc_items))

# Main execution
if __name__ == "__main__":
    input_file = "/home/padma/summer/test/ng_cricos/gdtools_annotate/annotate.gd"  # Replace with your input file path
    inv_data, invarc_data = parse_inv_data(input_file)

    # Process SCATTER01 data
    if inv_data:
        scatter01_output = format_scatter01(inv_data)
    else:
        scatter01_output = """
var SCATTER05 = [ "SCATTER05" , {
  SCATTERRadius: 300,
  innerCircleSize: 1,
  outerCircleSize: 3,
  innerCircleColor: "black",
  outerCircleColor: "#CC3399",
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
    with open("inv.js", "w") as scatter_file:
        scatter_file.write(scatter01_output)
    print(f"SCATTER01 data saved to inv.js with {len(inv_data)} entries (length ≤ 5000).")

    # Process ARC02 data
    if invarc_data:
        invarc02_output = format_invarc02(invarc_data)
    else:
        invarc02_output = """

var ARC03 = [ "ARC03" , {
  innerRadius: 294,
  outerRadius: 307,
} , [
]];
"""
    with open("invarc.js", "w") as invarc_file:
        invarc_file.write(invarc02_output)
    print(f"ARC02 data saved to invarc.js with {len(invarc_data)} entries (length > 5000).")

