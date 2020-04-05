import numpy as np
from bs4 import BeautifulSoup
import random
import json
import pandas as pd
import requests
import argparse
class Instagram:

    def __init__(self, username):
        self.username = username
        
        self.scrape_profile()


    def __repr__(self):
        return f"Current Username: {self.username}"

    def __str__(self):
        return f"Current Username: {self.username}"

    def __getitem__(self, i):
        return self.profile_data[i]


    def scrape_profile(self):
        """
        This is the main scrape which takes the profile data retrieved and saves it into profile_data
        :params: None
        :return: profile data
        """
        # Get the html data with the requests module
        r = requests.get(f'http://instagram.com/{self.username}')
        
        soup = BeautifulSoup(r.text, 'html.parser')
        # Find the tags that hold the data we want to parse
        general_data = soup.find_all('meta', attrs={'property': 'og:description'})
        more_data = soup.find_all('script', attrs={'type': 'text/javascript'})
        description = soup.find('script', attrs={'type': 'application/ld+json'})
        # Try to parse the content -- if it fails then the program exits
        try:
            text = general_data[0].get('content').split()
            self.description = json.loads(description.get_text())
            self.profile_meta = json.loads(more_data[3].get_text()[21:].strip(';'))

        except:
            
            return 1
        self.profile_data = {"Username": self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['username'],
                             "Profile name": self.description['name'],
                             "URL": self.description['mainEntityofPage']['@id'],
                             "Followers": text[0], "Following": text[2], "Posts": text[4],
                             "Bio": str(
                                 self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['biography']),
                             "profile_pic_url": str(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                                        'profile_pic_url_hd']),
                             "is_business_account": str(
                                 self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                     'is_business_account']),
                             "connected_to_fb": str(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                                        'connected_fb_page']),
                             "externalurl": str(
                                 self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['external_url']),
                             "joined_recently": str(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                                        'is_joined_recently']),
                             "business_category_name": str(
                                 self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user'][
                                     'business_category_name']),
                             "is_private": str(
                                 self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['is_private']),
                             "is_verified": str(
                                 self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['is_verified'])}

        return self.profile_data


    def scrape_posts(self):
        """Scrapes all posts and downloads them
        :return: none
        :param: none
        """
        if self.profile_data['is_private'].lower() == 'true':
            print("[*]Private profile, cannot scrape photos!")
            return 1
        else:
            posts = {}
            for index, post in enumerate(self.profile_meta['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']):
              
                posts[index] = {"Caption": str(post['node']['edge_media_to_caption']['edges'][0]['node']['text']),
                                "Number of Comments": str(post['node']['edge_media_to_comment']['count']),
                                "Comments Disabled": str(post['node']['comments_disabled']),
                                "Taken At Timestamp": str(post['node']['taken_at_timestamp']),
                                "Number of Likes": str(post['node']['edge_liked_by']['count']),
                                "Location": str(post['node']['location']),
                                "Accessability Caption": str(post['node']['accessibility_caption'])
                                }
        return posts

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("username", help="Instagram Username (Profile Name)",type=str)
    parser.add_argument('-v','--version', action='version',
                    version='%(prog)s 1.0')
   
    results = parser.parse_args()
    print("#########################-----INSTAGRAM SCRAPER-----#########################")
    print("Scraping for ",results.username)
    df = Instagram(results.username)
    print('Details : \n')
    for key,values in df.scrape_profile().items():
        print(key," : ",values)
    try:
       
        for key,values in df.scrape_posts().items():
            print("\n")
            print("Post : ",key+1)
            print("\n")
            for key,values in values.items():
                print(key," : ",values)        
    except:
        pass
    print("Follow : https://github.com/dhanushnayak")
if __name__=='__main__':
    main()
