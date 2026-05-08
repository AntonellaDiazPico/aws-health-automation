import feedparser

FEED_URL = "https://status.aws.amazon.com/rss/all.rss"
LAST_SEEN_FILE = "last_seen.txt"

feed = feedparser.parse(FEED_URL)
if not feed.entries:
    raise SystemExit("ERROR: No entries found in feed.")

latest_id = feed.entries[0].id
with open(LAST_SEEN_FILE, "w") as f:
    f.write(latest_id)

print(f"Seeded last_seen.txt with: {latest_id}")
