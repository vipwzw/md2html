#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 转图片工具
支持将 HTML 文件转换为图片格式（PNG、JPG、WEBP）
"""

import sys
import os
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright


class HTML2Image:
    """HTML 转图片转换器"""
    
    def __init__(self):
        self.default_viewport = {"width": 1200, "height": 800}
        self.supported_formats = ["png", "jpeg"]
    
    async def convert_file(self, html_path, output_path, options=None):
        """
        将 HTML 文件转换为图片
        
        Args:
            html_path: HTML 文件路径
            output_path: 输出图片路径
            options: 转换选项
        """
        if options is None:
            options = {}
        
        # 验证输入文件
        if not os.path.exists(html_path):
            raise FileNotFoundError(f"HTML 文件不存在: {html_path}")
        
        # 获取输出格式
        output_format = self._get_output_format(output_path)
        
        async with async_playwright() as p:
            # 启动浏览器
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # 设置视口大小
            viewport = options.get("viewport", self.default_viewport)
            await page.set_viewport_size(viewport)
            
            # 加载 HTML 文件
            html_file_url = f"file://{os.path.abspath(html_path)}"
            await page.goto(html_file_url, wait_until="networkidle")
            
            # 等待页面完全加载（特别是数学公式）
            await page.wait_for_timeout(2000)
            
            # 截图选项
            screenshot_options = {
                "path": output_path,
                "type": output_format,
                "full_page": options.get("full_page", True)
            }
            
            # 如果是 jpeg 格式，设置质量
            if output_format == "jpeg":
                screenshot_options["quality"] = options.get("quality", 90)
            
            # 截取图片
            await page.screenshot(**screenshot_options)
            
            await browser.close()
    
    async def convert_html_string(self, html_content, output_path, options=None):
        """
        将 HTML 字符串转换为图片
        
        Args:
            html_content: HTML 内容字符串
            output_path: 输出图片路径
            options: 转换选项
        """
        if options is None:
            options = {}
        
        # 获取输出格式
        output_format = self._get_output_format(output_path)
        
        async with async_playwright() as p:
            # 启动浏览器
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # 设置视口大小
            viewport = options.get("viewport", self.default_viewport)
            await page.set_viewport_size(viewport)
            
            # 设置 HTML 内容
            await page.set_content(html_content, wait_until="networkidle")
            
            # 等待页面完全加载
            await page.wait_for_timeout(2000)
            
            # 截图选项
            screenshot_options = {
                "path": output_path,
                "type": output_format,
                "full_page": options.get("full_page", True)
            }
            
            # 如果是 jpeg 格式，设置质量
            if output_format == "jpeg":
                screenshot_options["quality"] = options.get("quality", 90)
            
            # 截取图片
            await page.screenshot(**screenshot_options)
            
            await browser.close()
    
    def _get_output_format(self, output_path):
        """获取输出格式"""
        ext = Path(output_path).suffix.lower()
        if ext == ".png":
            return "png"
        elif ext in [".jpg", ".jpeg"]:
            return "jpeg"
        else:
            raise ValueError(f"不支持的图片格式: {ext}. 支持的格式: {self.supported_formats}")


def main():
    """命令行主函数"""
    if len(sys.argv) < 3:
        print("用法: python html2image.py <HTML文件> <输出图片> [选项]")
        print("选项:")
        print("  --width WIDTH     设置页面宽度 (默认: 1200)")
        print("  --height HEIGHT   设置页面高度 (默认: 800)")
        print("  --quality QUALITY 设置JPEG质量 (1-100, 默认: 90)")
        print("  --no-full-page    不截取整个页面，只截取可见区域")
        print()
        print("支持的图片格式: png, jpg, jpeg")
        print()
        print("示例:")
        print("  python html2image.py input.html output.png")
        print("  python html2image.py input.html output.jpg --width 800 --quality 95")
        sys.exit(1)
    
    html_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # 解析选项
    options = {
        "viewport": {"width": 1200, "height": 800},
        "full_page": True,
        "quality": 90
    }
    
    i = 3
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--width" and i + 1 < len(sys.argv):
            options["viewport"]["width"] = int(sys.argv[i + 1])
            i += 2
        elif arg == "--height" and i + 1 < len(sys.argv):
            options["viewport"]["height"] = int(sys.argv[i + 1])
            i += 2
        elif arg == "--quality" and i + 1 < len(sys.argv):
            options["quality"] = int(sys.argv[i + 1])
            i += 2
        elif arg == "--no-full-page":
            options["full_page"] = False
            i += 1
        else:
            print(f"未知选项: {arg}")
            sys.exit(1)
    
    # 创建转换器并执行转换
    converter = HTML2Image()
    
    try:
        asyncio.run(converter.convert_file(html_path, output_path, options))
        print(f"转换完成: {output_path}")
    except Exception as e:
        print(f"转换失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 