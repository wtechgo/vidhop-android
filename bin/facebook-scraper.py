import argparse
import json
import warnings
import datetime
from facebook_scraper import get_posts


# https://github.com/kevinzg/facebook-scraper
# https://github.com/bisguzar/twitter-scraper
class FacebookScraper:
    def value_for_key(self, post: dict, key: str):
        try:
            if key in 'time' or key in 'fetched_time':
                return datetime.datetime.strftime(post[key], "%Y-%m-%d %H:%M:%S")
            value = post[key]
            if value is None:
                return ""
            return value
        except KeyError:
            return ""
        except TypeError:
            return ""

    def stringify_comments_full(self, post):
        comments = {
            'comment_id': self.value_for_key(post, 'comment_id'),
            'comment_url': self.value_for_key(post, 'comment_url'),
            'commenter_id': self.value_for_key(post, 'commenter_id'),
            'commenter_url': self.value_for_key(post, 'commenter_url'),
            'commenter_name': self.value_for_key(post, 'commenter_name'),
            'commenter_meta': self.value_for_key(post, 'commenter_meta'),
            'comment_text': self.value_for_key(post, 'comment_text'),
            'comment_time': self.value_for_key(post, 'comment_time'),
            'comment_image': self.value_for_key(post, 'comment_image'),
            'comment_reactors': self.value_for_key(post, 'comment_reactors'),
            'comment_reactions': self.value_for_key(post, 'comment_reactions'),
            'comment_reaction_count': self.value_for_key(post, 'comment_reaction_count'),
            'replies': self.value_for_key(post, 'replies'),
        }
        return comments

    # post = next(posts)
    def create_json_post(self, post: dict):
        # print({post['time']})
        # print({post['fetched_time']})

        json_post = {
            'original_request_url': self.value_for_key(post, 'original_request_url'),
            'post_url': self.value_for_key(post, 'post_url'), 'post_id': self.value_for_key(post, 'post_id'),
            'text': self.value_for_key(post, 'text'), 'post_text': self.value_for_key(post, 'post_text'),
            'shared_text': self.value_for_key(post, 'shared_text'),
            'original_text': self.value_for_key(post, 'original_text'),
            'time': self.value_for_key(post, 'time'), 'timestamp': self.value_for_key(post, 'timestamp'),
            'image': self.value_for_key(post, 'image'),
            'image_lowquality': self.value_for_key(post, 'image_lowquality'),
            'images': self.value_for_key(post, 'images'),
            'images_description': self.value_for_key(post, 'images_description'),
            'images_lowquality': self.value_for_key(post, 'images_lowquality'),
            'images_lowquality_description': self.value_for_key(post, 'images_lowquality_description'),
            'video': self.value_for_key(post, 'video'),
            'video_duration_seconds': self.value_for_key(post, 'video_duration_seconds'),
            'video_height': self.value_for_key(post, 'video_height'),
            'video_id': self.value_for_key(post, 'video_id'),
            'video_quality': self.value_for_key(post, 'video_quality'),
            'video_size_MB': self.value_for_key(post, 'video_size_MB'),
            'video_thumbnail': self.value_for_key(post, 'video_thumbnail'),
            'video_watches': self.value_for_key(post, 'video_watches'),
            'video_width': self.value_for_key(post, 'video_width'), 'likes': self.value_for_key(post, 'likes'),
            'comments': self.value_for_key(post, 'comments'), 'shares': self.value_for_key(post, 'shares'),
            'link': self.value_for_key(post, 'link'), 'links': self.value_for_key(post, 'links'),
            'user_id': self.value_for_key(post, 'user_id'), 'username': self.value_for_key(post, 'username'),
            'user_url': self.value_for_key(post, 'user_url'), 'is_live': self.value_for_key(post, 'is_live'),
            'factcheck': self.value_for_key(post, 'factcheck'),
            'shared_post_id': self.value_for_key(post, 'shared_post_id'),
            'shared_time': self.value_for_key(post, 'shared_time'),
            'shared_user_id': self.value_for_key(post, 'shared_user_id'),
            'shared_username': self.value_for_key(post, 'shared_username'),
            'shared_post_url': self.value_for_key(post, 'shared_post_url'),
            'available': self.value_for_key(post, 'available'),
            'comments_full': self.stringify_comments_full(post['comments_full']),  # important
            'reactors': self.value_for_key(post, 'reactors'),
            'w3_fb_url': self.value_for_key(post, 'w3_fb_url'),
            'reactions': self.value_for_key(post, 'reactions'),
            'reaction_count': self.value_for_key(post, 'reaction_count'),
            'with': self.value_for_key(post, 'with'), 'page_id': self.value_for_key(post, 'page_id'),
            'sharers': self.value_for_key(post, 'sharers'), 'image_id': self.value_for_key(post, 'image_id'),
            'image_ids': self.value_for_key(post, 'image_ids')}

        return json_post

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
        post_json = self.create_json_post(posts[0])
        print(json.dumps(post_json))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Twitter Scraper.')
    parser.add_argument('-u', '--url', help='the url of the tweet', required=True)
    args = parser.parse_args()
    scraper = FacebookScraper()
    scraper.fetch_post(args.url)
