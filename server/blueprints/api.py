from quart import Blueprint
from quart_auth import login_required

API_BP = Blueprint("api", __name__, url_prefix="/api")


@API_BP.get("/")
async def index():
    return {"message": "Welcome to Test Quart App API"}


@API_BP.get("/users")
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
