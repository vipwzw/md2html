#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 转图片功能使用示例
演示如何使用 html2image.py 和 md2image.py
"""

import asyncio
import os
from html2image import HTML2Image
from md2image import MD2Image


async def demo_html_to_image():
    """演示 HTML 转图片功能"""
    print("=== HTML 转图片功能演示 ===")
    
    # 创建转换器
    converter = HTML2Image()
    
    # 基本用法
    if os.path.exists("output/快速幂算法.html"):
        print("1. 基本用法：HTML 转 PNG")
        await converter.convert_file(
            "output/快速幂算法.html", 
            "output/demo_basic.png"
        )
        print("   生成：output/demo_basic.png")
    
    # 自定义选项
    print("\n2. 自定义选项：设置尺寸和质量")
    options = {
        "viewport": {"width": 800, "height": 600},
        "quality": 85,
        "full_page": True
    }
    
    if os.path.exists("output/快速幂算法.html"):
        await converter.convert_file(
            "output/快速幂算法.html", 
            "output/demo_custom.jpg",
            options
        )
        print("   生成：output/demo_custom.jpg")
    
    # 从 HTML 字符串生成
    print("\n3. 从 HTML 字符串生成图片")
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>测试页面</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container { 
                max-width: 600px; 
                margin: 0 auto; 
                text-align: center;
            }
            h1 { font-size: 2.5em; margin-bottom: 20px; }
            p { font-size: 1.2em; line-height: 1.6; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>HTML 转图片演示</h1>
            <p>这是一个由 HTML 字符串生成的图片</p>
            <p>支持 CSS 样式和现代网页设计</p>
        </div>
    </body>
    </html>
    """
    
    await converter.convert_html_string(
        html_content,
        "output/demo_from_string.png",
        {"viewport": {"width": 800, "height": 400}}
    )
    print("   生成：output/demo_from_string.png")


async def demo_md_to_image():
    """演示 Markdown 直接转图片功能"""
    print("\n=== Markdown 直接转图片功能演示 ===")
    
    # 创建转换器
    converter = MD2Image()
    
    # 基本用法
    if os.path.exists("example/快速幂算法.md"):
        print("1. 基本用法：Markdown 转 PNG")
        await converter.convert_file(
            "example/快速幂算法.md", 
            "output/demo_md_basic.png"
        )
        print("   生成：output/demo_md_basic.png")
    
    # 自定义选项
    print("\n2. 自定义选项：高分辨率 PNG 格式")
    options = {
        "viewport": {"width": 1600, "height": 1200},
        "full_page": True
    }
    
    if os.path.exists("example/快速幂算法.md"):
        await converter.convert_file(
            "example/快速幂算法.md", 
            "output/demo_md_hires.png",
            options
        )
        print("   生成：output/demo_md_hires.png")
    
    # 从 Markdown 字符串生成
    print("\n3. 从 Markdown 字符串生成图片")
    md_content = """
# Markdown 转图片演示

这是一个演示 **Markdown** 直接转换为图片的示例。

## 支持的功能

- ✅ 标题和文本格式
- ✅ **粗体** 和 *斜体*
- ✅ 代码块和行内代码
- ✅ 列表和表格
- ✅ 数学公式（MathJax）

## 代码示例

```python
def hello_world():
    print("Hello, World!")
    return "转换成功！"
```

## 数学公式

行内公式：$E = mc^2$

块级公式：
$$
\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}
$$

> 这是一个引用块，演示了 Markdown 的丰富格式支持。
"""
    
    await converter.convert_md_string(
        md_content,
        "output/demo_md_from_string.png",
        {"viewport": {"width": 1000, "height": 800}}
    )
    print("   生成：output/demo_md_from_string.png")


async def main():
    """主函数"""
    print("开始 HTML 转图片功能演示...")
    
    # 确保输出目录存在
    os.makedirs("output", exist_ok=True)
    
    # 演示 HTML 转图片
    await demo_html_to_image()
    
    # 演示 Markdown 直接转图片
    await demo_md_to_image()
    
    print("\n=== 演示完成 ===")
    print("请查看 output/ 目录中生成的图片文件")


if __name__ == "__main__":
    asyncio.run(main()) 