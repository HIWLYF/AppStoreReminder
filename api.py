#!/usr/bin/python3
# coding=utf-8
############################################################
#
#	appstore api
#
############################################################
import os, sys
import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}


class Client():
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = headers

    ################################
    # get app info
    # @param 	app_id 		app track id in appstore
    # @param 	country		country code
    # @return 	app info
    #################################
    def get_app_info(self, app_id, country):
        response = self.session.get('https://itunes.apple.com/lookup?id={}&country={}'.format(app_id, country))
        data = json.loads(response.content.decode('utf-8'))
        # -- main keys --
        # trackId
        # trackName
        # price
        # formattedPrice
        # version
        # bundleId
        # releaseDate
        # currentVersionReleaseDate
        # fileSizeBytes
        try:
            return data['results'][0]
        except Exception as e:
            if 'errorMessage' in data:
                print('errorMessage', data['errorMessage'])
            else:
                print(e)

    ################################
    # search app
    # @param 	keyword 	search keyword
    # @param 	max_count	allow max data
    # @return 	app info list
    #################################
    def search_app(self, keyword, country, max_count):
        response = self.session.get(
            'https://itunes.apple.com/search?term={}&country={}&media=software&limit={}'.format(keyword, country,
                                                                                                max_count))
        data = json.loads(response.content.decode('utf-8'))
        try:
            return data['results']
        except Exception as e:
            if 'errorMessage' in data:
                print('errorMessage', data['errorMessage'])
            else:
                print(e)

    def send_notice(self, token, notice_type=0, title='', content='', url=''):
        if token == "":
            print("Please install Bark on your phone and input token to config.json")
            return
        # https://api.day.app/token/Customed Notification Content
        type_1 = 'https://api.day.app/{}/{}/{}'
        type_2 = 'https://api.day.app/{}/{}?url={}'
        notice_url = ""
        if notice_type == 0:
            notice_url = type_1.format(token, title, content)
        elif notice_type == 1:
            notice_url = type_2.format(token, title, url)
        self.session.get(notice_url)
