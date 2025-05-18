# Importujemy klasę FastAPI i odpowiedzi HTML
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Importujemy nasze routery (trasowania) z aplikacji
from app.routers import transactions, reports, categories, plaid

# Tworzymy instancję aplikacji FastAPI z metadanymi
app = FastAPI(
    title="FinPilot",  # Tytuł aplikacji
    description="API for personal finance automation with Plaid and PostgreSQL",  # Opis
    version="1.0.0"  # Wersja API
)

# Definiujemy główną trasę ("/"), która nie jest częścią dokumentacji Swagger
@app.get("/", include_in_schema=False)
async def root():
    return HTMLResponse(
        """
        <h1>Welcome in FinPilot API</h1>
        <p>Please, open <a href="/docs">Swagger UI</a> for using it with API.</p>
        """
    )

# Dołączamy router trasowania transakcji
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

# Dołączamy router trasowania raportów
app.include_router(reports.router, prefix="/reports", tags=["Reports"])

# Dołączamy router trasowania kategorii
app.include_router(categories.router, prefix="/categories", tags=["Categories"])

# Dołączamy router trasowania plaid
app.include_router(plaid.router)