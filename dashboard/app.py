import sqlite3
import os
from flask import Flask, render_template

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "ptaci.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def dashboard():
    conn = get_db()
    ptaci = conn.execute("SELECT * FROM ptaci ORDER BY nazev ASC").fetchall()
    conn.close()
    return render_template("dashboard.html", ptaci=ptaci)

if __name__ == "__main__":
    app.run(debug=True)