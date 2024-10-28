from Bio import Blast
from Bio import SeqIO
from io import StringIO
from tqdm import tqdm
import pandas as pd
import subprocess
import tempfile
import os
from datetime import datetime

Blast.email = os.getenv("BLAST_EMAIL")

def run_deeplocpro(fasta_record):

    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_fasta:
        SeqIO.write(fasta_record, temp_fasta, "fasta")
        temp_fasta = temp_fasta.name


    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = temp_dir

        cmd = f"deeplocpro -f {temp_fasta} -o {temp_dir}"
        subprocess.run(cmd,
                        capture_output=True,
                        text=False,
                        shell=True)

        temp_file = subprocess.check_output(f"ls -t {temp_dir} | head -n 1", shell=True).decode('utf-8').strip()
        with open(temp_dir + "/" + temp_file, "r") as oarchi:
            output = oarchi.read()

    return parse_deeplocpro(output)

def parse_deeplocpro(deeploc_outp):
    output_io = StringIO(deeploc_outp)

    df = pd.read_csv(output_io)

    return df[["ACC", "Localization"]]

def run_pfam_scan(fasta_record):

    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_fasta:
        SeqIO.write(fasta_record, temp_fasta, "fasta")
        temp_fasta_path = temp_fasta.name


        # Obtener la ruta del directorio donde está este script (anotacion.py)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    

    pfam_scan_path = os.path.join(script_dir, "pfam_scan", "pfam_scan.py")
    pfam_db_path = os.path.join(script_dir, "pfam_scan", "pfamdb")

    cmd = f"python {pfam_scan_path} {temp_fasta_path} {pfam_db_path}"
    result = subprocess.run(cmd,
                    capture_output=True,
                    text=True,
                    shell=True)

    output = result.stdout

    output_io = StringIO(output)

    df = pd.read_csv(output_io)

    columnas_interes = [
        "hmm_acc",
        "hmm_name",
        "type",
        "hmm_start",
        "hmm_end"
    ]

    rename_columnas_interes = [
        "pfam_acc",
        "pfam_name",
        "pfam_type",
        "pfam_start",
        "pfam_end"
    ]

    rename_dict = dict(zip(columnas_interes, rename_columnas_interes))

    df.rename(columns=rename_dict, inplace=True)

    columnas_interes = rename_columnas_interes
    del(rename_columnas_interes)

    return df[columnas_interes]

def current_time():
    return datetime.now().strftime("%H:%M:%S")

df = pd.DataFrame({
    "id": [],
    "funcion_prokka": [],
    "largo": pd.Series(dtype="int"),
    "pfam_acc": [],
    "pfam_name": [],
    "pfam_type": [],
    "pfam_start": pd.Series(dtype="int"),
    "pfam_end": pd.Series(dtype="int"),
#    "interpro_scan": [],
    "location": [],
})

dbs = ["nr", "swissprot", "refseq_protein"]

fasta_file = "../data/prokka/PROKKA_10252024/PROKKA_10252024.faa"

blast_output = "blast_output"
os.makedirs(blast_output, exist_ok=True)

records = list(SeqIO.parse(fasta_file, "fasta"))
bar_format = "{l_bar}{bar}| {n_fmt}/{total_fmt}"

with tqdm(records, desc="Procesando secuencias", bar_format=bar_format, dynamic_ncols=True) as pbar:
    for record in pbar:
        id = record.id
        pbar.set_description(f"Procesando {id}")
        tqdm.write(f"{current_time()} - Start processing {id}")
        
        nombre = record.description
        nombre = " ".join(nombre.split(sep=" ")[1:])

        largo = int(len(record.seq))

        ruta_salida_blast = f"{blast_output}/{record.id}.xml"

        if id + ".xml" not in os.listdir(blast_output):
            tqdm.write(f"{current_time()} - Start running Blast for {id}")
            result_stream = Blast.qblast("blastp", "nr", format(record, "fasta"), hitlist_size=10)
            tqdm.write(f"{current_time()} - End running Blast for {id}")

            with open(ruta_salida_blast, "wb") as out_stream:
                out_stream.write(result_stream.read())

            tqdm.write(f"{current_time()} - Write Blast results for {id} at {ruta_salida_blast}")

            result_stream.close()

        else:
            tqdm.write(f"{current_time()} - Blast results for {id} already available at {ruta_salida_blast}")


        tqdm.write(f"{current_time()} - Start running pfam scan for {id}")
        pfam_info = run_pfam_scan(record)
        tqdm.write(f"{current_time()} - End running pfam scan for {id}")

        tqdm.write(f"{current_time()} - Start running deeploc for {id}")
        location_info = run_deeplocpro(record)
        tqdm.write(f"{current_time()} - End running deeploc for {id}")

        new_row = {
            "id": id,
            "funcion_prokka": nombre,
            "largo": largo,
            "pfam_acc": pfam_info["pfam_acc"].iloc[0] if not pfam_info.empty else None,
            "pfam_name": pfam_info["pfam_name"].iloc[0] if not pfam_info.empty else None,
            "pfam_type": pfam_info["pfam_type"].iloc[0] if not pfam_info.empty else None,
            "pfam_start": pfam_info["pfam_start"].iloc[0] if not pfam_info.empty else None,
            "pfam_end": pfam_info["pfam_end"].iloc[0] if not pfam_info.empty else None,
#            "interpro_scan": None,  # Puedes añadir interpro_scan después
            "location": location_info["Localization"].iloc[0]
        }
        
        df = df._append(new_row, ignore_index=True)

        tqdm.write(f"{current_time()} - End processing {id}")


# print(df)

df.to_csv("output.tsv", sep="\t", index=False)
