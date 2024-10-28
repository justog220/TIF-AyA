<div align="center">

# 🧬 Proyecto Final: Análisis y Alineamiento de Secuencias

## 🦠 Brote de Brucelosis en Entre Ríos, Argentina

## Garcia Justo, Valle Abril
</div>

Este proyecto es parte de un trabajo integrador donde aplicamos conceptos bioinformáticos avanzados para caracterizar la cepa *Brucella suis*, agente de un brote de brucelosis en Entre Ríos, Argentina. El objetivo es ensamblar, anotar, y analizar secuencias genómicas, así como diseñar un kit diagnóstico por PCR. 

## 🎯 Objetivos
- **Análisis de Calidad** de datos Sanger e Illumina.
- **Ensamblado de Secuencias** y generación de contigs y scaffolds.
- **Anotación** y **predicción** de genes.
- **Filogenia** para analizar la evolución de *B. suis*.
- **Diseño de Primers PCR** para diagnóstico del brote.

## 📂 Estructura de Directorios

```plaintext
.
├── anotacion/
│   ├── blast_output/               # Resultados de BLAST en archivos XML
│   ├── anotacion.py                # Script de anotación general
│   ├── Anotacion.zip               # Archivo comprimido con datos de anotación
│   ├── blast_parseado.txt          # Resultados de BLAST procesados
│   ├── blast_resume.txt            # Resumen de los resultados de BLAST
│   ├── output.tsv                  # Archivo TSV con resultados de anotación
│   ├── parse_blast.py              # Script para parsear resultados BLAST
│   ├── print_output.py             # Script para imprimir el output final
│   └── README.md                   # Instrucciones de la carpeta anotacion/
├── data/
│   ├── glimmer/                    # Datos de Glimmer para predicción de ORFs
│   ├── ncbi_dataset/               # Datos de NCBI para análisis comparativo
│   ├── prokka/                     # Anotación de genes y predicciones con Prokka
│   ├── set3/                       # Secuencias de consenso y bases de datos
│   └── spades/                     # Datos procesados de ensamblaje con SPAdes
└── disenio_primers/                # Script para el diseño de primers
```

## 🔧 Requisitos
Para ejecutar este proyecto necesitas las siguientes herramientas:

- Python 3.7+
- BLAST+
- Glimmer
- Prokka
- SPAdes

## 🚀 Etapas del Proyecto
1. Preprocesamiento de Secuencias
   - Sanger: Limpiar secuencias de baja calidad.
   - Illumina: Analizar calidad (sin procesamiento adicional).
2. Ensamblado de Secuencias
   - Ensamblar secuencias largas con Sanger y generar el contig de consenso en anotacion/.
   - Ejecutar un ensamblado híbrido con SPAdes, usando el contig de Sanger y lecturas cortas de Illumina.
3. Anotación y Predicción de Genes
    - Predicción ab initio con Glimmer.
    - Anotar genes con Prokka y visualizar el ensamblado anotado en un visor de genomas.
4. Análisis Filogenético
   - Realiza una búsqueda PSI-BLAST
   - Alineamiento múltiple con Clustal X 
   - Construcción de un árbol filogenético para explorar la relación evolutiva de B. suis.
5. Diseño de Primers para Diagnóstico PCR
    - Diseñar primers para todos los genes predichos con Perl.

## 📊 Resultados
Cada subdirectorio contiene los resultados específicos de cada análisis:

- `data/spades`: Contiene ensamblados de alta precisión y corrección de secuencias.
- `data/glimmer`: Archivos de predicción de ORFs.
- `data/prokka`: Archivos de anotación de genes y predicciones con Prokka.
- `anotacion/blast_output`: Archivos XML de resultados BLASTp para los genes predichos con Prokka.
- `disenio_primers`: Archivo de primers en formato fasta y tabla con temperaturas de melting y longitud de producto.

## 📈 Informe y Documentación
Una versión más académica y extendida de los procesos llevados a cabo puede visualizarse en [`Informe.pdf`](https://github.com/justog220/TIF-AyA/blob/main/Informe.pdf).

