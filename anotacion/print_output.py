import pandas as pd

df = pd.read_csv("output.tsv", sep="\t")

print(df)

print(df.to_markdown())
