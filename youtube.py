import re
import urllib.request
import json
import urllib.parse
import ssl
from mumo_module import MumoModule

class youtube(MumoModule):
    default_config = {'youtube': ()}

    def __init__(self, name, manager, configuration=None):
        MumoModule.__init__(self, name, manager, configuration)
        self.murmur = manager.getMurmurModule()

    def connected(self):
        manager = self.manager()
        self.log().debug("Registering YouTube Fail-Safe module")
        manager.subscribeServerCallbacks(self, manager.SERVERS_ALL)

    def disconnected(self):
        pass

    def sendMessage(self, server, user, message, msg):
        if message.channels:
            server.sendMessageChannel(user.channel, False, msg)
        else:
            server.sendMessage(user.session, msg)

    def userTextMessage(self, server, user, message, current=None):
        # 1. Clean rich HTML formatting out of the message
        clean_text = re.sub(r'<[^>]*>', ' ', message.text)
        
        # 2. Grab the 11-digit YouTube video identifier
        yt_regex = r'(?:v=|/shorts/|youtu\.be/)([a-zA-Z0-9_-]{11})'
        matches = re.findall(yt_regex, clean_text)
        
        if matches:
            for video_id in set(matches):
                video_title = None
                target_url = f"https://www.youtube.com/watch?v={video_id}"
                
                # Global browser headers to resemble a human user
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5'
                }
                context = ssl._create_unverified_context()

                # METHOD 1: Try the OEmbed JSON Endpoint
                try:
                    oembed_url = f"https://youtube.com{urllib.parse.quote(target_url)}&format=json"
                    req = urllib.request.Request(oembed_url, headers=headers)
                    with urllib.request.urlopen(req, context=context, timeout=4) as response:
                        data = json.loads(response.read().decode('utf-8'))
                        video_title = data.get('title')
                except Exception:
                    pass # Silently proceed to Method 2 fallback if oEmbed limits us

                # METHOD 2: Fallback Web Scraper (Scans raw HTML for the <title> tag)
                if not video_title:
                    try:
                        req = urllib.request.Request(target_url, headers=headers)
                        with urllib.request.urlopen(req, context=context, timeout=4) as response:
                            html_content = response.read().decode('utf-8', errors='ignore')
                            # Match <title>Title Text - YouTube</title>
                            title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
                            if title_match:
                                raw_title = title_match.group(1)
                                # Strip away the trailing " - YouTube" brand text
                                video_title = re.sub(r'\s*-\s*YouTube$', '', raw_title, flags=re.IGNORECASE)
                    except Exception as fallback_error:
                        # Print the explicit system exception mapping type
                        self.sendMessage(server, user, message, f"⚠️ <b>Connection Error:</b> {repr(fallback_error)}")
                        return

                # 3. Deliver the final parsed title output to the channel
                if video_title:
                    # Clean up common HTML entities like &amp; or &#39;
                    video_title = video_title.replace('&amp;', '&').replace('&#39;', "'").replace('&quot;', '"')
                    self.sendMessage(server, user, message, f"📺 <b>YouTube:</b> {video_title}")
                else:
                    self.sendMessage(server, user, message, "⚠️ <b>Error:</b> Video found but title could not be extracted.")

    def userConnected(self, server, state, context=None): pass
    def userDisconnected(self, server, state, context=None): pass
    def userStateChanged(self, server, state, context=None): pass
    def channelCreated(self, server, state, context=None): pass
    def channelRemoved(self, server, state, context=None): pass
    def channelStateChanged(self, server, state, context=None): pass
