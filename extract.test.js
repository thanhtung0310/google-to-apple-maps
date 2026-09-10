const assert = require('assert');
const { extractCoords, extractPlaceName, buildMapUrls, isAppleMapsSource } = require('./extract');
const { hostnameAllowed, isPrivateOrReservedIp, parseHttpUrl } = require('./urlGuard');

const pinAndViewport = 'https://www.google.com/maps/@10.0,20.0,17z/data=!3d21.011967!4d105.838405';
const pin = extractCoords(pinAndViewport);
assert.strictEqual(pin.source, 'protobuf');
assert.strictEqual(pin.lat, 21.011967);
assert.strictEqual(pin.lng, 105.838405);

const reversedProtobuf = extractCoords('data=!4d105.838405!3d21.011967');
assert.strictEqual(reversedProtobuf.source, 'protobuf');
assert.strictEqual(reversedProtobuf.lat, 21.011967);
assert.strictEqual(reversedProtobuf.lng, 105.838405);

const splitProtobuf = extractCoords('data=!3d21.5!1sxxx!4d105.8');
assert.strictEqual(splitProtobuf.lat, 21.5);
assert.strictEqual(splitProtobuf.lng, 105.8);

const viewportOnly = extractCoords('https://www.google.com/maps/@21.5,105.8,14z');
assert.strictEqual(viewportOnly.source, 'viewport');
assert.strictEqual(viewportOnly.lat, 21.5);

const integerViewport = extractCoords('https://www.google.com/maps/@21,105,14z');
assert.strictEqual(integerViewport.source, 'viewport');
assert.strictEqual(integerViewport.lat, 21);
assert.strictEqual(integerViewport.lng, 105);

const param = extractCoords('https://maps.apple.com/?ll=21.01,105.83&q=Hoan%20Kiem');
assert.strictEqual(param.source, 'param');
assert.strictEqual(extractPlaceName('https://maps.apple.com/?ll=21.01,105.83&q=Hoan%20Kiem'), 'Hoan Kiem');

const directions = extractCoords('https://www.google.com/maps/dir/?api=1&daddr=21,105');
assert.strictEqual(directions.source, 'param');
assert.strictEqual(directions.lat, 21);

const placePath = extractPlaceName('https://www.google.com/maps/place/Cafe+Giang/@21.0,105.8,17z');
assert.strictEqual(placePath, 'Cafe Giang');

const placeWithQuery = extractPlaceName('https://www.google.com/maps/place/Cafe+Giang?g_st=ic');
assert.strictEqual(placeWithQuery, 'Cafe Giang');

const raw = extractCoords('21.011967, 105.838405');
assert.strictEqual(raw.source, 'raw');

const integerRaw = extractCoords('21, 105');
assert.strictEqual(integerRaw.source, 'raw');
assert.strictEqual(integerRaw.lat, 21);
assert.strictEqual(integerRaw.lng, 105);

const urls = buildMapUrls(21.01, 105.83, 'Cafe Giang');
assert.ok(urls.appleUrl.includes('ll=21.01,105.83'));
assert.ok(urls.appleUrl.includes('q=Cafe%20Giang'));
assert.ok(urls.googleUrl.includes('query=21.01,105.83'));
assert.ok(!urls.googleUrl.includes('Cafe'));

assert.ok(isAppleMapsSource('https://apple.co/3abc'));
assert.ok(isAppleMapsSource('https://maps.apple.com/?ll=1,2'));
assert.ok(!isAppleMapsSource('https://maps.app.goo.gl/abc'));

assert.ok(hostnameAllowed('maps.app.goo.gl'));
assert.ok(hostnameAllowed('maps.apple.com'));
assert.ok(hostnameAllowed('apple.co'));
assert.ok(!hostnameAllowed('evil.example'));
assert.ok(isPrivateOrReservedIp('127.0.0.1'));
assert.ok(isPrivateOrReservedIp('169.254.169.254'));
assert.ok(isPrivateOrReservedIp('::1'));
assert.ok(!isPrivateOrReservedIp('8.8.8.8'));

parseHttpUrl('https://maps.app.goo.gl/abc');
assert.throws(() => parseHttpUrl('https://127.0.0.1:3000'), /known maps host/);
assert.throws(() => parseHttpUrl('https://evil.example/maps'), /Only Google Maps/);

console.log('extract tests passed');
