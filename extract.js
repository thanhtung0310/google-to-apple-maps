const NUM = '-?\\d+(?:\\.\\d+)?';
const COORD_PAIR = new RegExp(`^(${NUM}),\\s*(${NUM})$`);
const APPLE_SOURCE = /(maps\.apple\.com|apple\.co)/i;

function isCoordPair(value) {
  return typeof value === 'string' && COORD_PAIR.test(value.trim());
}

function isAppleMapsSource(text) {
  return APPLE_SOURCE.test(text || '');
}

function parseCoord(value) {
  return parseFloat(value);
}

/**
 * Prefer a dropped pin over the map camera (viewport).
 * Priority: protobuf !3d / !4d (any order), then coord query params, then exact raw pair, then @viewport.
 */
function extractCoords(text) {
  if (!text) return null;

  const latMatch = text.match(new RegExp(`!3d(${NUM})`));
  const lngMatch = text.match(new RegExp(`!4d(${NUM})`));
  if (latMatch && lngMatch) {
    return { lat: parseCoord(latMatch[1]), lng: parseCoord(lngMatch[1]), source: 'protobuf' };
  }

  const param = text.match(new RegExp(`[?&](?:ll|q|query|saddr|daddr|near)=(${NUM}),\\s*(${NUM})`));
  if (param) {
    return { lat: parseCoord(param[1]), lng: parseCoord(param[2]), source: 'param' };
  }

  const exactRaw = text.trim().match(COORD_PAIR);
  if (exactRaw) {
    return { lat: parseCoord(exactRaw[1]), lng: parseCoord(exactRaw[2]), source: 'raw' };
  }

  const viewport = text.match(new RegExp(`@(${NUM}),(${NUM})`));
  if (viewport) {
    return { lat: parseCoord(viewport[1]), lng: parseCoord(viewport[2]), source: 'viewport' };
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

  const placePath = text.match(/\/place\/([^/@?#]+)/);
  if (placePath) {
    const name = decodeQueryValue(placePath[1].split('/')[0]);
    if (name && !isCoordPair(name) && name.length < 200) return name;
  }

  const params = text.matchAll(/[?&](?:q|query|name|saddr|daddr|near)=([^&]+)/gi);
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
  const googleUrl = `https://www.google.com/maps/search/?api=1&query=${lat},${lng}`;
  return { appleUrl, googleUrl, query };
}

module.exports = {
  extractCoords,
  extractPlaceName,
  buildMapUrls,
  isAppleMapsSource,
};
