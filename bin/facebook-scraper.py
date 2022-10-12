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

    def convert_none_type(self, value):
        if value is None:
            return ""
        return value

    def convert_list_of_none_types(self, a_list):
        new_list = []
        for item in a_list:
            if item is None:
                item = ""
            if isinstance(item, list):
                self.convert_list_of_none_types(item)
            new_list.append(item)
        return new_list

    def convert_datetimes_to_strings_in_dict_recursive(self, d) -> dict:
        updated_dict = {}
        for k, v in d.items():
            if isinstance(v, dict):
                updated_dict[k] = self.convert_datetimes_to_strings_in_dict_recursive(v)
            elif isinstance(v, list):
                updated_dict[k] = self.convert_list_of_none_types(v)
            else:
                if isinstance(v, datetime.date):
                    updated_dict[k] = v.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    updated_dict[k] = self.convert_none_type(v)
        return updated_dict

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
    def create_json_post(self, post):
        return self.convert_datetimes_to_strings_in_dict_recursive(post)

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
        sanitized_post = self.convert_datetimes_to_strings_in_dict_recursive(post)
        # sanitized_post = self.create_json_post(post)
        json_post = json.dumps(sanitized_post)
        print(json_post)
        return json_post


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Twitter Scraper.')
    parser.add_argument('-u', '--url', help='the url of the tweet', required=True)
    args = parser.parse_args()
    scraper = FacebookScraper()
    scraper.fetch_post(args.url)
