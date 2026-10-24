import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# --- Servírovanie statických súborov (frontend) ---
# Mountne sa iba ak existuje zložka frontend
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def read_index():
    """Vráti hlavné HTML okno (frontend)."""
    if os.path.exists("frontend/index.html"):
        return FileResponse("frontend/index.html")
    return {"sprava": "FastAPI backend beží úspešne. Frontend nie je dostupný."}


@app.get("/api/tabulka")
def ukaz_tabulku():
    """Vráti zoznam tabuliek z databázy."""
    try:
        with engine.connect() as connection:
            vysledok = connection.execute(
                text("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
            )
            riadky = [row._asdict() for row in vysledok]
            return {"data": riadky}
    except Exception as e:
        return {"chyba": str(e)}
