
# Function to parse SNP data from a file
def parse_snp_data(file_path):
    snp_data = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            # Skip lines that do not start with "SNP"
            if not line.startswith("SNP"):
                continue

            try:
                fields_list = line.strip().split('\t')

                # Ensure the line has enough fields
                if len(fields_list) < 4:
                    print(f"Line {line_num} skipped: Not enough fields")
                    continue

                # Extract chr name from the 4th entry
                chr_name = fields_list[3] 
                change = fields_list[5]
                # Extract relevant fields using regular expressions
                fields = dict(item.split('=') for item in line.strip().split('\t') if '=' in item)
                
                # Ensure the mutation category starts with "snp" to process SNPs
                mutation_category = fields.get("mutation_category", "")
                if mutation_category:
                    # Extract relevant fields
                    start = fields.get("position_start", "")
                    end = fields.get("position_end", "")
                    name = fields.get("gene_name", "")
                    genep = fields.get("gene_product", "")
                    noc = ""  # Placeholder for additional notes/comments
                    codon_ref_seq = fields.get("codon_ref_seq", "")
                    codon_new_seq = fields.get("codon_new_seq", "")

                    # Adjust mutation category and notes
                    mutation_type = "SNP"  # Only use "SNP" as the type
                    additional_notes = mutation_category.split('_', 1)[-1] if '_' in mutation_category else ""  # Extract details like "intergenic"
                    notes = f'{additional_notes}, {codon_ref_seq}->{codon_new_seq}'  # Include extracted notes and codon change

                    # Build the SNP data dictionary
                    snp_data.append({
                        "chr": chr_name,
                        "start": start,
                        "end": end,
                        "name": name,
                        "genep": genep,
                        "change": change,
                        "type": mutation_type,  # Fixed as "SNP"
                        "noc": noc,
                        "notes": notes
                    })

            except Exception as e:
                print(f"Error parsing line {line_num}: {line.strip()}")
                print(f"Error details: {e}")
    return snp_data

# Function to format data into the SCATTER01 structure
def format_scatter01(snp_data):
    scatter_template = """
var SCATTER01 = [ "SCATTER01" , {{
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
    scatter_items = []
    for data in snp_data:
        scatter_items.append(f'  {{chr: "{data["chr"]}", start: "{data["start"]}", end: "{data["start"]}", '
                             f'name: "{data["name"]}", genep: "{data["genep"]}", '
                             f'change: "{data["change"]}", type: "{data["type"]}", noc: "{data["noc"]}", notes: "{data["notes"]}"}}')

    return scatter_template.format(",\n".join(scatter_items))

# Main execution
if __name__ == "__main__":
    input_file = "/home/padma/summer/test/ng_cricos/gdtools_annotate/annotate.gd"  # Replace with your input file path
    snp_data = parse_snp_data(input_file)

    if snp_data:
        scatter01_output = format_scatter01(snp_data)

        # Save output to a file
        with open("snp.js", "w") as output_file:
            output_file.write(scatter01_output)

        print("SCATTER01 data saved to snp.js")
    else:
        print("No SNP data found in the input file.")
