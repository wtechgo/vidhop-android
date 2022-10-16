import argparse
import json

import snscrape.modules.twitter as sntwitter
from snscrape.base import ScraperException


class TwitterScraper:
    def extract_id_from_url(self, url: str) -> str:
        if url.find("twitter.com") == -1:
            raise ValueError("not a twitter url")
        tweet_id = url.split("?")[0].split('status/')[1]
        return tweet_id

    def fetch_tweet(self, url: str) -> dict:
        tweet_id = self.extract_id_from_url(url)
        try:
            gen = sntwitter.TwitterTweetScraper(
                tweetId=tweet_id,
                mode=sntwitter.TwitterTweetScraperMode.SINGLE
            ).get_items()
            tweet = list(gen)[0]
            return {
                # All SnScrape attributes.
                "url": tweet.url,
                "date": tweet.date,
                "content": tweet.content,
                "renderedContent": tweet.renderedContent,
                "id": tweet.id,
                "username": tweet.user.username,
                "user": tweet.user,
                "outlinks": tweet.outlinks,
                "tcooutlinks": tweet.tcooutlinks,
                "replyCount": tweet.replyCount,
                "retweetCount": tweet.retweetCount,
                "likeCount": tweet.likeCount,
                "quoteCount": tweet.quoteCount,
                "conversationId": tweet.conversationId,
                "lang": tweet.lang,
                "source": tweet.source,
                "media": tweet.media,
                "retweetedTweet": tweet.retweetedTweet,
                "quotedTweet": tweet.quotedTweet,
                "mentionedUsers": tweet.mentionedUsers,
            }
        except ScraperException:
            print(f"Error: Scrape for url '{url}' failed")
            return {}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Twitter Scraper.')
    parser.add_argument('-u', '--url', help='the url of the tweet', required=True)
    args = parser.parse_args()
    scraper = TwitterScraper()
    result = scraper.fetch_tweet(args.url)
    json = json.dumps(result, default=str)
    print(json)
