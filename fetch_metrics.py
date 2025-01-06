import requests
import json

# Detalii despre repository
owner = "coozila"
repo = "memcached-cluster"
url = f"https://api.github.com/repos/{owner}/{repo}"

# Obține date despre repository
response = requests.get(url)
data = response.json()

# Initializează metricile
metrics = {
    'open_issues': data.get('open_issues_count', 0),
    'downloads': 0,  # Aceasta va fi calculată din releases
    'releases': {},
    'tags': {},
    'branches': {},
}

# Obține date despre release-uri
releases_url = f"{url}/releases"
releases_response = requests.get(releases_url)
releases = releases_response.json()

for release in releases:
    download_count = sum(asset.get('download_count', 0) for asset in release.get('assets', []))
    metrics['releases'][release['tag_name']] = download_count

# Obține date despre tag-uri
tags_url = f"{url}/tags"
tags_response = requests.get(tags_url)
tags = tags_response.json()

for tag in tags:
    metrics['tags'][tag['name']] = 0  # Inițializat cu 0, pentru a reflecta statisticile dorite

# Obține date despre branch-uri
branches_url = f"{url}/branches"
branches_response = requests.get(branches_url)
branches = branches_response.json()

for branch in branches:
    metrics['branches'][branch['name']] = {
        'commits': branch['commit']['commit']['message'],  # Optional: mesajul ultimului commit
        'downloads': 0  # Inițializat la 0, deoarece GitHub nu urmărește descărcările aici
    }

# Salvează metricile în fișier JSON
with open('metrics.json', 'w') as file:
    json.dump(metrics, file, indent=4)

print(f"Metrics: {metrics}")
