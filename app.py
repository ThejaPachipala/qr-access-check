from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# ------------------ CONFIG ------------------
CLIENT_ID = 'd13c0cca-d75f-4bc9-8dcb-b18315c40d0e'
CLIENT_SECRET = '0P58Q~SimMHbMDVBEsIvbhMWK3d6NSdwjzoVlcJR'
TENANT_ID = 'a456fbc2-921d-42a4-a7a8-fc0f343ede61'

SHAREPOINT_HOSTNAME = 'smartinfrastructure.sharepoint.com'
SITE_PATH = 'teams/TimesheetScoreCards'  # Adjust if needed
LIST_NAME = 'Vehiclepool'

MS_FORM_URL = "https://forms.office.com/r/Saurgpg1XQ"  # optional

# --------------------------------------------

def get_access_token():
    url = f'https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()['access_token']

def get_site_id(token):
    url = f"https://graph.microsoft.com/v1.0/sites/{SHAREPOINT_HOSTNAME}:/sites/{SITE_PATH}"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['id']

def get_list_items(token, site_id):
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{LIST_NAME}/items?$expand=fields&$top=999"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('value', [])

@app.route('/check_access', methods=['POST'])
def check_access():
    try:
        data = request.json
        email = data.get('email', '').lower()

        if not email:
            return jsonify({'allowed': False, 'error': 'Email required'}), 400

        token = get_access_token()
        site_id = get_site_id(token)
        items = get_list_items(token, site_id)

        # Assuming SharePoint list field is called 'Username'
        for item in items:
            username = item.get("fields", {}).get("Username", "").lower()
            if username == email:
                return jsonify({'allowed': True})

        return jsonify({'allowed': False})
    
    except Exception as e:
        return jsonify({'allowed': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
