from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text

app = FastAPI(title="Susedská Výpomoc API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Zmena mssql+pyodbc na mssql+pymssql
DB_URL = "mssql+pymssql://Matus-admin:[REDACTED]@skolsky-projekt.database.windows.net:1433/SusedskaBurza"

engine = create_engine(DB_URL)

@app.get("/api/tabulka")
def ukaz_tabulku():
    try:
        with engine.connect() as connection:
            # Tento dopyt vráti zoznam všetkých tabuliek v databáze
            vysledok = connection.execute(text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"))
            riadky = [row._asdict() for row in vysledok]
            return {"data": riadky}
    except Exception as e:
        return {"chyba": str(e)}