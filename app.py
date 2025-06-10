from flask import Flask, request, jsonify
import requests
from msal import ConfidentialClientApplication

app = Flask(__name__)

# Config
CLIENT_ID = 'd13c0cca-d75f-4bc9-8dcb-b18315c40d0e'
CLIENT_SECRET = '0P58Q~SimMHbMDVBEsIvbhMWK3d6NSdwjzoVlcJR'
TENANT_ID = 'a456fbc2-921d-42a4-a7a8-fc0f343ede61'
SHAREPOINT_SITE = 'smartinfrastructure.sharepoint.com'
SITE_PATH = 'teams/TimesheetScoreCards'
LIST_NAME = 'Vehiclepool'

# Scopes for SharePoint access
SCOPE = [f'https://{SHAREPOINT_SITE}/.default']

# MSAL authority
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'

# Get MSAL access token
def get_access_token():
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    token_result = app.acquire_token_silent(SCOPE, account=None)
    if not token_result:
        token_result = app.acquire_token_for_client(scopes=SCOPE)

    if 'access_token' in token_result:
        return token_result['access_token']
    else:
        raise Exception(f"Token error: {token_result.get('error_description')}")

# Check if user email is authorized
def is_email_authorized(email):
    access_token = get_access_token()
    url = f'https://graph.microsoft.com/v1.0/sites/{SHAREPOINT_SITE}:/{SITE_PATH}:/lists/{LIST_NAME}/items?$expand=fields&$top=999'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)
    if not response.ok:
        raise Exception(f'SharePoint API error: {response.status_code} {response.text}')

    items = response.json().get('value', [])
    email = email.lower()
    
    for item in items:
        username = item.get("fields", {}).get("Username", "").lower()
        if username == email:
            return True
    return False

# Route to check email
@app.route('/check_email')
def check_email():
    email = request.args.get('email', '').strip().lower()
    if not email:
        return jsonify({'error': 'Missing email'}), 400
    try:
        authorized = is_email_authorized(email)
        return jsonify({'authorized': authorized})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
