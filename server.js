require('dotenv').config();
const express = require('express');
const axios = require('axios');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

async function getAccessToken() {
  const url = `https://login.microsoftonline.com/${process.env.TENANT_ID}/oauth2/v2.0/token`;

  const params = new URLSearchParams();
  params.append("grant_type", "client_credentials");
  params.append("client_id", process.env.CLIENT_ID);
  params.append("client_secret", process.env.CLIENT_SECRET);
  params.append("scope", "https://graph.microsoft.com/.default");

  try {
    const res = await axios.post(url, params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });

    if (!res.data.access_token) {
      throw new Error("No access token received from Azure");
    }

    return res.data.access_token;
  } catch (err) {
    console.error("Token fetch failed:", err.response?.data || err.message);
    throw err;
  }
}

app.get('/api/approved-emails', async (req, res) => {
  try {
    const token = await getAccessToken();

    const listUrl = `https://graph.microsoft.com/v1.0/sites/${process.env.SHAREPOINT_HOSTNAME}/${process.env.SITE_PATH}/lists/${process.env.LIST_NAME}/items?$expand=fields&$top=999`;

    const listRes = await axios.get(listUrl, {
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: "application/json"
      }
    });

    const emails = listRes.data.value.map(item => {
      const fields = item.fields || {};
      return (fields.Username || fields.TitleId || fields.Title || "").trim();
    }).filter(Boolean);

    res.json({ emails });

  } catch (err) {
    console.error("Error fetching SharePoint list:", err.response?.data || err.message);
    res.status(500).json({ error: "Failed to fetch list" });
  }
});

app.listen(PORT, () => console.log(`✅ Backend running on port ${PORT}`));
