# Predicción y anotación: Prokka

Como se mencionó anteriormente y como lo solicitaba la consigna, llevamos a cabo el proceso de predicción con dos herramientas, la ab initio descrita en la sección anterior y un pipeline integrador que además realiza la anotación de los orfs. 

Utilizamos el siguiente comando para ejecutar Prokka:

```bash
prokka contigs.fasta --evalue 1e-05 --rawproduct
```
