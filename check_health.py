import os
import sys
import feedparser
import requests

FEED_URL = "https://status.aws.amazon.com/rss/all.rss"
LAST_SEEN_FILE = "last_seen.txt"
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
AWS_DASHBOARD_URL = "https://health.aws.amazon.com/health/status"
SUMMARY_MAX_CHARS = 500


def load_last_seen():
    try:
        with open(LAST_SEEN_FILE) as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def save_last_seen(entry_id):
    with open(LAST_SEEN_FILE, "w") as f:
        f.write(entry_id)


def post_to_slack(title, summary, link):
    truncated = summary[:SUMMARY_MAX_CHARS] + "…" if len(summary) > SUMMARY_MAX_CHARS else summary
    payload = {
        "text": f"*AWS Health Event*: {title}\n{truncated}\n<{link}|View on AWS Health Dashboard>"
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
    response.raise_for_status()


def main():
    if not SLACK_WEBHOOK_URL:
        print("ERROR: SLACK_WEBHOOK_URL environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    feed = feedparser.parse(FEED_URL)
    if not feed.entries:
        print("No entries found in feed.")
        return

    last_seen = load_last_seen()

    # Feed entries are newest-first; collect new ones before the last seen ID
    new_entries = []
    for entry in feed.entries:
        if entry.id == last_seen:
            break
        new_entries.append(entry)

    if not new_entries:
        print("No new events.")
        return

    # Post oldest-first so Slack shows them in chronological order
    for entry in reversed(new_entries):
        summary = entry.get("summary", "No details available.")
        # feedparser may return HTML; strip tags with a simple approach
        summary = summary.replace("<br>", "\n").replace("<br/>", "\n")
        import re
        summary = re.sub(r"<[^>]+>", "", summary).strip()
        print(f"Posting: {entry.title}")
        post_to_slack(entry.title, summary, entry.link)

    save_last_seen(feed.entries[0].id)
    print(f"Done. Last seen updated to: {feed.entries[0].id}")


if __name__ == "__main__":
    main()
