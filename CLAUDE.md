# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python script that polls the public AWS Health RSS feed (`status.aws.amazon.com`) and posts new events to a Slack channel via an incoming webhook. No AWS credentials required. Runs on a 15-minute GitHub Actions cron schedule.

## How It Works

1. Fetches the AWS status RSS feed using `feedparser`
2. Compares feed entries against the last-seen entry ID stored in `last_seen.txt`
3. Posts any new events to Slack via `requests` and an incoming webhook URL
4. Commits the updated `last_seen.txt` back to the repo to persist state between runs

## Dependencies

```
feedparser
requests
```

Install locally: `pip install feedparser requests`

## Running Locally

```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/... python check_health.py
```

`last_seen.txt` is read and written in the repo root. An empty or missing file causes all current feed entries to be treated as new on first run.

## GitHub Actions

The workflow in `.github/workflows/` triggers every 15 minutes. It requires a `SLACK_WEBHOOK_URL` secret set in the repository settings. After posting, it commits any change to `last_seen.txt` back to `main`.

## State Tracking

`last_seen.txt` holds the entry ID (or timestamp/link) of the most recently seen RSS item. It is committed by the Actions bot after each run — do not add it to `.gitignore`.
