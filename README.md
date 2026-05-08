# aws-health-automation

Polls the public AWS Health RSS feed every 30 minutes and posts new events to a Slack channel. Runs on GitHub Actions — no AWS credentials required.

## How it works

- `check_health.py` fetches `status.aws.amazon.com/rss/all.rss`, compares entries against the last-seen ID in `last_seen.txt`, and posts any new events to Slack via an incoming webhook.
- After each run, `last_seen.txt` is committed back to the repo to persist state.