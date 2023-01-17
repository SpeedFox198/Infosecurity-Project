import pyotp
import sqlalchemy as sa
from quart import Blueprint
from quart_schema import validate_request, validate_response
from models.request_data import TwoFABody
from models.response_data import UserData
from db_access.twoFA import create_2fa, get_2fa, delete_2fa
from db_access.globals import async_session
from quart_auth import current_user, login_required

from models import TwoFA
from db_access.backup_codes import get_2fa_backup_codes
from db_access.twoFA import check_2fa_exists
from db_access.backup_codes import create_2fa_backup_codes


settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


@settings_bp.get("/twofa_secretgenerate")
@login_required
async def google_secret():
    #Generate the secret token
    twoFA_checker = await check_2fa_exists(await current_user.user_id)
    if twoFA_checker:
        existingsecret = (await get_2fa(await current_user.user_id)).secret
        return {"message": "Secret Already Exists", "secret": existingsecret}, 200
    else:
        secret_token = pyotp.random_base32()
        await create_2fa(await current_user.user_id, secret_token)
        return {"message":"Secret generated", "secret": secret_token}, 200

#Set 2FA user page
@settings_bp.post("/twofa")
@login_required
@validate_request(TwoFABody)
async def google_authenticator(data: TwoFABody):
    #Check if 2FA is already enabled
    if current_user.twofa_status:
        return {"message": "2FA already enabled"}, 400
    else:
        twoFA_code = (await get_2fa(await current_user.user_id))[1]
        secret_token = twoFA_code
        OTP_check = data.twofacode
        verified = pyotp.TOTP(secret_token).verify(OTP_check)
        if verified:
            await create_2fa_backup_codes(await current_user.user_id)
            backupcodes = await get_2fa_backup_codes(await current_user.user_id)
            await current_user.update(twofa_status=True)
            return {"message": "2FA enabled", "backupcodes": backupcodes}, 200
        else:
            return {"message": "Invalid 2FA code"}, 400


@settings_bp.delete("/twofa-delete")
@login_required
async def delete_2fa():
    if current_user.twofa_status:
        await delete_2fa(await current_user.user_id)
        return {"message": "2FA disabled"}, 200
    else:
        return {"message": "2FA not enabled"}, 400
