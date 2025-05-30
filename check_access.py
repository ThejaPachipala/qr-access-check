from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
TENANT_ID = 'your-tenant-id'
LIST_ID = 'your-list-id'  # or derive via Graph API
SITE_ID = 'your-site-id'

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
