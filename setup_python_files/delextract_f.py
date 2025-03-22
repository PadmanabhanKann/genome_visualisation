import re

# Function to parse DEL data from a file
def parse_del_data(file_path):
    del_data = []
    delarc_data = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            if not line.startswith("DEL"):
                continue

            try:
                fields_list = line.strip().split('\t')

                if len(fields_list) < 4:
                    print(f"Line {line_num} skipped: Not enough fields")
                    continue

                chr_name = fields_list[3]
                fields = dict(item.split('=') for item in line.strip().split('\t') if '=' in item)

                start = fields.get("position_start", "")
                end = fields.get("position_end", "")
                name = fields.get("gene_name", "")
                codon_ref_seq = fields.get("codon_ref_seq", "")
                codon_new_seq = fields.get("codon_new_seq", "")
                mutation_category = fields.get("mutation_category", "")
                genep = fields.get("gene_product", "")
                gene_count = len(genep.split(',')) if genep else 0
                genep = gene_count if gene_count > 5 else genep

                if start.isdigit() and end.isdigit():
                    length = int(end) - int(start)
                else:
                    print(f"Line {line_num} skipped: Invalid start/end positions")
                    continue

                additional_notes = mutation_category.split('_', 1)[-1] if '_' in mutation_category else ""
                notes = f'{additional_notes}, {codon_ref_seq}->{codon_new_seq}'.strip(", ")

                del_entry = {
                    "chr": chr_name,
                    "start": start,
                    "end": end,
                    "name": name,
                    "genep": genep,
                    "type": "DEL",
                    "notes": notes,
                    "length": length
                }

                if length <= 5000:
                    del_data.append(del_entry)
                else:
                    delarc_data.append(del_entry)

            except Exception as e:
                print(f"Error parsing line {line_num}: {line.strip()}")
                print(f"Error details: {e}")
    return del_data, delarc_data

# Function to format SCATTER01 data
def format_scatter01(del_data):
    scatter_template = """
var SCATTER02 = [ "SCATTER02" , {{
  SCATTERRadius: 300,
  innerCircleSize: 1,
  outerCircleSize: 3,
  innerCircleColor: "black",
  outerCircleColor: "black",
  innerPointType: "circle",
  outerPointType: "circle",
  innerrectWidth: 2,
  innerrectHeight: 2,
  outerrectWidth: 10,
  outerrectHeight: 10,
  outerCircleOpacity: 1,
  random_data: 0,
}} , [
{}
]];
"""
    scatter_items = [
        f'  {{chr: "{data["chr"]}", start: "{data["start"]}", end: "{data["end"]}", '
        f'name: "{data["name"]}", genep: "{data["genep"]}", '
        f'change: "{data["length"]}", type: "{data["type"]}", notes: "{data["notes"]}"}}'
        for data in del_data
    ]
    return scatter_template.format(",\n".join(scatter_items))

# Function to format ARC02 data
def format_delarc02(delarc_data):
    delarc_template = """
var ARC01 = [ "ARC01" , {{
  innerRadius: 294,
  outerRadius: 307,
}} , [
{}
]];
"""
    delarc_items = [
        f'  {{chr: "{data["chr"]}", start: "{data["start"]}", end: "{data["end"]}", '
        f'name: "{data["name"]}", genep: "{data["genep"]}", '
        f'change: "{data["length"]}", type: "DEL", notes: "{data["notes"]}", color: "rgb(128, 128, 128)"}}'
        for data in delarc_data
    ]
    return delarc_template.format(",\n".join(delarc_items))

# Main execution
if __name__ == "__main__":
    input_file = "/home/padma/Downloads/an.gd"  # Replace with your input file path
    del_data, delarc_data = parse_del_data(input_file)

    # Process SCATTER01 data
    #the {} are different
    scatter01_output = format_scatter01(del_data) if del_data else """
var SCATTER02 = [ "SCATTER02" , {
  SCATTERRadius: 300,
  innerCircleSize: 1,
  outerCircleSize: 3,
  innerCircleColor: "black",
  outerCircleColor: "black",
  innerPointType: "circle",
  outerPointType: "circle",
  innerrectWidth: 2,
  innerrectHeight: 2,
  outerrectWidth: 10,
  outerrectHeight: 10,
  outerCircleOpacity: 1,
  random_data: 0,
} , [
]];
"""
    with open("del.js", "w") as scatter_file:
        scatter_file.write(scatter01_output)
    print(f"SCATTER01 data saved to del.js with {len(del_data)} entries (length ≤ 5000).")

    # Process ARC02 data
    delarc02_output = format_delarc02(delarc_data) if delarc_data else """
var ARC01 = [ "ARC01" , {
  innerRadius: 294,
  outerRadius: 307,
} , [
]];
"""
    with open("delarc.js", "w") as delarc_file:
        delarc_file.write(delarc02_output)
    print(f"ARC02 data saved to delarc.js with {len(delarc_data)} entries (length > 5000).")
