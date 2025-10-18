# Assets 资源目录

本目录存放项目相关的静态资源文件。

## 📁 目录结构

```
assets/
├── images/          # 图片资源
│   ├── flomo.png   # 项目 Logo（主要使用）
│   └── logo.png    # 备用 Logo
└── README.md       # 本文件
```

## 🖼️ 图片资源

### flomo.png（主要使用）

- **用途**: 项目主 Logo，显示在 README 顶部
- **尺寸**: 在 README 中设置为 width="100"
- **大小**: ~44KB
- **格式**: PNG
- **来源**: Flomo 官方 Logo

### logo.png（备用）

- **用途**: 备用 Logo
- **尺寸**: 可根据需要调整
- **大小**: ~21KB
- **格式**: PNG

## 📝 使用说明

### 在 Markdown 中引用

```markdown
![Logo](./assets/images/flomo.png)
```

或者指定尺寸：

```markdown
<img src="./assets/images/flomo.png" alt="Logo" width="100"/>
```

## 🎨 设计规范

- Logo 使用 Flomo 品牌色：绿色 (#00C896)
- 保持简洁、清晰、可识别
- 适配暗色和亮色主题

## 📄 许可证

Logo 版权归 Flomo 所有，本项目仅作为工具集成使用。

