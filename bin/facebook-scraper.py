import argparse
import json
import warnings
from facebook_scraper import get_posts


# https://github.com/kevinzg/facebook-scraper
# https://github.com/bisguzar/twitter-scraper
class FacebookScraper:
    def silence_warning(self):
        # Suppresses the following 2 warnings.
        language_error = "/home/freetalk/.local/share/virtualenvs/vidhop-4Px9w5UP/lib/python3.10/site-packages/facebook_scraper/facebook_scraper.py:855: UserWarning: Facebook language detected as nl_BE - for best results, set to en_US"
        localize_error = "/home/freetalk/.local/share/virtualenvs/vidhop-4Px9w5UP/lib/python3.10/site-packages/dateparser/freshness_date_parser.py:76: PytzUsageWarning: The localize method is no longer necessary, as this time zone supports the fold attribute (PEP 495). For more details on migrating to a PEP 495-compliant implementation, see https://pytz-deprecation-shim.readthedocs.io/en/latest/migration.html; now = self.get_local_tz().localize(now)"
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore",
                                message="The localize method is no longer necessary, as this time zone supports the fold attribute")

    def fetch_post(self, url: str):
        self.silence_warning()
        posts = list(
            get_posts(
                post_urls=[url],
                options={"comments": True}
            )
        )
        post = posts[0]
        print(json.dumps(post, sort_keys=True, default=str))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Twitter Scraper.')
    parser.add_argument('-u', '--url', help='the url of the tweet', required=True)
    args = parser.parse_args()
    scraper = FacebookScraper()
    scraper.fetch_post(args.url)
