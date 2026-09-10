# Map Bridge • Google to Apple Maps

Paste a Google Maps link (or raw coordinates) and open the same pin in Apple Maps.

The backend follows short/share URLs, extracts latitude and longitude, and builds an Apple Maps URL with a 1:1 coordinate match.

## Run locally

Requires Node.js.

```bash
npm install
node server.js
```

Then open [http://localhost:3000](http://localhost:3000).

## Usage

1. Paste a Google Maps URL or `lat, lng` into the input.
2. Click **Convert to Apple Maps**.
3. Open the resolved pin in Apple Maps.

Supported inputs:

- Google Maps share / short links (`maps.app.goo.gl`, `goo.gl/maps`, …)
- Full Google Maps URLs with `@lat,lng` or dropped-pin data
- Query params such as `q=lat,lng` or `ll=lat,lng`
- Raw coordinates, e.g. `21.011967, 105.838405`

## How it works

`POST /api/resolve` accepts `{ "url": "..." }`.

1. If the input is already `lat, lng`, it returns those coordinates immediately.
2. Otherwise it fetches the URL (following redirects) and scans the redirect chain plus HTML for coordinates.
3. On success it returns `lat`, `lng`, and `appleUrl` (`https://maps.apple.com/?ll=…&q=…`).

The UI is a static page served by Express from `index.html`.
