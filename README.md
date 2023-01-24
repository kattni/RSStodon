# TwitteRSS
## Parse an RSS Feed and Post Content to Twitter and Mastodon

Thank you to @foamyguy for help with the `feedparser` code.

### Code usage
**If you have not already, please complete the prerequisites below before running the script.**

To use this example, from the directory containing the script file, simply run the following from command line:

```commandline
python rss_to_toot.py
```
Note: If Python 2 is your default version, you may need to modify the command to begin with `python3`.

### Prerequisites
1. You must have Python 3 installed on your computer, along with the `pip` installer. If you have not already done so, search for the instructions specific to your computer hardware and operating system.

2. Use `pip` to install the packages within the _requirements.txt_ file. From within the same directory as the _requirements.txt_ file, run the following:
    ```commandline
    pip install -r requirements.txt
    ```
   Note: If Python 3 is not your default version, you may have to modify the command to begin with `pip3`.
3. You must acquire API access for Mastodon. Please check the documentation for Mastodon for information on how to obtain the appropriate token.
   * For Mastodon, this means you should obtain the following:
     * Mastodon access token

4. Once the key is obtained, it should be added to a _keys.py_ file in the same directory as this script, as a string assigned to the following variable.
      * MASTODON_ACCESS_TOKEN

   For example, keys.py should contain something similar to the following:
   ```python
   MASTODON_ACCESS_TOKEN = "yourmastodonaccesstokenhere"
   ```

5. Create an empty file named _string_cache.txt_ in the same directory from which you plan to run this script. The code checks for it and fails with instructions if you have not already done this before running the script.

6. In the `** CUSTOMISATIONS **` section at the beginning of the code, update the variables to your desired settings or content. The customisable options are as follows:
    * Disable sending to Mastodon, by updating `True` shown on the following line to `False`. It defaults to `True` meaning sending is enabled by default.
      ```python
      SEND_TO_MASTODON = True
      ```
    * Update mastodon_server_url to your Mastodon server URL as a string. Defaults to `"https://octodon.social"`.
      ```python
      mastodon_server_url = "https://octodon.social"
      ```
    * Update the feed URL to match the URL of the RSS feed you intend to parse. Defaults to the kattni.com blog RSS feed.
      ```python
      feed = feedparser.parse("https://kattni.com/feeds/all.atom.xml")
      ```

Once you've completed the steps above, you're ready to run the script!
