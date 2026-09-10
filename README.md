# Map Bridge • Google ⇆ Apple Maps

Paste a Google Maps or Apple Maps link (or raw coordinates) and open the same pin in the other app.

The backend follows short/share URLs, extracts latitude and longitude, and builds a 1:1 coordinate match for the destination map.

## Run locally

Requires Node.js.

```bash
npm install
npm start
```

Then open [http://localhost:3000](http://localhost:3000).

```bash
npm test
```

## Usage

1. Paste a Google Maps URL, Apple Maps URL, or `lat, lng`.
2. Click **Convert Link**.
3. Open the pin in the other maps app.

Supported inputs:

- Google Maps share / short links (`maps.app.goo.gl`, `goo.gl/maps`, …)
- Full Google Maps URLs with `@lat,lng` or dropped-pin data (`!3d…!4d…`)
- Apple Maps URLs (`maps.apple.com` with `ll=` / `q=`)
- Query params such as `q=lat,lng` or `ll=lat,lng`
- Raw coordinates, e.g. `21.011967, 105.838405`

Dropped pins (`!3d!4d`) are preferred over the map camera (`@lat,lng`), so the converted pin matches the place, not the viewport.

## How it works

`POST /api/resolve` accepts `{ "url": "..." }`.

1. Parse coordinates from the pasted text when possible.
2. If the input is an `http(s)` URL and the pin is missing (or only a viewport), fetch the link (following redirects) and scan the redirect chain plus HTML.
3. Detect Apple vs Google from the pasted URL, then return the opposite `targetUrl`.
4. On success: `lat`, `lng`, optional `name`, `appleUrl`, `googleUrl`, and `targetUrl`.

Apple Maps URLs use `ll` for the pin and `q` for the label. Google Maps URLs always use `query=lat,lng` so a place name cannot send Search to a different result.

`GET /api/health` returns `{ "ok": true }` for the iOS client.

## iOS app

`ios/MapBridge` is a companion app (iPhone, share extension, watch). Debug builds call `http://127.0.0.1:3000`. Set `MAPBRIDGE_API_BASE_URL` in `ios/MapBridge/Config/Release.xcconfig` before a Release build.
