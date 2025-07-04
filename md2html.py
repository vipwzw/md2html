import sys
import os
from markdown import markdown


def md_to_html(md_path, html_path):
    # 读取md文件
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    # 转为HTML
    html_content = markdown(md_content, output_format='html5', extensions=[
        'mdx_math',
        'fenced_code',
        'codehilite',
        'tables'
    ], extension_configs={
        'codehilite': {
            'css_class': 'highlight',
            'use_pygments': True,
            'noclasses': True  # 内联样式，不依赖外部CSS
        }
    })
    
    # 创建完整的HTML文档
    filename = os.path.splitext(os.path.basename(md_path))[0]
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{filename}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-top: 1.5em;
        }}
        code {{
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            border: 1px solid #e1e4e8;
            line-height: 1.45;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
            font-size: 0.9em;
            line-height: inherit;
        }}
        /* 代码高亮样式优化 */
        .highlight {{
            background-color: #f8f9fa;
            border-radius: 6px;
            padding: 16px;
            overflow-x: auto;
            border: 1px solid #e1e4e8;
            margin: 16px 0;
        }}
        .highlight pre {{
            background-color: transparent;
            border: none;
            padding: 0;
            margin: 0;
        }}
        blockquote {{
            border-left: 4px solid #ddd;
            margin: 0;
            padding-left: 16px;
            color: #666;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 16px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: 600;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
    </style>
    <!-- MathJax for math formulas -->
    <script type="text/javascript" async
        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML">
    </script>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({{
            tex2jax: {{
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true
            }}
        }});
    </script>
</head>
<body>
{html_content}
</body>
</html>"""
    
    # 保存HTML文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)


def main():
    if len(sys.argv) != 3:
        print('用法: python md2html.py 输入文件.md 输出文件.html')
        sys.exit(1)
    md_path = sys.argv[1]
    html_path = sys.argv[2]
    if not os.path.isfile(md_path):
        print(f'输入文件不存在: {md_path}')
        sys.exit(1)
    md_to_html(md_path, html_path)
    print(f'转换完成: {html_path}')


if __name__ == '__main__':
    main() 