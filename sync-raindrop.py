#!/usr/bin/env python3
"""Run locally to sync Raindrop links to links.json. Reads from .env."""

import json, os, urllib.request, datetime

# Load .env
if os.path.exists('.env'):
    with open('.env') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

token = os.environ.get('RAINDROP_TOKEN', '')
collection_id = os.environ.get('RAINDROP_COLLECTION_ID', '')

if not token or not collection_id:
    print("Error: RAINDROP_TOKEN and RAINDROP_COLLECTION_ID must be set in .env")
    exit(1)

req = urllib.request.Request(
    f'https://api.raindrop.io/rest/v1/raindrops/{collection_id}?perpage=50&sort=-created',
    headers={'Authorization': f'Bearer {token}'}
)

with urllib.request.urlopen(req) as res:
    data = json.loads(res.read())

links = [{
    'title': item['title'],
    'url': item['link'],
    'excerpt': item.get('excerpt', ''),
    'tags': item.get('tags', []),
    'domain': item.get('domain', ''),
    'date': item['created']
} for item in data['items']]

output = {
    'updated': datetime.datetime.utcnow().isoformat() + 'Z',
    'links': links
}

with open('links.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"Done — wrote {len(links)} links to links.json")
