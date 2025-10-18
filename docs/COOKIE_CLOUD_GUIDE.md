# Cookie Cloud 配置指南

## 🎯 为什么使用 Cookie Cloud？

根据最新信息（2025年），微信读书的 Cookie 认证机制发生了变化：
- **传统方式**：手动复制 Cookie，有效期短（小于 2 小时）
- **Cookie Cloud**：自动同步浏览器 Cookie，无需手动更新

## 📦 安装 Cookie Cloud

### 步骤 1：安装浏览器插件

选择你的浏览器安装插件：

**Chrome / Edge：**
- 访问 [Chrome Web Store](https://chromewebstore.google.com/detail/cookiecloud/ffjiejobkoibkjlhjnlgmcnnigeelbdl)
- 点击"添加到 Chrome"

**Firefox：**
- 访问 Firefox 插件商店搜索 "CookieCloud"

### 步骤 2：配置 Cookie Cloud 服务器

你有两个选择：

#### 方案 A：使用公共服务器（推荐，简单）

使用默认公共服务器：
```
https://cc.chenge.ink
```
或：
```
https://cookiecloud.malinkang.com/
```

#### 方案 B：自建服务器（可选，更安全）

使用 Docker 部署：
```bash
docker run -d -p=8088:8088 easychen/cookiecloud:latest
```

然后使用：`http://你的服务器IP:8088`

### 步骤 3：配置浏览器插件

1. **点击浏览器中的 Cookie Cloud 插件图标**

2. **填写配置信息：**
   - **服务器地址**：`https://cc.chenge.ink`（或你的自建服务器地址）
   - **用户 KEY（UUID）**：插件会自动生成，记住这个值
   - **端对端加密密码**：设置一个强密码，记住这个值

3. **设置微信读书域名过滤（重要）：**
   - 在"同步域名关键词"中填入：`weread.qq.com`
   - 这样只会同步微信读书的 Cookie，提高安全性

4. **开启 Cookie 保活（可选但推荐）：**
   - 在"Cookie 保活"中填入：`https://weread.qq.com/|60`
   - 这会每 60 分钟自动访问一次微信读书，保持 Cookie 活跃

5. **设置为上传模式：**
   - 选择"上传模式"（从浏览器同步到服务器）

6. **点击"保存并同步"**

### 步骤 4：登录微信读书

1. 在浏览器中访问：https://weread.qq.com/
2. 使用微信扫码登录
3. 登录成功后，Cookie Cloud 会自动上传 Cookie

### 步骤 5：配置项目

编辑 `.env` 文件，添加 Cookie Cloud 配置：

```bash
# Cookie Cloud 配置（推荐）
CC_URL="https://cc.chenge.ink"
CC_ID="你的UUID（从插件中复制）"
CC_PASSWORD="你的加密密码"

# 备用：直接设置 Cookie（可选）
# WEREAD_COOKIE="你的cookie"
```

## ✅ 验证配置

运行测试脚本：
```bash
python3 diagnostic.py
```

如果看到：
```
✅ Cookie 状态: 正常
✅ 账号状态: 已激活，有 X 本书
✅ 可以开始同步
```

说明配置成功！

## 🔧 常见问题

### Q1: Cookie Cloud 插件无法连接服务器？
A: 检查服务器地址是否正确，确保可以访问

### Q2: 同步失败？
A:
1. 检查 UUID 和密码是否正确
2. 确保浏览器已登录微信读书
3. 检查域名关键词是否设置为 `weread.qq.com`

### Q3: Cookie 还是过期？
A:
1. 启用 Cookie 保活功能
2. 设置更短的同步间隔（在插件中设置）

### Q4: 多个浏览器如何配置？
A:
- 主浏览器设置为"上传模式"
- 其他浏览器设置为"下载模式"
- 使用相同的 UUID 和密码

## 📝 配置示例

完整的 `.env` 配置示例：

```bash
# ==================== Cookie Cloud 配置 ====================
# 服务器地址
CC_URL="https://cc.chenge.ink"

# 用户 UUID（从浏览器插件中获取）
CC_ID="12345678-1234-1234-1234-123456789abc"

# 端对端加密密码
CC_PASSWORD="你的强密码"

# ==================== Flomo API ====================
FLOMO_API="https://flomoapp.com/iwh/xxxxxx/"

# ==================== 备用 Cookie（可选）====================
# 如果 Cookie Cloud 失败，会使用这个 Cookie
# WEREAD_COOKIE="手动获取的cookie"
```

## 🎯 优势

使用 Cookie Cloud 的好处：
- ✅ **自动更新**：无需手动复制 Cookie
- ✅ **长期有效**：Cookie 保活功能保持登录状态
- ✅ **多端同步**：多个设备共享同一个登录状态
- ✅ **安全加密**：端对端加密，服务器无法读取
- ✅ **自动容错**：Cookie 失效时自动重新获取

---

配置完成后，项目会优先使用 Cookie Cloud，只有失败时才会使用 `WEREAD_COOKIE`。
