# md2html

将 Markdown (md) 文件转换为 HTML 文件，并支持 HTML 转图片的多功能命令行工具。

## 功能特性

- ✅ 支持标准 Markdown 语法（标题、列表、表格、链接等）
- ✅ 支持代码块语法高亮 
- ✅ 支持数学公式渲染（MathJax）
- ✅ 支持本地图片（自动转换为base64嵌入）
- ✅ 响应式设计，适配多种设备
- ✅ 优美的现代化样式
- 🆕 **HTML 转图片功能**
- 🆕 **Markdown 直接转图片**
- 🆕 **可自定义图片尺寸和质量**

## 🚀 快速开始

### 1. 安装依赖

#### 方法一：一键安装（推荐）

```bash
python install.py
```

#### 方法二：手动安装

```bash
pip install -r requirements.txt
# 安装 Playwright 浏览器驱动
playwright install chromium
```

### 2. 立即体验

```bash
# 运行完整功能演示
python 示例用法.py

# 或者直接转换示例文件
python md2image.py example/快速幂算法.md output/demo.png
```

## 使用方法

### 1. Markdown 转 HTML

#### 基础版本 (md2html.py)
适用于不包含本地图片的简单文档：

```bash
python md2html.py 输入文件.md 输出文件.html
```

#### 高级版本 (md2html_with_images.py)
支持本地图片和完整功能：

```bash
python md2html_with_images.py 输入文件.md 输出文件.html
```

### 2. HTML 转图片 🆕

```bash
# 基本用法
python html2image.py input.html output.png

# 自定义选项
python html2image.py input.html output.jpg --width 1600 --height 1200 --quality 95
```

**支持的图片格式：** PNG、JPG、JPEG

**可用选项：**
- `--width WIDTH`: 设置页面宽度（默认：1200）
- `--height HEIGHT`: 设置页面高度（默认：800）
- `--quality QUALITY`: 设置JPEG质量（1-100，默认：90）
- `--no-full-page`: 不截取整个页面，只截取可见区域

### 3. Markdown 直接转图片 🆕

```bash
# 基本用法
python md2image.py document.md output.png

# 自定义选项
python md2image.py document.md output.jpg --width 1600 --height 1200 --quality 95
```

这个工具整合了 Markdown 转 HTML 和 HTML 转图片的功能，一步直接从 Markdown 生成图片。

## 示例用法

```bash
# 转换示例文件为 HTML
python md2html_with_images.py example/快速幂算法.md output/快速幂算法.html

# 将 HTML 转换为图片
python html2image.py output/快速幂算法.html output/快速幂算法.png

# 直接从 Markdown 生成图片
python md2image.py example/快速幂算法.md output/快速幂算法.png

# 生成高质量图片
python md2image.py example/快速幂算法.md output/快速幂算法.jpg --width 1600 --quality 95

# 运行完整功能演示
python 示例用法.py
```

## 支持的功能

### 数学公式
- 行内公式：`$E = mc^2$` 
- 块级公式：
  ```
  $$
  \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
  $$
  ```

### 代码高亮
支持多种编程语言的语法高亮：

````markdown
```python
def hello_world():
    print("Hello, World!")
```
````

### 图片支持
- 网络图片：自动保持原样
- 本地图片：自动转换为base64嵌入（无需额外文件）
- 🆕 **HTML 转图片**：支持将渲染后的 HTML 页面转换为图片

### 表格和列表
完整支持Markdown表格和有序/无序列表。

## 输出特性

### HTML 输出
生成的HTML文件具有以下特点：

- 🎨 现代化设计风格
- 📱 响应式布局
- 🔤 优化的字体选择
- 🎯 代码语法高亮
- 📐 数学公式渲染
- 🖼️ 图片自动适配

### 图片输出 🆕
生成的图片文件具有以下特点：

- 📸 高质量网页截图
- 🎨 保持完整的CSS样式
- 📐 支持数学公式渲染
- 🎯 代码语法高亮完整保留
- 📏 可自定义尺寸和质量
- 🖼️ 支持 PNG 和 JPG 格式

## 依赖说明

- `markdown`: 核心Markdown解析器
- `python-markdown-math`: 数学公式扩展
- `Pygments`: 代码语法高亮
- `pillow`: 图片处理支持
- `playwright`: HTML转图片支持（需要额外安装浏览器驱动）

## 文件结构

```
md2html/
├── md2html.py                    # 基础版本转换器
├── md2html_with_images.py       # 高级版本转换器
├── html2image.py                # HTML转图片工具 🆕
├── md2image.py                  # Markdown直接转图片工具 🆕
├── 示例用法.py                   # 功能演示脚本 🆕
├── install.py                   # 一键安装脚本 🆕
├── requirements.txt              # 项目依赖
├── README.md                    # 项目文档
├── example/                      # 示例文件
│   └── 快速幂算法.md
├── imgs/                        # 测试图片
└── output/                      # 输出目录
```

## 高级用法

### 程序化使用

```python
import asyncio
from html2image import HTML2Image
from md2image import MD2Image

async def main():
    # HTML 转图片
    html_converter = HTML2Image()
    await html_converter.convert_file("input.html", "output.png")
    
    # Markdown 直接转图片
    md_converter = MD2Image()
    await md_converter.convert_file("document.md", "output.png", {
        "viewport": {"width": 1600, "height": 1200},
        "quality": 95
    })

asyncio.run(main())
```

### 从字符串生成图片

```python
import asyncio
from html2image import HTML2Image
from md2image import MD2Image

async def main():
    # 从 HTML 字符串生成图片
    html_converter = HTML2Image()
    html_content = "<h1>Hello World</h1>"
    await html_converter.convert_html_string(html_content, "output.png")
    
    # 从 Markdown 字符串生成图片
    md_converter = MD2Image()
    md_content = "# Hello World\n\nThis is **bold** text."
    await md_converter.convert_md_string(md_content, "output.png")

asyncio.run(main())
```

## 注意事项

1. 生成的HTML文件是完全自包含的，包含所有必要的CSS和JavaScript
2. 本地图片会被转换为base64编码嵌入到HTML中
3. 数学公式使用MathJax在线渲染，需要网络连接
4. 代码高亮使用Highlight.js在线库
5. 🆕 **HTML 转图片功能需要安装 Playwright 浏览器驱动**
6. 🆕 **图片生成过程中会启动无头浏览器，首次使用可能需要一些时间**

---

如有问题或建议，欢迎提出Issue！ 