from quart import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.get("/")
async def index():
    return {"message": "Welcome to Test Quart App API"}
