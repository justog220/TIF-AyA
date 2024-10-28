# 🧬 Anotación de genes predichos

Este directorio contiene los scripts y resultados generados para la anotación de secuencias proteicas. El archivo principal, `anotacion.py`, coordina la ejecución de herramientas bioinformáticas y produce un archivo en formato TSV con las predicciones funcionales y de localización subcelular para cada proteína.

## 📜 Descripción de `anotacion.py`

Este script realiza un proceso de anotación automática para proteínas predichas, combinando tres herramientas principales:

1. **BLAST**: Realiza búsquedas remotas de secuencias contra la base de datos `nr` (proteínas no redundantes) y guarda los resultados en formato XML en la carpeta `blast_output`. Este proceso lo lleva a cabos a través de la librería `Bio.Blast.Applications` de Biopython.
2. **Pfam_scan**: Utiliza modelos de HMM para detectar dominios conservados en las proteínas contra la base de datos PFAM.
3. **DeepLocPro**: Predice la localización subcelular de las proteínas en células procariotas usando redes neuronales.

### 🚀 Funcionalidades Principales

1. **Ejecución de BLAST**  
   Para cada secuencia en el archivo FASTA, `anotacion.py` ejecuta una búsqueda BLAST y guarda los resultados en formato XML en `blast_output/`. Se limita a 10 hits por búsqueda para mejorar la eficiencia.

2. **Análisis con Pfam_scan**  
   Mediante HMMER y los perfiles de la base de datos PFAM, se identifican los dominios conservados de cada proteína. La salida contiene columnas como `pfam_acc` y `pfam_name`, que se almacenan en un DataFrame de pandas.

3. **Predicción de Localización Subcelular con DeepLocPro**  
   Esta herramienta predice las localizaciones subcelulares de cada proteína, utilizando un modelo de redes neuronales adaptado para procariotas.

### 🔍 Estructura de Salida

El script genera un archivo `output.tsv` que consolida los datos de cada herramienta. Las columnas principales incluyen:
- **ID** de la secuencia
- **Función Prokka**: Predicción inicial generada por Prokka
- **Pfam**: Información sobre dominios conservados, como `pfam_acc`, `pfam_name`, `pfam_start`, y `pfam_end`
- **Localización Subcelular**: Predicción realizada por DeepLocPro

### 📂 Archivos y Directorios

- **`blast_output/`**: Carpeta donde se almacenan los resultados de BLAST en formato XML.
- **`anotacion.py`**: Script principal para realizar anotaciones automáticas y guardar las salidas de BLAST, Pfam_scan, y DeepLocPro en un archivo consolidado.
- **`output.tsv`**: Archivo de salida con la anotación consolidada de cada proteína.

---

## ⚙️ Ejecución del Script

Deben estar instaladas las herramientas utilizadas, `HMMER` (para Pfam_scan) y `DeepLocPro`. 

### Requisitos Previos

El script asume que tienes configuradas las siguientes variables y herramientas:
- **Correo BLAST**: Configurado mediante la variable de entorno `BLAST_EMAIL`.
- **Python**: Instalación de los módulos `biopython`, `pandas`, `tqdm`.
- **Pfam_scan**: Ubicado en `pfam_scan/pfam_scan.py` dentro de este directorio.
- **DeepLocPro**: Preinstalado en el sistema y accesible en la línea de comandos.

### Ejemplo de Ejecución

```bash
python anotacion.py
```

Para parsear los xml de las búsquedas con BLAST se generó el script `parse_blast.py`

```bash
python parse_blast.py
```

## 🔗 Referencias y Créditos
- Jaimomar99. (2024). Jaimomar99/deeplocpro [Python]. https://github.com/Jaimomar99/deeplocpro (Obra original publicada en 2023)
- Moreno, J., Nielsen, H., Winther, O., & Teufel, F. (2024). Predicting the subcellular location of prokaryotic proteins with DeepLocPro. https://doi.org/10.1101/2024.01.04.574157
- Zielezinski, A. (2024). Aziele/pfam_scan [Python]. https://github.com/aziele/pfam_scan (Obra original publicada en 2022)