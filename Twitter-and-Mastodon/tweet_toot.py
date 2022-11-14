# SPDX-FileCopyrightText: 2022 Kattni Rembor
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Parse an RSS feed and generate a string based on the content, and send that string as a message to
Twitter and Mastodon.

PREREQUISITES FOR RUNNING THIS CODE
Note: Prerequisites are also detailed in the README on GitHub.
1. You MUST acquire API access for both Twitter and Mastodon. Please check the documentation for
each platform for information on how to obtain the appropriate keys.
    For Twitter, this means you should obtain the following:
    * Twitter API key
    * Twitter API key secret
    * Twitter access token
    * Twitter access token secret
    * Twitter bearer token
    For Mastodon, this means you should obtain the following:
    * Mastodon access token

2. Once all six keys are obtained, they should be added to a keys.py file in the same directory as
this script, as strings assigned to the following list of variables.
    * TWITTER_API_KEY
    * TWITTER_API_KEY_SECRET
    * TWITTER_ACCESS_TOKEN
    * TWITTER_ACCESS_TOKEN_SECRET
    * TWITTER_BEARER_TOKEN
    * MASTODON_ACCESS_TOKEN
    For example, the first line in keys.py should look similar to the following:
    TWITTER_API_KEY = "yourtwitterapikeyhere"

3. Create an empty file named string_cache.txt in the same directory from which you plan to run
this script. The code checks for it and fails with instructions if you have not already done this
before running the script.

4. In the CUSTOMISATIONS section at the beginning of the code, update each of the variables to
your desired settings or content. Instructions for each included in the code comments.
"""

from pathlib import Path
import feedparser
import tweepy
import mastodon
from keys import (
    TWITTER_API_KEY,
    TWITTER_API_KEY_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_BEARER_TOKEN,
    MASTODON_ACCESS_TOKEN,
)

# ** CUSTOMISATIONS **
# Disable one or both of the platforms by setting the related variable to False. Defaults to True.
SEND_TO_TWITTER = True
SEND_TO_MASTODON = True

# Update to match your Mastodon server base URL. Defaults to "https://octodon.social".
mastodon_server_url = "https://octodon.social"

# Update this URL to match the RSS feed of your choice. Defaults to kattni.com feed.
feed = feedparser.parse("https://kattni.com/feeds/all.atom.xml")


# ** CODE **
# Set up for duplicate post checking.
# Creates a variable to use as this instance is included multiple times throughout this script.
string_cache = Path("string_cache.txt")

# If the file string_cache.txt does not exist...
if not string_cache.exists():
    # ...fail here with instructions to create the file.
    raise Exception(
        f"{string_cache} does not exist. "
        f"Create an empty file named {string_cache} in "
        f"the same directory as this script."
    )

# Hashtag generation.
# Creates an empty string to which to append tags.
tags_str = ""
# Try to parse "tags" out of the RSS feed.
try:
    # Loop through tags to obtain the tags.
    for tag_obj in feed["items"][0]["tags"]:
        # Filter out tags that are numeric (i.e. years). This was added as a workaround due to
        # an issue that causes inclusion of the current year as a tag even though it is not
        # explicitly included in the tag list.
        if not tag_obj["term"].isnumeric():
            # Append each tag to string with space and hashtag.
            tags_str = f"{tags_str} #{tag_obj['term']}"
    # Trim the leading space.
    tags_str = tags_str[1:]
# If there is no "tags" entry in the RSS feed, continue on to the next section.
except KeyError:
    pass

# Message content generation.
# Generate the message content from the parsed RSS feed.
message_template_string = (
    f"{feed['items'][0]['title']} {feed['items'][0]['links'][0]['href']} {tags_str}"
)

# Duplicate post check.
# Avoids sending duplicate messages by verifying that the message template string
# generated above is not identical to the last string sent using this script.
if string_cache.read_text() == message_template_string:
    raise Exception("Message template string has not been updated.")

# API Authentication.
# try/except used here because the default error is not clear as to why it failed.
try:
    # Authenticate to Twitter.
    client = tweepy.Client(
        TWITTER_BEARER_TOKEN,
        TWITTER_API_KEY,
        TWITTER_API_KEY_SECRET,
        TWITTER_ACCESS_TOKEN,
        TWITTER_ACCESS_TOKEN_SECRET,
    )
    # Attempts to access Twitter API to verify authentication.
    client.get_me()
# If Twitter authentication fails, except confusing error...
except tweepy.errors.Unauthorized:
    # ...and raise clearer one.
    raise Exception("Authentication failed. Check your keys.")

# try/except used here for consistency. The Mastodon authentication failure is clearer.
try:
    # Authenticate to Mastodon.
    mastodon = mastodon.Mastodon(
        access_token=MASTODON_ACCESS_TOKEN, api_base_url=mastodon_server_url
    )
    # Attempts to access Mastodon API to verify authentication.
    mastodon.me()
# If authentication fails, except Mastodon default error...
except mastodon.Mastodon.MastodonUnauthorizedError:
    # ...and raise the same as above.
    raise Exception("Authentication failed. Check your keys.")

# Send messages.
# If Twitter is enabled (True) above...
if SEND_TO_TWITTER:
    # Send the generated string as a message to Twitter.
    client.create_tweet(text=message_template_string)

# If Mastodon is enabled (True) above...
if SEND_TO_MASTODON:
    # Send the generated string as a message to Mastodon.
    mastodon.toot(message_template_string)

# Update string cache.
# Once both messages are sent successfully, update the content of string_cache.txt to the latest
# message template string for comparison the next time this script is run.
string_cache.write_text(message_template_string)
