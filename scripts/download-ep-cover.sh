#!/bin/bash
# Run this locally to download the Eclectic Polymath cover art from Spotify
# Usage: bash scripts/download-ep-cover.sh

CLIENT_ID="${SPOTIFY_CLIENT_ID:-305dc054851a42d09c194cdb04e19c07}"
CLIENT_SECRET="${SPOTIFY_CLIENT_SECRET:-60142a5ef9e54ca19ae0cd80fd15bb7c}"
SHOW_ID="3dlagzJ0jiWLTB9mF3y069"
OUT="Images/Podcasts/eclectic-polymath-cover.jpg"

TOKEN=$(curl -s -X POST "https://accounts.spotify.com/api/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -u "${CLIENT_ID}:${CLIENT_SECRET}" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

IMAGE_URL=$(curl -s "https://api.spotify.com/v1/shows/${SHOW_ID}" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -c "import sys,json; imgs=json.load(sys.stdin)['images']; print(sorted(imgs,key=lambda x:-x['width'])[0]['url'])")

echo "Downloading cover from: $IMAGE_URL"
curl -s -L "$IMAGE_URL" -o "$OUT"
echo "Saved to $OUT"
