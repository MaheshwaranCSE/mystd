from flask import Flask, render_template, request
import sqlite3
import pickle
import os

app = Flask(__name__)

DB_NAME = "students.db"
MODEL_PATH = "model.pkl"

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            student_id TEXT,
            assignment_id TEXT,
            marks INTEGER,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- SUBMIT ----------
@app.route("/submit", methods=["POST"])
def submit():
    student_id = request.form["student_id"]
    assignment_id = request.form["assignment_id"]
    marks = int(request.form["marks"])
    status = request.form["status"]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO submissions VALUES (?, ?, ?, ?)",
                   (student_id, assignment_id, marks, status))
    conn.commit()
    conn.close()

    return render_template("index.html")

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM submissions")
    rows = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", rows=rows)

# ---------- PREDICT ----------
@app.route("/predict", methods=["POST"])
def predict():
    attendance = float(request.form["attendance"])
    marks = float(request.form["marks"])

    if not os.path.exists(MODEL_PATH):
        return "Model not trained yet!"

    model = pickle.load(open(MODEL_PATH, "rb"))
    prediction = model.predict([[attendance, marks]])

    result = "At Risk of Dropout" if prediction[0] == 1 else "Safe"

    return f"<h3>Prediction Result: {result}</h3><a href='/'>Back</a>"

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
