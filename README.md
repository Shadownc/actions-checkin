# Actions Check-in

本仓库用于存放 `GitHub Actions` 执行的各种签到脚本。

## 新增功能：
### **企业微信消息推送**

现在可以通过**企业微信**接收 `GitHub Actions` 执行的通知。要启用该功能，请设置企业微信机器人的 `webhook` 并将 `webhook key` 添加为 `GitHub Actions` 的 `secret`。

**配置步骤：**

1. 前往 `GitHub` 仓库的 `Settings` > `Secrets and variables` > `Actions`。
2. 添加名称为 `WEBHOOK_KEY` 的新 `secret`，并将企业微信 `webhook key` 作为值输入。

完成后，`Actions` 工作流可以使用该 `key` 发送通知。

### **Server酱**
[文档地址](https://sct.ftqq.com/)  
**配置步骤：**
1. 前往 `GitHub` 仓库的 `Settings` > `Secrets and variables` > `Actions`。
2. 添加名称为 `SERVER_CHAN_KEY` 的新 `secret`，并将管理后台的`key` 作为值输入。

### **Qmsg酱消息推送**  
[文档地址](https://qmsg.zendee.cn/)  
**配置步骤：**
1. 前往 `GitHub` 仓库的 `Settings` > `Secrets and variables` > `Actions`。
2. 添加名称为 `QMSG_KEY` 的新 `secret`，并将`Qmsg酱`管理台的`key` 作为值输入。

---

## [WebP Cloud](https://dashboard.webp.se/proxy)

在签到脚本中使用 **WebP Cloud**：

1. 前往 `GitHub` 仓库的 `Settings` > `Secrets and variables` > `Actions`。
2. 添加名称为 `WEBPCLOUD_TOKEN` 的新 `secret`。
3. 从登录后的**Local Storage**中获取 `token` 并将其作为 `secret` 的值。

---

## [Follow](https://app.follow.is/)

**重要提示**：建议使用无痕模式进行登录 千万不要退出登录，否则参数值将失效 有效期似乎只有五天 五天以后需要重新设置变量。

使用 **Follow**，需要在 `GitHub` 中添加以下两个 `secret`：

1. 前往 `GitHub` 仓库的 `Settings` > `Secrets and variables` > `Actions`。
2. 添加两个新 `secret`：
   - `FOLLOW_CSRF_TOKEN`
   - `FOLLOW_COOKIE`

   > 这两个值可以从浏览器开发者工具的 `/auth/session` 请求头（`Request Header`）中获取。

---
