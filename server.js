const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname)); // Serves index.html from current directory

/**
 * Helper to extract coordinates from text, URLs, or protobuf strings
 */
function extractCoordsFromText(text) {
  if (!text) return null;

  // Pattern 1: Exact Dropped Pin Protobuf (!3dLAT!4dLNG)
  let match = text.match(/!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)/);
  if (match) {
    return { lat: parseFloat(match[1]), lng: parseFloat(match[2]), method: 'protobuf' };
  }

  // Pattern 2: Viewport Coordinates (@LAT,LNG)
  match = text.match(/@(-?\d+\.\d+),(-?\d+\.\d+)/);
  if (match) {
    return { lat: parseFloat(match[1]), lng: parseFloat(match[2]), method: 'viewport' };
  }

  // Pattern 3: Query parameters (q=LAT,LNG or ll=LAT,LNG)
  match = text.match(/[?&](?:q|ll)=(-?\d+\.\d+),(-?\d+\.\d+)/);
  if (match) {
    return { lat: parseFloat(match[1]), lng: parseFloat(match[2]), method: 'query_param' };
  }

  // Pattern 4: Raw Coordinates string (21.011967, 105.838405)
  match = text.match(/^(-?\d+\.\d+),\s*(-?\d+\.\d+)$/);
  if (match) {
    return { lat: parseFloat(match[1]), lng: parseFloat(match[2]), method: 'raw' };
  }

  return null;
}

app.post('/api/resolve', async (req, res) => {
  const { url } = req.body;

  if (!url) {
    return res.status(400).json({ error: 'URL is required.' });
  }

  const cleanUrl = url.trim();

  // 1. Instant check for raw coordinate input
  const rawCoords = extractCoordsFromText(cleanUrl);
  if (rawCoords && rawCoords.method === 'raw') {
    return res.json({
      success: true,
      lat: rawCoords.lat,
      lng: rawCoords.lng,
      appleUrl: `https://maps.apple.com/?ll=${rawCoords.lat},${rawCoords.lng}&q=${rawCoords.lat},${rawCoords.lng}`
    });
  }

  try {
    const redirectChain = [cleanUrl];

    // 2. Perform HTTP GET following redirects
    const response = await axios.get(cleanUrl, {
      maxRedirects: 15,
      timeout: 10000,
      headers: {
        // Mobile Safari UA ensures Google returns clean mobile layout without heavy JS blocks
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        // Bypasses Google's Cookie Consent prompt on EU/VPN/MDM networks
        'Cookie': 'CONSENT=PENDING+999; SOCS=CAISHAgBEhJnd3NfMjAyMzA4MTAtMF9SQzEgGgJ2aSAAYACaAcU'
      },
      beforeRedirect: (options, { headers }) => {
        if (headers.location) {
          redirectChain.push(headers.location);
        }
      }
    });

    const finalUrl = response.request?.res?.responseUrl || response.config?.url || '';
    redirectChain.push(finalUrl);

    // Combine redirect history + HTML body content to scan all possible locations
    const fullSearchBlob = redirectChain.join(' ') + ' ' + (typeof response.data === 'string' ? response.data : '');

    // 3. Extract Coordinates
    let coords = extractCoordsFromText(fullSearchBlob);

    // 4. Fallback: Parse HTML Meta Refresh tag if present
    if (!coords && typeof response.data === 'string') {
      const metaRefresh = response.data.match(/content="0;\s*url=([^"]+)"/i);
      if (metaRefresh && metaRefresh[1]) {
        coords = extractCoordsFromText(metaRefresh[1]);
      }
    }

    if (coords) {
      return res.json({
        success: true,
        lat: coords.lat,
        lng: coords.lng,
        extractionMethod: coords.method,
        appleUrl: `https://maps.apple.com/?ll=${coords.lat},${coords.lng}&q=${coords.lat},${coords.lng}`
      });
    }

    // Return detailed error for debugging if parsing fails
    return res.status(422).json({
      error: 'Could not extract coordinates from expanded link.',
      debug: {
        redirectChain,
        finalUrl
      }
    });

  } catch (err) {
    console.error('Resolution Error:', err.message);
    return res.status(500).json({
      error: 'Failed to resolve Google Maps link.',
      details: err.message
    });
  }
});

// Serve index.html for root path
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});