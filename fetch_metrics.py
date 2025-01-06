import requests
import json

# GitHub repository details
owner = "coozila"
repo = "memcached-cluster"
url = f"https://api.github.com/repos/{owner}/{repo}"

# Fetch release data for download counts
releases_url = f"{url}/releases"
releases_response = requests.get(releases_url)
releases = releases_response.json()

downloads_per_release = {}
total_downloads = 0

# Calculate downloads per release and total downloads
for release in releases:
    # Verifică dacă release-ul are assets
    if 'assets' in release and release.get('tag_name') == "1.0.0":  # Use only the existing tag
        download_count = sum(asset.get('download_count', 0) for asset in release['assets'])
        downloads_per_release[release['tag_name']] = download_count
        total_downloads += download_count

# Fetch repository data
repo_response = requests.get(url)
repo_data = repo_response.json()

# Extract required metrics
metrics = {
    'open_issues': repo_data.get('open_issues_count', 0),
    'downloads': downloads_per_release,  # Include downloads for each release
    'total_downloads': total_downloads,    # Add total downloads
    'branches': {
        'dev': {
            'downloads': 0  # You can update this if needed
        }
    }
}

# Save metrics to JSON file
with open('metrics.json', 'w') as file:
    json.dump(metrics, file, indent=4)

print(f"Metrics: {metrics}")
