"""
Script pentru actualizarea automata a feed-ului Instagram - IsisPharma
Ruleaza periodic prin GitHub Actions (vezi .github/workflows/update-feed.yml)

Nu contine tokenul in cod - acesta vine din variabilele de mediu (GitHub Secrets),
deci nu e niciodata vizibil public in repository sau pe site.
"""

import os
import json
import urllib.request
import urllib.error

ACCESS_TOKEN = os.environ["IG_ACCESS_TOKEN"]
IG_USER_ID = os.environ["IG_USER_ID"]
POST_COUNT = 12
OUTPUT_FILE = "posts.json"


def fetch_media():
    fields = "id,caption,media_type,media_url,thumbnail_url,permalink,timestamp"
    url = (
        f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
        f"?fields={fields}&limit={POST_COUNT}&access_token={ACCESS_TOKEN}"
    )
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Eroare HTTP {e.code}: {error_body}")
        raise
    return data.get("data", [])


def main():
    posts = fetch_media()
    output = {
        "updated_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "posts": posts,
    }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Salvate {len(posts)} postari in {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
