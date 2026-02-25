import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

df = pd.read_csv("cleaned_data.csv")

X = df[["attendance", "marks"]]
y = df["dropout"]

model = LogisticRegression()
model.fit(X, y)

pickle.dump(model, open("../app/model.pkl", "wb"))

print("Model trained and saved successfully!")
