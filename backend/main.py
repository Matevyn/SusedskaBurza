from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import pymssql

app = FastAPI()

# --- PREPOJENIE NA DATABÁZU ---
DB_SERVER = os.getenv("DB_SERVER", "skolsky-projekt.database.windows.net")
DB_USER = os.getenv("DB_USER", "matus")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")  # Na Azure sa berie z Environment Variables
DB_NAME = os.getenv("DB_NAME", "SusedskaBurza")

def get_db_data():
    try:
        conn = pymssql.connect(
            server=DB_SERVER,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            as_dict=True
        )
        cursor = conn.cursor()
        # Názov tvojej tabuľky v databáze
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
    # Zistíme cestu k adresáru, kde leží main.py (t.j. web/backend)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Prejdeme o úroveň vyššie do 'web' a potom do 'frontend/index.html'
    index_path = os.path.abspath(os.path.join(base_dir, "..", "web", "frontend", "index.html"))
    
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    return {"chyba": f"Súbor index.html sa nenašiel na ceste: {index_path}"}# redeploy trigger
