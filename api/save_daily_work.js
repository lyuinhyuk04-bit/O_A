const fs = require('fs');
const path = require('path');

module.exports = async function handler(req, res) {
  // CORS Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Content-Type', 'application/json');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ status: 'error', message: 'Method Not Allowed' });
  }

  try {
    let payload = req.body;
    if (typeof payload === 'string') {
      try {
        payload = JSON.parse(payload);
      } catch (e) {
        return res.status(400).json({ status: 'error', message: 'Invalid JSON body' });
      }
    }

    const { member, date, content } = payload;
    if (!member || !date) {
      return res.status(400).json({ status: 'error', message: 'Missing member or date in request' });
    }

    const supabaseUrl = process.env.SUPABASE_URL;
    const supabaseAnonKey = process.env.SUPABASE_ANON_KEY;

    if (supabaseUrl && supabaseAnonKey) {
      // 1. Check if the record already exists
      const checkUrl = `${supabaseUrl}/rest/v1/daily_works?member=eq.${member}&date=eq.${date}`;
      const checkResp = await fetch(checkUrl, {
        headers: {
          'apikey': supabaseAnonKey,
          'Authorization': `Bearer ${supabaseAnonKey}`
        }
      });

      if (checkResp.ok) {
        const records = await checkResp.json();
        if (records && records.length > 0) {
          // Update
          const recordId = records[0].id;
          const updateUrl = `${supabaseUrl}/rest/v1/daily_works?id=eq.${recordId}`;
          const updateResp = await fetch(updateUrl, {
            method: 'PATCH',
            headers: {
              'apikey': supabaseAnonKey,
              'Authorization': `Bearer ${supabaseAnonKey}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content })
          });

          if (!updateResp.ok) {
            const updateErr = await updateResp.text();
            return res.status(500).json({ status: 'error', message: `Supabase daily_works update failed: ${updateErr}` });
          }
        } else {
          // Insert
          const insertUrl = `${supabaseUrl}/rest/v1/daily_works`;
          const insertResp = await fetch(insertUrl, {
            method: 'POST',
            headers: {
              'apikey': supabaseAnonKey,
              'Authorization': `Bearer ${supabaseAnonKey}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ member, date, content })
          });

          if (!insertResp.ok) {
            const insertErr = await insertResp.text();
            return res.status(500).json({ status: 'error', message: `Supabase daily_works insert failed: ${insertErr}` });
          }
        }
      } else {
        const checkErr = await checkResp.text();
        return res.status(500).json({ status: 'error', message: `Supabase daily_works check failed: ${checkErr}` });
      }
    }

    // Always try to write local daily_works.json cache (works locally, fails silently on Vercel)
    try {
      const worksPath = path.join(process.cwd(), 'daily_works.json');
      let works = {};
      if (fs.existsSync(worksPath)) {
        try {
          works = JSON.parse(fs.readFileSync(worksPath, 'utf8'));
        } catch (e) {
          works = {};
        }
      }

      if (!works[date]) {
        works[date] = {};
      }
      works[date][member] = content;

      fs.writeFileSync(worksPath, JSON.stringify(works, null, 2), 'utf8');
    } catch (writeErr) {
      // Ignore write failures in read-only environment
    }

    return res.status(200).json({ status: 'ok' });
  } catch (err) {
    return res.status(500).json({ status: 'error', message: err.message });
  }
};
