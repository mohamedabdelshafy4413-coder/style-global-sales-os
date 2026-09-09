from pathlib import Path

APP_NAME = "STYLE Global Sales OS"
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "style_sales_os.db"

MARKET_WEIGHTS = {
    "import_demand": 15,
    "import_growth": 10,
    "product_fit": 10,
    "buyer_quality": 10,
    "deal_potential": 10,
    "construction": 10,
    "repeat_potential": 10,
    "logistics": 7,
    "market_access": 7,
    "competition_advantage": 6,
    "fast_response": 5,
}

ACCOUNT_WEIGHTS = {
    "import_activity": 20,
    "purchasing_power": 20,
    "product_fit": 15,
    "repeat_potential": 15,
    "project_activity": 10,
    "decision_access": 8,
    "financial_strength": 7,
    "buying_signal": 5,
}

# Default product set for the Buyer Intelligence module.
# These can be changed later in the UI without changing the scoring model.
STYLE_MATERIALS = [
    "Galala Light",
    "Sunny Light",
    "Meli Brown",
    "Meli Grey",
    "Zafarana Flower",
]

BUYER_INTELLIGENCE_WEIGHTS = {
    "import_signal": 25,
    "buyer_scale": 20,
    "material_fit": 15,
    "repeat_potential": 10,
    "project_signal": 10,
    "contact_quality": 8,
    "decision_access": 5,
    "source_confidence": 7,
}
