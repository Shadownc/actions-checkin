# actions-checkin
用来存放actions执行各种签到的脚本

## [WebP Cloud](https://dashboard.webp.se/proxy)
在 `GitHub` 仓库的 `Settings` > `Secrets and variables` > `Actions` 中添加的 `Secret` 名称是 `WEBPCLOUD_TOKEN`。
值从登录后的`Local storage`取 `token`

## [follow](https://app.follow.is/)
在 `GitHub` 仓库的 `Settings` > `Secrets and variables` > `Actions` 中添加两个变量：
* `FOLLOW_CSRF_TOKEN`
* `FOLLOW_COOKIE`
> 两个值都可以从`/auth/session`的`Request Header`中拿到