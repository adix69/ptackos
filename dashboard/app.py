import sqlite3
import os
from flask import Flask, render_template, request

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "ptaci.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def build_query(params):
    conditions = []
    values = []

    if params.get("rad"):
        conditions.append("rad = ?")
        values.append(params["rad"])
    if params.get("typ_potravy"):
        conditions.append("typ_potravy = ?")
        values.append(params["typ_potravy"])
    if params.get("kontinent"):
        conditions.append("vyskyt_kontinent = ?")
        values.append(params["kontinent"])
    if params.get("migrace") in ("0", "1"):
        conditions.append("migrace = ?")
        values.append(int(params["migrace"]))
    if params.get("status"):
        conditions.append("status_ohrozeni = ?")
        values.append(params["status"])
    if params.get("hmotnost_min"):
        conditions.append("hmotnost_g >= ?")
        values.append(int(params["hmotnost_min"]))
    if params.get("hmotnost_max"):
        conditions.append("hmotnost_g <= ?")
        values.append(int(params["hmotnost_max"]))

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    return where, values

def get_filter_options(conn):
    def distinct(col):
        return [r[0] for r in conn.execute(f"SELECT DISTINCT {col} FROM ptaci WHERE {col} IS NOT NULL ORDER BY {col}").fetchall()]

    return {
        "rady":       distinct("rad"),
        "potravy":    distinct("typ_potravy"),
        "kontinenty": distinct("vyskyt_kontinent"),
        "statusy":    distinct("status_ohrozeni"),
    }

@app.route("/")
def dashboard():
    conn = get_db()
    params = {
        "rad":          request.args.get("rad", ""),
        "typ_potravy":  request.args.get("typ_potravy", ""),
        "kontinent":    request.args.get("kontinent", ""),
        "migrace":      request.args.get("migrace", ""),
        "status":       request.args.get("status", ""),
        "hmotnost_min": request.args.get("hmotnost_min", ""),
        "hmotnost_max": request.args.get("hmotnost_max", ""),
    }

    where, values = build_query(params)
    ptaci = conn.execute(f"SELECT * FROM ptaci {where} ORDER BY nazev ASC", values).fetchall()
    filter_options = get_filter_options(conn)
    conn.close()

    return render_template("templates/dashboard.html", ptaci=ptaci, params=params, filter_options=filter_options)

if __name__ == "__main__":
    app.run(debug=True)