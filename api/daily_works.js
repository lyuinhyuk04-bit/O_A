const fs = require('fs');
const path = require('path');

module.exports = async function handler(req, res) {
  // CORS Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET');
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0');

  try {
    const supabaseUrl = process.env.SUPABASE_URL;
    const supabaseAnonKey = process.env.SUPABASE_ANON_KEY;

    let works = {};

    if (supabaseUrl && supabaseAnonKey) {
      // Fetch from Supabase
      const url = `${supabaseUrl}/rest/v1/daily_works?select=*`;
      const response = await fetch(url, {
        headers: {
          'apikey': supabaseAnonKey,
          'Authorization': `Bearer ${supabaseAnonKey}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        if (Array.isArray(data)) {
          data.forEach(item => {
            const d = item.date;
            const m = item.member;
            const c = item.content || '';
            if (d && m) {
              if (!works[d]) {
                works[d] = {};
              }
              works[d][m] = c;
            }
          });
        } else {
          console.error('Supabase daily_works response is not an array:', data);
          works = readLocalDailyWorks();
        }
      } else {
        const errText = await response.text();
        console.error('Supabase daily_works fetch failed:', errText);
        works = readLocalDailyWorks();
      }
    } else {
      works = readLocalDailyWorks();
    }

    res.status(200).json(works);
  } catch (err) {
    console.error('API Handler Exception:', err);
    res.status(500).json({ error: err.message, stack: err.stack });
  }
};

function readLocalDailyWorks() {
  const worksPath = path.join(process.cwd(), 'daily_works.json');
  if (fs.existsSync(worksPath)) {
    try {
      return JSON.parse(fs.readFileSync(worksPath, 'utf8'));
    } catch (e) {
      console.error('Failed to parse daily_works.json:', e);
    }
  }
  return {};
}
