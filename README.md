# Installation

Python 3.X required

Libraries :
- dotenv
- feedparser
- pytz
- urllib

# Configuration

1. Add a .env file with 2 variables :
  - WEBHOOK_URL="your_webhook_url"
  - RSS_URL="your_rss_url"
2. Change the variables' name
3. Add a new task on crontab

crontab -e
* * * * * /usr/bin/python3 /path/to/feed.py 2> /path/to/feed.log

It will automatically change the feed.

# Example

<img width="1064" alt="Screenshot 2024-05-16 at 22 36 11" src="https://github.com/RickHolaaa/Feed-Parser/assets/66788498/584b32a4-57c9-459a-8c15-77ecf3a0d2e9">
