const assert = require('assert');
const { extractCoords, extractPlaceName, buildMapUrls } = require('./extract');

const pinAndViewport = 'https://www.google.com/maps/@10.0,20.0,17z/data=!3d21.011967!4d105.838405';
const pin = extractCoords(pinAndViewport);
assert.strictEqual(pin.source, 'protobuf');
assert.strictEqual(pin.lat, 21.011967);
assert.strictEqual(pin.lng, 105.838405);

const viewportOnly = extractCoords('https://www.google.com/maps/@21.5,105.8,14z');
assert.strictEqual(viewportOnly.source, 'viewport');
assert.strictEqual(viewportOnly.lat, 21.5);

const param = extractCoords('https://maps.apple.com/?ll=21.01,105.83&q=Hoan%20Kiem');
assert.strictEqual(param.source, 'param');
assert.strictEqual(extractPlaceName('https://maps.apple.com/?ll=21.01,105.83&q=Hoan%20Kiem'), 'Hoan Kiem');

const placePath = extractPlaceName('https://www.google.com/maps/place/Cafe+Giang/@21.0,105.8,17z');
assert.strictEqual(placePath, 'Cafe Giang');

const raw = extractCoords('21.011967, 105.838405');
assert.strictEqual(raw.source, 'raw');

const urls = buildMapUrls(21.01, 105.83, 'Cafe Giang');
assert.ok(urls.appleUrl.includes('ll=21.01,105.83'));
assert.ok(urls.appleUrl.includes('q=Cafe%20Giang'));
assert.ok(urls.googleUrl.includes('query=21.01,105.83'));
assert.ok(!urls.googleUrl.includes('Cafe'));

console.log('extract tests passed');
