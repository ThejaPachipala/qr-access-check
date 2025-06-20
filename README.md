# SharePoint App-Only Access via Microsoft Graph

This Node.js backend fetches a SharePoint list using Microsoft Graph `client_credentials` flow. It avoids requiring end-user SharePoint permissions.

## 🔧 Setup

1. Register an Azure AD App
2. Grant `Sites.Read.All` (Application) in Microsoft Graph API
3. Admin consent the permission
4. Assign app permissions to your SharePoint site using appinv.aspx

## 🧪 Run Locally

```bash
npm install
cp .env.example .env # and fill values
node server.js
