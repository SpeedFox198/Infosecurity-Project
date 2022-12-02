from quart import Blueprint
from quart_auth import login_required

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.get("/")
async def index():
    return {"message": "Welcome to Test Quart App API"}


@api_bp.get("/users")
@login_required
async def users():
    data = [
        {
            "id": 1,
            "name": "bob"
        },
        {
            "id": 2,
            "name": "alice"
        }
    ]
    return data
