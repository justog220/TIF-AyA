# Ensamblado híbrido: SPAdes

Para el ensamblado híbrido, utilizamos el programa SPAdes, el cual ejecutamos con el siguiente comando:

```bash
spades.py --s1 Set3.fq --trusted-contigs contig.fasta --careful -o spades
```

Como usamos el el resultado del ensamblado por Sanger, le indicamos al programa la opción `—trusted-contigs contig.fasta` y, como el tipo de biblioteca que se usó para Illumina es single pair no unpaired y de la hebra R1 indicamos esto con `—s1` para poder pasarle correctamente los archivos de entrada con las reads. 
