import pyotp
import json
import os
import datetime
import sqlalchemy as sa
from quart import Blueprint, render_template, current_app 
from quart_schema import validate_request, validate_response
from models.request_data import TwoFABody
from models.response_data import UserData
from models import Device
from db_access.twoFA import create_2fa, get_2fa, delete_2fa
from db_access.globals import async_session
from db_access.user import get_user_details
from db_access.device import get_device
from quart_auth import current_user, login_required
from zipfile import ZipFile, ZIP_DEFLATED
from google_authenticator.google_email_send import gmail_send

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
    if (await current_user.twofa_status):
        print("Checkpoint No")
        return {"message": "2FA already enabled"}, 400
    else:
        twoFA_code = await get_2fa(await current_user.user_id)
        secret_token = twoFA_code.secret
        OTP_check = data.twofacode
        verified = pyotp.TOTP(secret_token).verify(OTP_check)
        if verified:
            await create_2fa_backup_codes(await current_user.user_id)
            #Put the backup codes in an array
            backup_codes: list[str] = [
                bc.code
                for bc in await get_2fa_backup_codes(await current_user.user_id)
            ]
            print("Checkpoint Yes")
            return {"message": "2FA enabled", "backup_codes": backup_codes}, 200
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


@settings_bp.get("/get-account-information")
@login_required
async def get_account_information():
    
    async with async_session() as session:
        # get user details
        user_results = await get_user_details(current_user.user_id)

        # get device details
        statement = sa.select(Device)\
            .where(Device.user_id == await current_user.user_id)\
            .order_by(sa.desc(Device.time))
        results = await session.execute(statement)
        device_results = results.mappings().all()
    
    # convert all data into json format
    user_json = json.loads(json.dumps(user_results, indent=4, default=str))
    device_json = json.loads(json.dumps(device_results, indent=4, default=str))

    # write to json file
    with open("account_data.json", "w") as outfile:
        outfile.write(user_json)
    
    with open("account_data.json", "a") as outfile:
        outfile.append(device_json)
    
    # write to html file
    html_template = await render_template("account_data.html", 
                                username=user_json['username'], 
                                email=user_json['email'], 
                                first_name=user_json['first_name'], 
                                last_name=user_json['last_name'], 
                                twofa_status=user_json['twofa_status'], 
                                device_id=device_json['device_id'], 
                                device_name=device_json['device_name'], 
                                device_type=device_json['device_type'])

    with open("account_data.html", "w") as outfile:
        outfile.write(html_template)

    os.makedirs(f"media/exports/{await current_user.user_id}", exist_ok=True)
    # writing files to zipfile
    with ZipFile(f"media/exports/{await current_user.user_id}/account_data.zip", "w",
                compression=ZIP_DEFLATED,
                compresslevel=9) as zip:
        zip.write("account_data.json")
        zip.write("account_data.html")
    
    # directory = os.path.join(os.getcwd(), f"media/exports/{await current_user.user_id}/account_data.zip")

    # crafting the link
    url_serialiser = await current_app.config["url_serialiser"]
    email = user_json['email']
    token = url_serialiser.dumps(email)
    link = f"https://localhost:8443/api/{token}/{await current_user.user_id}/account_data.zip"

    # email the link to the user
    subject = "Your Bubbles Account - Requested Account Report"
    date_requested = datetime.date.today()
    expiry_date = date_requested + datetime.timedelta(days=30)
    message = await render_template("requested_data.html",
                                    date_requested=date_requested,
                                    expiry_date=expiry_date,
                                    link=link
                                    )
    gmail_send(email, subject, message)