import argparse
import json
import warnings
import os
from facebook_scraper import get_posts


# https://github.com/kevinzg/facebook-scraper
class FacebookScraper:
    def should_redirect(self, url: str):
        if 'facebook.com/photo/?fbid' in url:
            return True
        else:
            return False

    def silence_warning(self):
        # Suppresses the following 2 warnings.
        user = os.getlogin()
        language_error = f"/home/{user}/.local/share/virtualenvs/vidhop-4Px9w5UP/lib/python3.10/site-packages/facebook_scraper/facebook_scraper.py:855: UserWarning: Facebook language detected as nl_BE - for best results, set to en_US"
        localize_error = f"/home/{user}/.local/share/virtualenvs/vidhop-4Px9w5UP/lib/python3.10/site-packages/dateparser/freshness_date_parser.py:76: PytzUsageWarning: The localize method is no longer necessary, as this time zone supports the fold attribute (PEP 495). For more details on migrating to a PEP 495-compliant implementation, see https://pytz-deprecation-shim.readthedocs.io/en/latest/migration.html; now = self.get_local_tz().localize(now)"
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", message="The localize method is no longer necessary, as this time zone supports the fold attribute")

    def fetch_post(self, url: str):
        self.silence_warning()
        posts = list(
            get_posts(
                post_urls=[url],
                options={"comments": True}
            )
        )
        post = posts[0]
        if self.should_redirect(url):
            post_url = post.get('post_url', None)
            self.fetch_post(post_url)
            return

        print(json.dumps(post, sort_keys=True, default=str))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Facebook Scraper.')
    parser.add_argument('-u', '--url', help='the url of the post', required=True)
    args = parser.parse_args()
    scraper = FacebookScraper()
    scraper.fetch_post(args.url)
