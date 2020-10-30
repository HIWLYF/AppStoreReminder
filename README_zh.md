# App Store Reminder
## 简介
喜欢的app降价了？更新了？下架了又或者重新上架了？
脚本一键监听，邮件提醒，就这么点功能。
## 使用说明
* 修改config.json配置Bark推送的Token和通知开关
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
* 运行search_app.py
  输入app的名称搜索app并加入监听列表

* 运行handler_app.py
  运行一次刷新一次监听列表中的app，发现变化邮件通知
  推荐加入定时任务（linux crontab命令）中指定频率运行

## 注意事项
* 使用Bark的推送服务，需要在App Store中安装Bark APP， 并将Token保存到config.json文件中