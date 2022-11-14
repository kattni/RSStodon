# TwitteRSS
## Parse an RSS Feed and Post Content to Twitter and Mastodon

Thank you to @foamyguy for help with the `feedparser` code.

### Code usage
**If you have not already, please complete the prerequisites below before running the script.**

To use this example, from the directory containing the script file, simply run the following from command line:

```commandline
python tweet_toot.py
```
Note: If Python 2 is your default version, you may need to modify the command to begin with `python3`.

### Prerequisites
1. You must have Python 3 installed on your computer, along with the `pip` installer. If you have not already done so, search for the instructions specific to your computer hardware and operating system.

2. Use `pip` to install the packages within the _requirements.txt_ file. From within the same directory as the _requirements.txt_ file, run the following:
    ```commandline
    pip install -r requirements.txt
    ```
   Note: If Python 3 is not your default version, you may have to modify the command to begin with `pip3`.
3. You must acquire API access for both Twitter and Mastodon. Please check the documentation for each platform for information on how to obtain the appropriate keys.
   * For Twitter, this means you should obtain the following:
     * Twitter API key
     * Twitter API key secret
     * Twitter access token
     * Twitter access token secret
     * Twitter bearer token

   * For Mastodon, this means you should obtain the following:
     * Mastodon access token

4. Once all six keys are obtained, they should be added to a _keys.py_ file in the same directory as this script, as strings assigned to the following list of variables.
      * TWITTER_API_KEY
      * TWITTER_API_KEY_SECRET
      * TWITTER_ACCESS_TOKEN
      * TWITTER_ACCESS_TOKEN_SECRET
      * TWITTER_BEARER_TOKEN
      * MASTODON_ACCESS_TOKEN

   For example, the first line in keys.py should look similar to the following:
   ```python
   TWITTER_API_KEY = "yourtwitterapikeyhere"
   ```

5. Create an empty file named _string_cache.txt_ in the same directory from which you plan to run this script. The code checks for it and fails with instructions if you have not already done this before running the script.

6. In the `** CUSTOMISATIONS **` section at the beginning of the code, update each of the variables to your desired settings or content. The customisable options are as follows:
    * Disable one or both social media platforms from sending, by updating `True` on one or both of the following lines to `False`. Both default to `True` meaning both are enabled by default.
      ```python
      SEND_TO_TWITTER = True
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
