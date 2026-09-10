const { URL } = require('url');
const net = require('net');
const dns = require('dns').promises;

const ALLOWED_HOST_SUFFIXES = [
  'google.com',
  'googleapis.com',
  'googleusercontent.com',
  'goo.gl',
  'g.co',
  'g.page',
  'apple.com',
  'apple.co',
];

function hostnameAllowed(hostname) {
  const host = String(hostname || '').trim().toLowerCase().replace(/\.$/, '');
  if (!host) return false;
  return ALLOWED_HOST_SUFFIXES.some((domain) => host === domain || host.endsWith(`.${domain}`));
}

function isPrivateOrReservedIp(ip) {
  const version = net.isIP(ip);
  if (version === 4) {
    const [a, b] = ip.split('.').map(Number);
    if (a === 0 || a === 10 || a === 127) return true;
    if (a === 169 && b === 254) return true;
    if (a === 192 && b === 168) return true;
    if (a === 172 && b >= 16 && b <= 31) return true;
    return false;
  }
  if (version === 6) {
    const normalized = ip.toLowerCase();
    if (normalized === '::1') return true;
    if (normalized.startsWith('fe80:')) return true;
    if (normalized.startsWith('fc') || normalized.startsWith('fd')) return true;
    if (normalized.startsWith('::ffff:')) {
      return isPrivateOrReservedIp(normalized.slice('::ffff:'.length));
    }
  }
  return false;
}

function parseHttpUrl(raw, base) {
  let parsed;
  try {
    parsed = base ? new URL(raw, base) : new URL(raw);
  } catch {
    throw new Error('Invalid URL.');
  }
  if (!/^https?:$/i.test(parsed.protocol)) {
    throw new Error('Only http(s) map links can be fetched.');
  }
  const host = parsed.hostname.replace(/\.$/, '').toLowerCase();
  if (net.isIP(host)) {
    throw new Error('Map links must use a known maps host.');
  }
  if (!hostnameAllowed(host)) {
    throw new Error('Only Google Maps and Apple Maps links can be fetched.');
  }
  return parsed;
}

async function assertSafeMapUrl(raw, base) {
  const parsed = parseHttpUrl(raw, base);
  const { address } = await dns.lookup(parsed.hostname);
  if (isPrivateOrReservedIp(address)) {
    throw new Error('Refusing to fetch private addresses.');
  }
  return parsed;
}

module.exports = {
  ALLOWED_HOST_SUFFIXES,
  hostnameAllowed,
  isPrivateOrReservedIp,
  parseHttpUrl,
  assertSafeMapUrl,
};
