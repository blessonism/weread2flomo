# 如何正确获取微信读书 Cookie

## ❗重要提示

你的 Cookie **确实已经过期了**。虽然你的浏览器显示还在登录状态，但这可能是因为：
1. 页面使用了本地缓存
2. Cookie 已在后台过期，但页面未刷新
3. 需要额外的认证 token

## 🔧 正确获取 Cookie 的步骤

### 方法 1：从 Application 标签获取（最准确）

1. **打开微信读书网页版**
   ```
   https://weread.qq.com/
   ```

2. **按 F12 打开开发者工具**

3. **切换到 `Application` 标签**（Chrome）或 `存储` 标签（Firefox）

4. **展开左侧的 `Cookies` 节点**

5. **点击 `https://weread.qq.com`**

6. **检查关键 Cookie**：
   - `wr_skey` - 最重要！
   - `wr_vid` - 用户 ID
   - `RK` - 认证令牌

7. **重要：检查每个 Cookie 的值**
   - 确保 `wr_skey` 的值**不是空的**
   - 如果是空的，说明确实过期了

### 方法 2：强制刷新后重新获取

1. **退出登录**
   - 在微信读书页面点击退出登录

2. **重新登录**
   - 使用微信扫码登录

3. **立即获取 Cookie**
   - 登录成功后，按 F12
   - Network 标签 → 刷新页面
   - 找到第一个请求
   - 复制 Cookie 值

### 方法 3：使用脚本获取（推荐）

在浏览器控制台（Console 标签）运行以下代码：

```javascript
// 获取所有 Cookie 并格式化
const cookies = document.cookie.split('; ').map(c => {
  const [key, value] = c.split('=');
  return { key, value };
});

console.log('📋 所有 Cookie:');
console.log(document.cookie);
console.log('');
console.log('🔑 关键 Cookie 检查:');
const keyFields = ['wr_skey', 'wr_vid', 'RK'];
keyFields.forEach(field => {
  const cookie = cookies.find(c => c.key === field);
  if (cookie) {
    console.log(`✓ ${field}: ${cookie.value}`);
  } else {
    console.log(`✗ ${field}: 缺失`);
  }
});

// 复制到剪贴板
copy(document.cookie);
console.log('');
console.log('✅ Cookie 已复制到剪贴板！');
```

### 方法 4：检查 Cookie 是否真的有效

在控制台运行：

```javascript
// 测试 API 调用
fetch('https://i.weread.qq.com/user/notebooks', {
  credentials: 'include',
  headers: {
    'Accept': 'application/json'
  }
})
.then(r => r.json())
.then(data => {
  if (data.books) {
    console.log('✅ Cookie 有效！找到', data.books.length, '本书');
    console.log('前3本:', data.books.slice(0,3).map(b => b.book?.title));
  } else {
    console.log('❌ Cookie 无效:', data);
  }
})
.catch(err => console.log('❌ 请求失败:', err));
```

## 🎯 如果 Cookie 确实过期了

### 解决方案 1：重新登录
1. 访问 https://weread.qq.com/
2. 点击右上角退出登录
3. 使用微信扫码重新登录
4. 立即按 F12 获取新的 Cookie

### 解决方案 2：使用 Cookie Cloud（长期方案）
1. 安装 Cookie Cloud 浏览器插件
2. 配置自动同步
3. 在 `.env` 中配置：
   ```bash
   CC_URL="https://cookiecloud.malinkang.com/"
   CC_ID="你的ID"
   CC_PASSWORD="你的密码"
   ```

## 🔍 验证新 Cookie

获取新 Cookie 后，更新 `.env` 文件，然后运行：

```bash
python3 diagnostic.py
```

如果看到 ✅ 并找到书籍，说明 Cookie 有效。

## ⚠️ 常见问题

**Q: 为什么浏览器显示登录，但 Cookie 无效？**
A: 浏览器可能使用了缓存。尝试硬刷新（Ctrl+Shift+R）或清除缓存后重新登录。

**Q: Cookie 多久会过期？**
A: 微信读书的 Cookie 通常 30 天左右过期，或者在其他设备登录时失效。

**Q: 可以自动更新 Cookie 吗？**
A: 可以，使用 Cookie Cloud 或定期运行获取脚本。
