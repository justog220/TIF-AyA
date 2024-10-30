import sys

def parse_fasta(input_file):
    output_file = input_file.replace(".", "_parseado.")

    print(output_file)
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            if line.startswith(">"):
                
                especie = line.split("[")[-1].split("]")[0]
                
                especie = especie.replace(" ", "_")

                line = line.split("[")[0]
                
                nuevo_header = f">{especie} {line[1:]}\n"
                outfile.write(nuevo_header)
            else:
                outfile.write(line)
    print(f"Archivo procesado guardado como: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <archivo_multifasta.fasta>")
    else:
        parse_fasta(sys.argv[1])
