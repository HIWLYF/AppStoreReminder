#!/usr/bin/python3
# coding=utf-8
############################################################
#
#	handler app changes and mail to you
#	include the following:
#	* app is not available in App Store any more
#	* app come back to App Store
#	* app cut price
#	* app get a new version
#	please add this script to crontab:
# 	LC_CTYPE="en_US.UTF-8"
#	0 */1 * * * /usr/local/bin/python3  ~/App StoreReminder/handler_app.py >> ~/handler_app.log
#
############################################################
import os
import sys
import json
import api
import time


def report_print(index, count, content):
    print("[{}/{}] {}".format(index, count, content))

def main():
    root_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    cache_path = os.path.join(root_path, "app.json")
    config_path = os.path.join(root_path, "config.json")

    # read cache file
    try:
        f = open(cache_path, 'r', encoding='utf-8')
        content = f.read()
        f.close()
        cache_list = json.loads(content)
    except BaseException:
        print("read app.json error")
        return

    # token = ''
    # enable_notice = False
    # app_lost_notice = False
    # app_update_notice = False
    # app_price_change_notice = False
    # app_price_discount_notice = False

    # read config file
    try:
        f = open(config_path, 'r')
        content = f.read()
        f.close()
        config = json.loads(content)
        token = config['token']
        enable_notice = config['enable_notice']
        app_lost_notice = config['app_lost_notice']
        app_update_notice = config['app_update_notice']
        app_price_change_notice = config['app_price_change_notice']
        app_price_discount_notice = config['app_price_discount_notice']
    except BaseException:
        print('read config.json error')
        return

    client = api.Client()
    current_index = 0
    app_count = len(cache_list)

    for item in cache_list:
        has_change = False
        current_index += 1
        app_id = item['trackId']
        country = item['country']
        track_name = item['trackName']
        new_item = client.get_app_info(app_id, country)
        if new_item is None or len(new_item) == 0:
            # app lost in App Store
            if item['available']:
                item['available'] = False
                content = "{} 下架了".format(track_name)
                report_print(current_index, app_count, content)
                if enable_notice and app_lost_notice:
                    client.send_notice(token, 0, "APP 下架提示!", content)
        else:
            new_item['available'] = True
            new_item['country'] = item['country']

            if not item['available']:
                # app come back to App Store
                has_change = True
                item['available'] = True
                content = "【{}】 又上架了".format(track_name)
                report_print(current_index, app_count, content)
                if enable_notice and app_lost_notice:
                    client.send_notice(token, 0, "APP 上架提示!", content)

            if new_item['price'] != item['price']:
                # app price changed
                has_change = True
                content = "【{}】 从 {} -> {}".format(new_item['trackName'], item['price'], new_item['price'])
                report_print(current_index, app_count, content)
                if enable_notice:
                    if new_item['price'] < item['price']:
                        if app_price_discount_notice:
                            client.send_notice(token, 0, "APP 降价了!", content)
                    elif app_price_change_notice:
                        client.send_notice(token, 0, "APP 涨价了!", content)

            if new_item['version'] != item['version']:
                # app version changed
                has_change = True
                content = "【{}】 version changed {} -> {}".format(new_item['trackName'], item['version'],
                                                                 new_item['version'])
                report_print(current_index, app_count, content)
                if enable_notice and app_update_notice:
                    client.send_notice(token, 0, "APP version changed!", content)

            for key in item.keys():
                item[key] = new_item[key]

            if not has_change:
                content = "【{}】 没有变化".format(track_name)
                report_print(current_index, app_count, content)
            if current_index != app_count:
                time.sleep(2)

    content = json.dumps(cache_list, indent=4, sort_keys=True, ensure_ascii=False)
    f = open(cache_path, 'w', encoding='utf-8')
    f.write(content)
    f.close()


if __name__ == '__main__':
    main()
