#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md2html 项目一键安装脚本
自动安装所有必需的依赖，包括 Playwright 浏览器驱动
"""

import subprocess
import sys
import os


def run_command(command, description):
    """运行命令并显示进度"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败: {e}")
        if e.stdout:
            print(f"输出: {e.stdout}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False


def main():
    """主安装流程"""
    print("🚀 开始安装 md2html 项目依赖...")
    print("=" * 50)
    
    # 检查是否有 requirements.txt 文件
    if not os.path.exists("requirements.txt"):
        print("❌ 找不到 requirements.txt 文件")
        sys.exit(1)
    
    # 步骤1: 安装 Python 依赖
    success = run_command("pip install -r requirements.txt", "安装 Python 依赖")
    if not success:
        print("❌ Python 依赖安装失败，请检查网络连接和权限")
        sys.exit(1)
    
    # 步骤2: 安装 Playwright 浏览器驱动
    success = run_command("playwright install chromium", "安装 Chromium 浏览器驱动")
    if not success:
        print("❌ Playwright 浏览器驱动安装失败")
        print("💡 请尝试手动运行: playwright install chromium")
        sys.exit(1)
    
    # 步骤3: 创建 output 目录
    print("🔧 创建 output 目录...")
    try:
        if not os.path.exists("output"):
            os.makedirs("output")
            print("✅ output 目录创建完成")
        else:
            print("✅ output 目录已存在")
    except Exception as e:
        print(f"❌ 创建 output 目录失败: {e}")
        sys.exit(1)
    
    # 步骤4: 验证安装
    print("\n🔍 验证安装...")
    
    # 检查关键模块是否可以导入
    modules_to_check = [
        ("markdown", "Markdown 处理"),
        ("playwright", "Playwright 浏览器自动化"),
        ("PIL", "图片处理"),
        ("pygments", "代码语法高亮")
    ]
    
    all_ok = True
    for module, description in modules_to_check:
        try:
            __import__(module)
            print(f"✅ {description} 模块加载成功")
        except ImportError:
            print(f"❌ {description} 模块加载失败")
            all_ok = False
    
    print("=" * 50)
    
    if all_ok:
        print("🎉 安装完成！所有依赖都已成功安装。")
        print("\n📚 使用方法:")
        print("  # Markdown 转 HTML")
        print("  python md2html.py input.md output.html")
        print("\n  # HTML 转图片")
        print("  python html2image.py input.html output.png")
        print("\n  # Markdown 直接转图片")
        print("  python md2image.py input.md output.png")
        print("\n  # 运行功能演示")
        print("  python 示例用法.py")
        print("\n📖 详细文档请查看 README.md")
    else:
        print("❌ 安装过程中出现错误，请检查上述问题后重试。")
        sys.exit(1)


if __name__ == "__main__":
    main() 