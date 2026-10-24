import os
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

# --- Databázové pripojenie z environment variables ---
# Očakávané premenné:
#   DB_USER       – užívateľ v Azure SQL
#   DB_PASSWORD   – heslo
#   DB_SERVER     – logical server (napr. skolsky-projekt.database.windows.net)
#   DB_NAME       – názov databázy
#   DB_DRIVER     – voliteľné, predvolené: pymssql
DB_USER = os.environ.get("DB_USER", "Matus-admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_SERVER = os.environ.get("DB_SERVER", "skolsky-projekt.database.windows.net")
DB_NAME = os.environ.get("DB_NAME", "SusedskaBurza")
DB_DRIVER = os.environ.get("DB_DRIVER", "pymssql")

if not DB_PASSWORD:
    raise RuntimeError(
        "Chýba heslo do databázy. Nastavte environment premennú DB_PASSWORD."
    )

DB_URL = f"mssql+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:1433/{DB_NAME}"

engine = create_engine(DB_URL)


@app.get("/api/tabulka")
def ukaz_tabulku():
    try:
        with engine.connect() as connection:
            vysledok = connection.execute(
                text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
            )
            riadky = [row._asdict() for row in vysledok]
            return {"data": riadky}
    except Exception as e:
        return {"chyba": str(e)}
