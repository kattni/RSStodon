# SPDX-FileCopyrightText: 2022 Kattni Rembor
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Parse an RSS feed and generate a string based on the content, and send that string as a message to
Mastodon.

Thank you to @foamyguy for help with the `feedparser` code.

PREREQUISITES FOR RUNNING THIS CODE
Note: Prerequisites are also detailed in the README on GitHub.
1. You MUST acquire API access to Mastodon. Please check the documentation for
the Mastodon API for information on how to obtain the appropriate keys.
    This means you should obtain the following:
    * Mastodon access token

2. Once your access token is obtained, it should be added to a keys.py file in the same directory
as this script, as a string assigned to the following variable.
    * MASTODON_ACCESS_TOKEN
    For example, keys.py should contain a line similar to the following:
    MASTODON_ACCESS_TOKEN = "yourmastodonaccesstokenhere"

3. Create an empty file named string_cache.txt in the same directory from which you plan to run
this script. The code checks for it and fails with instructions if you have not already done this
before running the script.

4. In the CUSTOMISATIONS section at the beginning of the code, update the variable to
your desired setting or content. Instructions for each included in the code comments.
"""

from pathlib import Path
import feedparser
import mastodon
from keys import (
    MASTODON_ACCESS_TOKEN,
)

# ** CUSTOMISATIONS **
# Disable sending to Mastodon by setting the variable to False. Defaults to True.
SEND_TO_MASTODON = True

# Update to match your Mastodon server base URL. Defaults to "https://octodon.social".
MASTODON_SERVER_URL = "https://octodon.social"

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
TAGS_STRING = ""
# Try to parse "tags" out of the RSS feed.
try:
    # Loop through tags to obtain the tags.
    for tag_obj in feed["items"][0]["tags"]:
        # Filter out tags that are numeric (i.e. years). This was added as a workaround due to
        # an issue that causes inclusion of the current year as a tag even though it is not
        # explicitly included in the tag list.
        if not tag_obj["term"].isnumeric():
            # Append each tag to string with space and hashtag.
            TAGS_STRING = f"{TAGS_STRING} #{tag_obj['term']}"
    # Trim the leading space.
    TAGS_STRING = TAGS_STRING[1:]
# If there is no "tags" entry in the RSS feed, continue on to the next section.
except KeyError:
    pass

# Message content generation.
# Generate the message content from the parsed RSS feed.
message_template_string = (
    f"{feed['items'][0]['title']} {feed['items'][0]['links'][0]['href']} {TAGS_STRING}"
)

# Duplicate post check.
# Avoids sending duplicate messages by verifying that the message template string
# generated above is not identical to the last string sent using this script.
if string_cache.read_text(encoding="utf-8") == message_template_string:
    raise Exception("Message template string has not been updated.")

# API Authentication.
# Authenticate to Mastodon.
mastodon = mastodon.Mastodon(
    access_token=MASTODON_ACCESS_TOKEN, api_base_url=MASTODON_SERVER_URL
)
# Attempts to access Mastodon API to verify authentication.
mastodon.me()
# If authentication fails, you'll receive an error here. Verify your access token
# and URL are correct if this happens.


# Send messages.
# If Mastodon is enabled (True) above...
if SEND_TO_MASTODON:
    # Send the generated string as a message to Mastodon.
    mastodon.toot(message_template_string)

# Update string cache.
# Once the message is sent successfully, update the content of string_cache.txt to the latest
# message template string for comparison the next time this script is run.
string_cache.write_text(message_template_string, encoding="utf-8")
