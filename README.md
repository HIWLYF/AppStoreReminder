# App Store Reminder
[中文版本](https://github.com/ookcode/AppStoreReminder/blob/master/README_zh.md)
## Introduction
Did you want to get a notification when your favorite apps cut price,updated,or out off the shelf in the appstore?
This Script Help you to monitor these apps.

## Instructions for use
* edit config.json
```json
{
    "token": "",
    "enable_notice": true,
    "app_lost_notice": false,
    "app_update_notice": false,
    "app_price_change_notice": false,
    "app_price_discount_notice": true
}
```
* search_app.py
  `$python search_app.py`
  Enter the name of the app to search for the app and then add it to the listeners

* handler_app.py
  `$python handler_app.py`
  Each run will traverse the list of listeners and mail you the change.
  I recommended you join the script to the scheduler (linux crontab command) to make a frequency operation

## Precautions
* Need install Bark in App Store.