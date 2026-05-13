import csv
import sqlite3

CSV_FILE = "dataset_ptaci_final.csv"
DB_FILE = "ptaci.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ptaci (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nazev TEXT,
    vedecky_nazev TEXT,
    rad TEXT,
    celed TEXT,
    delka_cm INTEGER,
    rozpeti_cm INTEGER,
    hmotnost_g INTEGER,
    status_ohrozeni TEXT,
    typ_potravy TEXT,
    migrace INTEGER,
    vyskyt_kontinent TEXT,
    snuska_ks REAL
)
""")

pocet = 0
with open(CSV_FILE, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute("""
            INSERT INTO ptaci (
                nazev, vedecky_nazev, rad, celed,
                delka_cm, rozpeti_cm, hmotnost_g,
                status_ohrozeni, typ_potravy, migrace,
                vyskyt_kontinent, snuska_ks
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row.get("nazev"),
            row.get("vedecky_nazev"),
            row.get("rad"),
            row.get("celed"),
            int(row["delka_cm"])       if row.get("delka_cm")       else None,
            int(row["rozpeti_cm"])     if row.get("rozpeti_cm")     else None,
            int(row["hmotnost_g"])     if row.get("hmotnost_g")     else None,
            row.get("status_ohrozeni"),
            row.get("typ_potravy"),
            int(row["migrace"])        if row.get("migrace")        else None,
            row.get("vyskyt_kontinent"),
            float(row["snuska_ks"])    if row.get("snuska_ks")      else None,
        ))
        pocet += 1

conn.commit()
conn.close()

print(f"Import dokončen. Importováno záznamů: {pocet}")
