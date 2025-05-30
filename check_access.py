from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CLIENT_ID = 'd13c0cca-d75f-4bc9-8dcb-b18315c40d0e'
CLIENT_SECRET = '0P58Q~SimMHbMDVBEsIvbhMWK3d6NSdwjzoVlcJR'
TENANT_ID = 'a456fbc2-921d-42a4-a7a8-fc0f343ede61'
LIST_ID = 'your-list-id'  # or derive via Graph API
SITE_ID = 'TimesheetScoreCards'

def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials',
        'scope': 'https://graph.microsoft.com/.default'
    }
    resp = requests.post(url, data=data)
    return resp.json().get('access_token')

@app.route('/check_access', methods=['POST'])
def check_access():
    email = request.json.get('email')
    token = get_access_token()
    headers = {
        'Authorization': f'Bearer {token}'
    }
    url = f"https://graph.microsoft.com/v1.0/sites/{SITE_ID}/lists/Vehiclepool/items?$expand=fields&$top=999"
    resp = requests.get(url, headers=headers)
    items = resp.json().get('value', [])
    
    for item in items:
        if item['fields'].get('Username', '').lower() == email.lower():
            return jsonify({'access': True})
    
    return jsonify({'access': False})
