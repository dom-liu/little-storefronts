# Little Storefronts

**南瓜小镇与蓝莓海湾，两套已经构建好的交互式 3D 网页。**

[English](README.md) · **简体中文** · [来源与致谢](CREDITS.md)

| 南瓜小镇 · Pumpkin Hollow | 蓝莓海湾 · Blueberry Cove |
| --- | --- |
| ![南瓜小镇](docs/pumpkin-hollow.jpg) | ![蓝莓海湾](docs/blueberry-cove.jpg) |
| 秋日烘焙店 | 海边小厨房 |

这是我在小红书分享的两个主题，整理成可下载的 HTML 成品包。
仓库包含完整的 **HTML、CSS、JavaScript、模型和图片**。
不需要安装 Node.js、依赖或执行构建命令，也不需要 API 密钥。

## 下载与打开

1. 在 GitHub 点击 **Code → Download ZIP**，完整解压。
2. 进入 `pumpkin-hollow/`（南瓜）或 `blueberry-cove/`（蓝莓）。
3. `README.html` 是配图使用说明，`index.html` 是网页入口。

每个主题文件夹都是一套独立网站，文件要放在一起，不要只复制 HTML。
包的结构考虑了直接打开 `index.html` 的使用方式，但双击打开的 `file://` 兼容性
仍需在你的浏览器中手动验证。已验证的方式是通过静态 HTTP 服务打开。
如果电脑装有 Python，可以在仓库目录运行：

```sh
python3 -m http.server 8000
```

然后打开 [南瓜小镇](http://localhost:8000/pumpkin-hollow/)
或 [蓝莓海湾](http://localhost:8000/blueberry-cove/)。

两套独立 ZIP 也可通过 [GitHub Releases](https://github.com/dom-liu/little-storefronts/releases)
分发；Release 附件与 GitHub 的完整仓库 ZIP 不同。本仓库不会自动发布 Release。

## 修改内容

用纯文本编辑器打开对应主题的 **`shop-config.js`**，修改后保存并刷新：

| 字段 | 用途 |
| --- | --- |
| `shopName`、`subtitle`、`tagline` | 网页店名、副标题、页脚文案 |
| `hours` | 营业时间提示 |
| `hero`、`story` | 三行首页标题和故事段落 |
| `menu` | 四件商品的名称、美元价格、描述与图片路径 |
| `orderUrl` | 可选的外部 HTTPS 点单链接，留空隐藏 |

保留原商品 ID 和有效的 JavaScript 语法。商品图片在 `assets/photos/`，
可以同名替换，或修改配置中的图片路径。价格使用数字，不加美元符号。
修改网页店名不会改变模型贴图上的招牌，换商品图片也不会改变 3D 模型。
七个 3D 模型已经嵌入 `assets/model-data.js`，为缩小下载体积，不再附带重复的独立 GLB。
更换模型需要从开发项目重新导出。

## 内容与边界

每个文件夹包含网页入口、配置、构建好的 JS/CSS、图片、嵌入模型数据、
配图指南、来源说明、第三方许可和文件哈希清单。
可以旋转建筑和商品、浏览菜单、切换昼夜以及使用静态插画模式。
交互式 3D 需要支持 WebGL2 的近期桌面浏览器；项目以桌面为主，
尚未覆盖所有浏览器的兼容性。网页默认英文，本文件提供中文使用说明。

店铺、商品与美元价格都是演示。收藏、购物袋和预览小票只保存在本地，
不会产生真实订单或扣款。外部点单链接不会自动接收演示购物袋的商品。

## 部署与单独打包

把任意一个**完整主题文件夹**上传到静态网页托管服务，保持相对路径即可。
不需要服务器函数或构建命令；下载和打开本项目不会自动部署。

维护者可使用 Python 检查文件并生成两套独立 ZIP：

```sh
python3 scripts/check.py
python3 scripts/package.py
```

ZIP 和 `SHA256SUMS.txt` 会放在忽略提交的 `out/` 中，已有包不会被覆盖。
这两个命令不会部署网站或发布 Release。

## 授权与致谢

根目录 [MIT](LICENSE) 适用于本项目自有的文档与配置；构建后的运行代码保留
各主题 `licenses/` 中的第三方声明。**模型、图片与贴图不在根目录 MIT 授权范围内**，
详见 [素材说明](ASSET_LICENSE.md)。本仓库分享的是静态成品包，不是 React 开发工程。

视觉起点来自 [Dilum Sanjaya](https://x.com/DilumSanjaya) 的 **Strawberry Corner**。
两个主题使用 AI 辅助概念图、腾讯混元 3D V3.1 和后续 Blender 整理。
署名与 AI 生成不等于原创性或第三方授权证明。详见 [Credits](CREDITS.md)。
公开内容只有南瓜小镇与蓝莓海湾。
