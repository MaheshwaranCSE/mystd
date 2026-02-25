import pandas as pd

df = pd.read_csv("student_dataset.csv")
df = df.dropna()
df.to_csv("cleaned_data.csv", index=False)

print("Data cleaned successfully!")
