#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 直接转图片工具
整合了 md2html 和 html2image 的功能
"""

import sys
import os
import tempfile
import asyncio
from pathlib import Path
from md2html import md_to_html
from html2image import HTML2Image


class MD2Image:
    """Markdown 转图片转换器"""
    
    def __init__(self):
        self.html2image = HTML2Image()
    
    async def convert_file(self, md_path, output_path, options=None):
        """
        将 Markdown 文件转换为图片
        
        Args:
            md_path: Markdown 文件路径
            output_path: 输出图片路径
            options: 转换选项
        """
        if options is None:
            options = {}
        
        # 验证输入文件
        if not os.path.exists(md_path):
            raise FileNotFoundError(f"Markdown 文件不存在: {md_path}")
        
        # 创建临时 HTML 文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp_file:
            temp_html_path = tmp_file.name
        
        try:
            # 第一步：Markdown 转 HTML
            md_to_html(md_path, temp_html_path)
            
            # 第二步：HTML 转图片
            await self.html2image.convert_file(temp_html_path, output_path, options)
            
        finally:
            # 清理临时文件
            if os.path.exists(temp_html_path):
                os.unlink(temp_html_path)
    
    async def convert_md_string(self, md_content, output_path, options=None):
        """
        将 Markdown 字符串转换为图片
        
        Args:
            md_content: Markdown 内容字符串
            output_path: 输出图片路径
            options: 转换选项
        """
        if options is None:
            options = {}
        
        # 创建临时 Markdown 文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp_md_file:
            tmp_md_file.write(md_content)
            temp_md_path = tmp_md_file.name
        
        try:
            # 使用文件转换方法
            await self.convert_file(temp_md_path, output_path, options)
            
        finally:
            # 清理临时文件
            if os.path.exists(temp_md_path):
                os.unlink(temp_md_path)


def main():
    """命令行主函数"""
    if len(sys.argv) < 3:
        print("用法: python md2image.py <Markdown文件> <输出图片> [选项]")
        print("选项:")
        print("  --width WIDTH     设置页面宽度 (默认: 1200)")
        print("  --height HEIGHT   设置页面高度 (默认: 800)")
        print("  --quality QUALITY 设置JPEG质量 (1-100, 默认: 90)")
        print("  --no-full-page    不截取整个页面，只截取可见区域")
        print()
        print("支持的图片格式: png, jpg, jpeg")
        print()
        print("示例:")
        print("  python md2image.py document.md output.png")
        print("  python md2image.py document.md output.jpg --width 800 --quality 95")
        print("  python md2image.py document.md output.webp --width 1600 --height 1200")
        sys.exit(1)
    
    md_path = sys.argv[1]
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
    converter = MD2Image()
    
    try:
        asyncio.run(converter.convert_file(md_path, output_path, options))
        print(f"转换完成: {output_path}")
    except Exception as e:
        print(f"转换失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 