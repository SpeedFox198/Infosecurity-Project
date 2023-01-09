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


#Set 2FA user page
@settings_bp.post("/twofa")
@login_required
@validate_request(TwoFABody)
async def google_authenticator(data: TwoFABody):
    #Check if 2FA is already enabled
    twoFA_checker = await check_2fa_exists(await current_user.user_id)
    if twoFA_checker:
        return {"message": "2FA already enabled"}, 400
    else:
        #Create 2FA after checking if user input is valid
        secret_token = pyotp.random_base32()
        OTP_check = data.twofacode
        verified = pyotp.TOTP(secret_token).verify(OTP_check)
        if verified:
            await create_2fa(await current_user.user_id, secret_token)
            return {"message": "2FA enabled"}, 200
        else:
            return {"message": "Invalid 2FA code"}, 400

@settings_bp.get("/twofa_backupcode")
@login_required
async def google_authenticator_backupcodes():
    #Check if 2FA is already enabled
    twoFA_checker = await check_2fa_exists(await current_user.user_id)
    if twoFA_checker:
        #Check for existing backup codes
        backupcode_checker = await get_2fa_backup_codes(await current_user.user_id)
        if backupcode_checker:
            return {"message": "Backup codes already exist"}, 400
        else:
            #Create backup codes
            await create_2fa_backup_codes(await current_user.user_id)
            return {"message": "Backup codes created"}, 200
    else:
        return {"message": "2FA not enabled"}, 400


@settings_bp.delete("/twofa")
@login_required
async def delete_2fa():
    twoFA_checker = await check_2fa_exists(await current_user.user_id)
    if twoFA_checker:
        await delete_2fa(await current_user.user_id)
        return {"message": "2FA disabled"}, 200
    else:
        return {"message": "2FA not enabled"}, 400
