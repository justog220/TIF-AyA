from Bio import Blast
import os
import re

with open("blast_parseado.txt", "w") as salida_larga:
	with open("blast_resume.txt", "w") as salida_resumen:
		blast_xml_files = [archivo for archivo in os.listdir("blast_output") if re.findall(r'PROKKA\w+.xml', archivo)]

		blast_xml_files.sort()
		for blast_xml_file in blast_xml_files:
			result_stream = open("blast_output/" + blast_xml_file, "rb")

			blast_record = Blast.read(result_stream)

			salida_resumen.write(blast_xml_file + "\n")
			salida_larga.write(blast_xml_file + "\n")
			salida_larga.write(str(blast_record) + "\n")



			for br in blast_record:
				desc = br.target.description.split(sep="]")[0] + ']'
				if "MULTISPECIES:" in desc:
					desc = " ".join(desc.split(sep=": ")[1:])

				for hsp in br:
					evalue = hsp.annotations['evalue']

				salida_resumen.write("\t|_" +desc + "\n")
				salida_resumen.write("\t|\t|_E-value: " + str(evalue)+ "\n")


			salida_resumen.write(">"*80 + "\n")
			salida_larga.write(">"*80 + "\n"t)
