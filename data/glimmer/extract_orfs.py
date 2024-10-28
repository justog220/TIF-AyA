from Bio import SeqIO

def extraer_orfs_fasta(fasta_file, orfs_file, output_fasta_pos, output_fasta_neg):
    genome_seq = None
    for record in SeqIO.parse(fasta_file, "fasta"):
        genome_seq = record.seq

    if genome_seq is None:
        raise ValueError("No se pudo cargar la secuencia del genoma.")

    with open(orfs_file, 'r') as infile, \
            open(output_fasta_pos, 'w') as outfile_pos, \
            open(output_fasta_neg, 'w') as outfile_neg:

        for line in infile:
            if line.strip() == "":
                continue

            columns = line.split()

            if len(columns) != 5:
                print(f"Línea malformada: {line.strip()}")
                continue

            try:
                orf_id = columns[0]
                start = int(columns[1])
                end = int(columns[2])
                frame = columns[3]
                score = float(columns[4])

                if frame.startswith('+'):
                    orf_seq = genome_seq[start-1:end]
                    #Con .translate(to_stop=True) se pueden traducir las secuencias
                    outfile_pos.write(f">{orf_id} {frame} {start}-{end} Score:{score}\n")
                    outfile_pos.write(str(orf_seq) + "\n")

                elif frame.startswith('-'):
                    orf_seq = genome_seq[end-1:start].reverse_complement()
                    outfile_neg.write(f">{orf_id} {frame} {start}-{end} Score:{score}\n")
                    outfile_neg.write(str(orf_seq) + "\n")

            except Exception as e:
                print(f"Error procesando la línea: {line.strip()}. Error: {e}")


# Archivos de entrada y salida

fasta_file = '../contigs.fasta'
orfs_file = './bsuis.predict'
output_fasta_pos = 'orfs_positivos.fasta'
output_fasta_neg = 'orfs_negativos.fasta'

extraer_orfs_fasta(fasta_file, orfs_file, output_fasta_pos, output_fasta_neg)
