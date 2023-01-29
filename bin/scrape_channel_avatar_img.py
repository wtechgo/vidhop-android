import argparse
import sys
import textwrap
import os
import json
from selenium import webdriver
import requests
from PIL import Image
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def main(channel_url, channel_name, channels_meta_dir, is_playlist=False):
    platforms = [
        "bitchute.com",
        "odysee.com",
        "youtube.com",
        "youtu.be",
    ]
    platform = None
    for p in platforms:
        if p in channel_url:
            platform = p
    if platform not in platforms:
        sys.exit(f"avatar scraper only supported for YouTube, Odysee & BitChute")

    def scrape_avatar_img_url(channel_URL):  # param is channel URL
        if "bitchute.com" in channel_URL:
            html = requests.get(channel_URL).text
            soup = BeautifulSoup(html, 'html.parser')
            link = soup.find(id="fileupload-large-icon-2")["data-src"]
            return link
        if "odysee.com" in channel_URL:
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-logging")  # attempt to replace service_log_path, does nothing
            driver = webdriver.Firefox(service_log_path=os.path.devnull, options=options)  # service_log_path deprecated
            driver.implicitly_wait(10)

            driver.get(channel_URL)
            link = driver.find_element(By.CSS_SELECTOR, 'div.channel__primary-info img.channel-thumbnail__custom').get_attribute('src')
            driver.close()
            return link
        if "youtube.com" in channel_URL or "youtu.be" in channel_URL:
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-logging")  # attempt to replace service_log_path, does nothing
            driver = webdriver.Firefox(service_log_path=os.path.devnull, options=options)  # service_log_path deprecated
            driver.implicitly_wait(10)

            driver.get(channel_URL)
            driver.find_element(By.CSS_SELECTOR, 'form button').click()
            link = driver.find_element(By.XPATH, "//div[@id='channel-header']//img").get_attribute("src")
            driver.close()
            return link

    img_url = scrape_avatar_img_url(channel_url)
    print(f"channel name is {channel_name}")
    print(f"channel url is {channel_url}")
    print(f"channel platform is {platform}")
    print(f"avatar image src is {img_url}")

    # Save image to disk.
    img = Image.open(requests.get(img_url, stream=True).raw)
    rel_path_avatar_img = f"/{channel_name}/{platform}/avatar_picture.{img.format.lower()}"  # for avatar json
    if is_playlist:
        rel_path_avatar_img = f"/{channel_name}/{channel_name}.{img.format.lower()}"  # for avatar json
    abs_path_avatar_img = f"{channels_meta_dir}{rel_path_avatar_img}"
    os.makedirs(os.path.dirname(abs_path_avatar_img), exist_ok=True)
    print(f"image save path is {abs_path_avatar_img}")

    img.save(abs_path_avatar_img)
    print("channel avatar picture saved !")

    # Save avatar data to JSON file.
    channel_data = {
        "channel_thumbnail_path": rel_path_avatar_img,
        "channel_thumbnail_url": img_url,
        "platform": platform
    }

    avatar_json_path = f"{channels_meta_dir}/{channel_name}/{platform}/avatar_data.json"
    if is_playlist:
        avatar_json_path = f"{channels_meta_dir}/{channel_name}/avatar_data.json"
    print(f"avatar data json path: {avatar_json_path}")
    print(f"avatar json data: {channel_data}")

    with open(avatar_json_path, 'w', encoding='utf-8') as f:
        json.dump(channel_data, f, ensure_ascii=False, indent=4)
    print(f"Saved avatar_data.json !")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Video channel profile picture scraper.',
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent('''\
             additional information:
                 Scrapes and save the profile picture of a channel
                 in $channels_meta_dir/$name/$name.jpg.
                 Useful as an addition to e.g. yt-dlp.
                 Example:
                    Example:
                    python scrape_channel_avatar_img.py --channel-url "https://www.bitchute.com/channel/ZcpM80EVcYa7/" --channel-name "WT" --channels-meta-dir $(pwd)
             '''))
    parser.add_argument('-u', '--channel-url', help='the url of the channel', required=True)
    parser.add_argument('-n', '--channel-name', help='name of the channel', required=True)
    parser.add_argument('-d', '--channels-meta-dir', help='channels metadata directory', required=True)
    parser.add_argument('-p', '--is-playlist', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    channel_url, channel_name, channels_meta_dir, is_playlist = args.channel_url, args.channel_name, args.channels_meta_dir, args.is_playlist
    # Arguments configuration done.
    main(channel_url, channel_name, channels_meta_dir, is_playlist)
