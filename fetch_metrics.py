import requests

# Repository details
owner = "coozila"
repo = "memcached-cluster"
url = f"https://api.github.com/repos/{owner}/{repo}"

# Get release data
releases_url = f"{url}/releases"
releases_response = requests.get(releases_url)
releases = releases_response.json()

downloads = {}
for release in releases:
    downloads[release['tag_name']] = sum(asset.get('download_count', 0) for asset in release.get('assets', []))

# Get branch data
branches_url = f"{url}/branches"
branches_response = requests.get(branches_url)
branches = branches_response.json()

branch_downloads = {branch['name']: 0 for branch in branches}

# Get open issues data
issues_url = f"{url}/issues"
issues_response = requests.get(issues_url)
issues = issues_response.json()

open_issues_count = sum(1 for issue in issues if 'pull_request' not in issue)

# Final JSON structure
metrics = {
    "open_issues": open_issues_count,
    "downloads": downloads,
    "branches": branch_downloads
}

print(metrics)
