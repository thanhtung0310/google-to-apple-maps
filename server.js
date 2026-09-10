const express = require('express');
const axios = require('axios');
const path = require('path');
const { extractCoords, extractPlaceName, buildMapUrls } = require('./extract');

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname));

app.get('/api/health', (_req, res) => {
  res.json({ ok: true });
});

async function expandMapLink(cleanUrl) {
  const redirectChain = [cleanUrl];
  const response = await axios.get(cleanUrl, {
    maxRedirects: 15,
    timeout: 10000,
    headers: {
      'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1',
      'Accept-Language': 'en-US,en;q=0.9',
      'Cookie': 'CONSENT=PENDING+999; SOCS=CAISHAgBEhJnd3NfMjAyMzA4MTAtMF9SQzEgGgJ2aSAAYACaAcU'
    },
    beforeRedirect: (_options, { headers }) => {
      if (headers.location) redirectChain.push(headers.location);
    }
  });

  const finalUrl = response.request?.res?.responseUrl || response.config?.url || '';
  redirectChain.push(finalUrl);
  const html = typeof response.data === 'string' ? response.data : '';
  return {
    redirectChain,
    searchBlob: redirectChain.join(' ') + ' ' + html,
  };
}

app.post('/api/resolve', async (req, res) => {
  const { url } = req.body;
  if (!url) return res.status(400).json({ error: 'URL is required.' });

  const cleanUrl = url.trim();
  let searchBlob = cleanUrl;
  let nameSource = cleanUrl;
  let coords = extractCoords(cleanUrl);
  const isAppleSource = /maps\.apple\.com/i.test(cleanUrl);
  const needsExpand = !coords || coords.source === 'viewport';

  if (needsExpand && /^https?:\/\//i.test(cleanUrl)) {
    try {
      const expanded = await expandMapLink(cleanUrl);
      searchBlob = expanded.searchBlob;
      nameSource = expanded.redirectChain.join(' ');
      const resolved = extractCoords(searchBlob);
      if (resolved) coords = resolved;
    } catch (err) {
      if (!coords) {
        console.error('Resolution Error:', err.message);
        return res.status(500).json({ error: 'Failed to resolve map link.', details: err.message });
      }
    }
  }

  if (coords) {
    const name = extractPlaceName(nameSource) || extractPlaceName(cleanUrl);
    const { appleUrl, googleUrl } = buildMapUrls(coords.lat, coords.lng, name);

    return res.json({
      success: true,
      lat: coords.lat,
      lng: coords.lng,
      name: name || undefined,
      detectedPlatform: isAppleSource ? 'Apple Maps' : 'Google Maps',
      targetPlatform: isAppleSource ? 'Google Maps' : 'Apple Maps',
      targetUrl: isAppleSource ? googleUrl : appleUrl,
      appleUrl,
      googleUrl
    });
  }

  return res.status(422).json({ error: 'Could not extract coordinates from the provided link.' });
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running at http://localhost:${PORT}`));
