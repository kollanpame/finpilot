import os
from dotenv import load_dotenv
from plaid import Configuration, ApiClient
from plaid.api import plaid_api

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()

# Pobieranie zmiennych środowiskowych
PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID") 
PLAID_SECRET = os.getenv("PLAID_SECRET")       
PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")   

# Słownik z adresami URL dla różnych środowisk Plaid
environments = {
    "sandbox": "https://sandbox.plaid.com",       
    "development": "https://development.plaid.com",  
    "production": "https://production.plaid.com"     
}

# Konfiguracja klienta Plaid
configuration = Configuration(
    host=environments[PLAID_ENV],                
    api_key={
        "clientId": PLAID_CLIENT_ID,            
        "secret": PLAID_SECRET                   
    }
)

# Wyłączenie weryfikacji SSL
configuration.verify_ssl = False

# Inicjalizacja klienta API
api_client = ApiClient(configuration)

# Eksport instancji klienta Plaid
plaid_client = plaid_api.PlaidApi(api_client)