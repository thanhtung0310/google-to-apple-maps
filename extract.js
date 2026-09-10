const COORD_PAIR = /^(-?\d+\.\d+),\s*(-?\d+\.\d+)$/;

function isCoordPair(value) {
  return typeof value === 'string' && COORD_PAIR.test(value.trim());
}

/**
 * Prefer a dropped pin over the map camera (viewport).
 * Priority: protobuf !3d!4d, then ll/q/query coord params, then exact raw pair, then @viewport.
 */
function extractCoords(text) {
  if (!text) return null;

  const protobuf = text.match(/!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)/);
  if (protobuf) {
    return { lat: parseFloat(protobuf[1]), lng: parseFloat(protobuf[2]), source: 'protobuf' };
  }

  const param = text.match(/[?&](?:ll|q|query)=(-?\d+\.\d+),\s*(-?\d+\.\d+)/);
  if (param) {
    return { lat: parseFloat(param[1]), lng: parseFloat(param[2]), source: 'param' };
  }

  const exactRaw = text.trim().match(COORD_PAIR);
  if (exactRaw) {
    return { lat: parseFloat(exactRaw[1]), lng: parseFloat(exactRaw[2]), source: 'raw' };
  }

  const viewport = text.match(/@(-?\d+\.\d+),(-?\d+\.\d+)/);
  if (viewport) {
    return { lat: parseFloat(viewport[1]), lng: parseFloat(viewport[2]), source: 'viewport' };
  }

  return null;
}

function decodeQueryValue(raw) {
  try {
    return decodeURIComponent(String(raw).replace(/\+/g, ' ')).trim();
  } catch {
    return String(raw).replace(/\+/g, ' ').trim();
  }
}

function extractPlaceName(text) {
  if (!text) return null;

  const placePath = text.match(/\/place\/([^/@]+)/);
  if (placePath) {
    const name = decodeQueryValue(placePath[1].split('/')[0]);
    if (name && !isCoordPair(name) && name.length < 200) return name;
  }

  const params = text.matchAll(/[?&](?:q|query|name|daddr)=([^&]+)/gi);
  for (const match of params) {
    const value = decodeQueryValue(match[1]);
    if (value && !isCoordPair(value) && value.length > 1 && value.length < 200) {
      return value;
    }
  }

  return null;
}

function buildMapUrls(lat, lng, name) {
  const query = name && name.trim() ? name.trim() : `${lat},${lng}`;
  const encodedQuery = encodeURIComponent(query);
  const appleUrl = `https://maps.apple.com/?ll=${lat},${lng}&q=${encodedQuery}`;
  // Always pin by coordinates so a place name cannot send Google Search to a different result.
  const googleUrl = `https://www.google.com/maps/search/?api=1&query=${lat},${lng}`;
  return { appleUrl, googleUrl, query };
}

module.exports = {
  extractCoords,
  extractPlaceName,
  buildMapUrls,
};
