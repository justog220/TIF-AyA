# Predicción de genes con Glimmer

En primer lugar decidimos utilizar Glimmer (Delcher, 2006) para el primer caso, debido a que tenemos un genoma de referencia que nos permite entrenar los modelos ocultos de markov (HMM) que implementa este software. Por otro lado, lo elegimos también por la capacidad de ejecutarlo localmente y pudiendo ajustar los diferentes parámetros de él.

Como dijimos esta herramienta realiza la producción a través de HMM. Lógicamente, debemos entrenar estos modelos para luego predecir los orfs de nuestra secuencia ensamblada. Con este fin descargamos la secuencia en formato FASTA del genoma de referencia previamente referenciado (GCF_000007505.1).
A partir del genoma procedemos a realizar los pasos para extraer el set de entrenamiento utilizando las herramientas contenidas en el paquete.

```bash
tigr-glimmer long-orfs -n -t 1.15 suis.fna bsuis.longorfs
```

Con este comando, obtuvimos los diferentes orfs con información de su inicio, fin, hebra y marco de lectura. A partir de esta tabla buscamos la secuencia de los orfs en el genoma de referencia con el siguiente comando:

```bash
tigr-glimmer extract -t suis.fna bsuis.longorfs > bsuis.train
```

Dicho comando extrae las secuencias de los ORFs a partir del genoma completo en suis.fna y las guarda en un archivo FASTA llamado bsuis.train. 
Teniendo ya el set de entrenamiento tal como lo necesita Glimmer, podemos pasar a construir el HMM.

```bash
tigr-glimmer build-icm -r bsuis.icm < bsuis.train
```

Finalizada la ejecución del comando anterior tenemos en el archivo bsuis.icm el modelo oculto de Markov ya entrenado y listo para usar en la predicción de ORFs de nuestro ensamblado híbrido. Para ello, ejecutamos el siguiente comando:

```bash
tigr-glimmer glimmer3 -o50 -g110 -t30 contigs.fasta bsuis.icm bsuis
```

Parámetros:
- -o: Establece la longitud máxima de superposición en n. Se permiten superposiciones de esta cantidad o menos de bases entre genes. 
- -g: Establece la longitud mínima del gen en n nucleótidos. 
- -t: establece el puntaje umbral en el score del algoritmo para que sea considerado un potencial gen (el puntaje de las regiones tienen que ser igual o mayor que el umbral). Este puntaje es el de la columna etiquetada como “InFrm” en el archivo .detail, no el puntaje decimal en la columna etiquetada como “Raw”. 

Los archivos finales obtenidos para la predicción son los siguientes:
- `bsuis.predict` → Coordenadas de los genes predichos. 
- `bsuis.detail` → Parámetros y resultados detallados. 

Luego de la predicción podemos observar que se creó la carpeta bsuis tal como lo solicitamos en el comando, donde podemos encontrar diferente información sobre los orfs predichos. Por ejemplo, en bsuis.predict podemos encontrar información sobre los ids de los 27 ORF predichos, su inicio, fin, hebra, marco de lectura y el score de la predicción.
