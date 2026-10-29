from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import pymssql
from dotenv import load_dotenv

# Načíta premenné prostredia z .env súboru (ak existuje)
load_dotenv()

app = FastAPI()

# --- PREPOJENIE NA DATABÁZU ---
# Všetky hodnoty MUSIA byť nastavené ako environment premenné
# lokálne cez .env, na Azure cez App Service → Environment variables
DB_SERVER = os.environ["DB_SERVER"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]


def get_db_data():
    try:
        conn = pymssql.connect(
            server=DB_SERVER,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            as_dict=True,
        )
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 50 * FROM Users;")
        rows = cursor.fetchall()
        conn.close()
        return {"data": rows}
    except Exception as e:
        return {"chyba": str(e)}


# --- 1. ROUTA PRE API (DÁTA) ---
@app.get("/api/tabulka")
def get_tabulka():
    return get_db_data()


# --- 2. ROUTA PRE FRONTEND (HTML STRÁNKA) ---
@app.get("/")
def serve_frontend():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.abspath(os.path.join(base_dir, "..", "web", "frontend", "index.html"))

    if os.path.exists(index_path):
        return FileResponse(index_path)

    return {"chyba": f"Súbor index.html sa nenašiel na ceste: {index_path}"}
