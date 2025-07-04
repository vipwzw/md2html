import sys
import os
import re
import tempfile
import shutil
from markdown import markdown
import base64
from sympy import preview
from PIL import Image


def latex_to_image_sympy(latex_code, output_path, fontsize=12, dpi=800, is_inline=False):
    """
    使用sympy的preview函数将LaTeX数学公式转换为高质量PNG图片
    """
    try:
        # 准备LaTeX代码
        if not latex_code.startswith('$'):
            if is_inline:
                latex_expr = f'${latex_code}$'
            else:
                latex_expr = f'$${latex_code}$$'
        else:
            latex_expr = latex_code
        
        # 使用高质量PNG直接生成
        base_path = os.path.splitext(output_path)[0]
        
        # 尝试使用高DPI参数
        try:
            preview(latex_expr, filename=base_path, viewer='file', 
                   dvioptions=[f'-D {dpi}', '-T tight'])
            
            if os.path.exists(base_path):
                shutil.move(base_path, output_path)
                print(f"Sympy 超高清PNG 成功生成图片: {output_path} (DPI: {dpi})")
                return True
        except:
            # 如果高级参数失败，使用基本模式
            preview(latex_expr, filename=base_path, viewer='file')
            
            if os.path.exists(base_path):
                shutil.move(base_path, output_path)
                print(f"Sympy PNG 成功生成图片: {output_path}")
                return True
        
        print(f"Sympy 生成图片失败: {latex_code}")
        return False
            
    except Exception as e:
        print(f"Sympy 渲染错误: {e}")
        print(f"尝试降级到matplotlib...")
        # 如果sympy失败，降级到原来的matplotlib方法
        return latex_to_image_matplotlib(latex_code, output_path, fontsize, dpi, is_inline)


def latex_to_image_matplotlib(latex_code, output_path, fontsize=12, dpi=800, is_inline=False):
    """
    使用matplotlib将LaTeX数学公式转换为超高清PNG图片（备用方法）
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib
        
        # 配置matplotlib使用最佳渲染质量
        matplotlib.rcParams['figure.dpi'] = dpi
        matplotlib.rcParams['savefig.dpi'] = dpi
        matplotlib.rcParams['text.usetex'] = False
        matplotlib.rcParams['font.size'] = fontsize
        matplotlib.rcParams['text.antialiased'] = True
        matplotlib.rcParams['figure.facecolor'] = 'white'
        matplotlib.rcParams['savefig.facecolor'] = 'white'
        matplotlib.rcParams['savefig.edgecolor'] = 'white'
        matplotlib.rcParams['savefig.transparent'] = False
        # 使用Computer Modern字体，更接近LaTeX效果
        matplotlib.rcParams['mathtext.fontset'] = 'cm'
        matplotlib.rcParams['font.family'] = 'serif'
        
        fig, ax = plt.subplots(figsize=(1, 1), dpi=dpi)
        ax.axis('off')
        
        # 添加数学文本，使用超高质量渲染
        if not latex_code.startswith('$'):
            if is_inline:
                latex_expr = f'${latex_code}$'
            else:
                latex_expr = f'$${latex_code}$$'
        else:
            latex_expr = latex_code
            
        text = ax.text(0.5, 0.5, latex_expr, fontsize=fontsize, 
                      ha='center', va='center', transform=ax.transAxes,
                      antialiased=True)
        
        # 调整图片大小以适应文本
        fig.canvas.draw()
        bbox = text.get_window_extent(renderer=fig.canvas.get_renderer())
        bbox_inches = bbox.transformed(fig.dpi_scale_trans.inverted())
        
        # 添加一些边距
        padding = 0.1
        bbox_inches = bbox_inches.expanded(1 + padding, 1 + padding)
        
        # 保存为超高质量PNG
        plt.savefig(output_path, bbox_inches=bbox_inches, 
                   dpi=dpi, format='png', 
                   facecolor='white', edgecolor='white',
                   transparent=False, pad_inches=0.05)
        plt.close(fig)
        
        print(f"Matplotlib 超高清渲染成功: {output_path} (DPI: {dpi})")
        return True
        
    except Exception as e:
        print(f"Matplotlib 渲染错误: {e}")
        return False


# 重命名原函数为新的函数名
def latex_to_image(latex_code, output_path, fontsize=12, dpi=300, is_inline=False):
    """
    将LaTeX数学公式转换为PNG图片，优先使用sympy，失败时降级到matplotlib
    """
    return latex_to_image_sympy(latex_code, output_path, fontsize, dpi, is_inline)


def is_simple_inline_math(latex_code):
    """
    判断是否为简单的行内数学表达式，可以用文本替换
    """
    # 去除首尾空格
    code = latex_code.strip()
    
    # 包含复杂结构的不算简单
    complex_patterns = [
        r'\\begin\{',     # 环境（如矩阵）
        r'\\frac\{',      # 分数
        r'\\sqrt\{',      # 根号
        r'\\int',         # 积分
        r'\\sum',         # 求和
        r'\\prod',        # 乘积
        r'\\lim',         # 极限
        r'\{.*\}',        # 花括号（通常表示复杂结构）
        r'_\{.*\}',       # 复杂下标
        r'\^\{.*\}',      # 复杂上标
    ]
    
    for pattern in complex_patterns:
        if re.search(pattern, code):
            return False
    
    # 单个字母或数字
    if re.match(r'^[a-zA-Z0-9]$', code):
        return True
    
    # 简单的上标、下标
    simple_patterns = [
        r'^[a-zA-Z0-9]+\^[a-zA-Z0-9]$',       # 简单上标，如 x^2
        r'^[a-zA-Z0-9]+_[a-zA-Z0-9]$',        # 简单下标，如 x_i
        r'^[a-zA-Z0-9]+\^[a-zA-Z0-9]_[a-zA-Z0-9]$',  # 上下标组合
        r'^[a-zA-Z0-9]+_[a-zA-Z0-9]\^[a-zA-Z0-9]$',  # 下上标组合
    ]
    
    for pattern in simple_patterns:
        if re.match(pattern, code):
            return True
    
    # 检查是否只包含简单的希腊字母或数学符号
    simple_symbols = [
        '\\alpha', '\\beta', '\\gamma', '\\delta', '\\epsilon', 
        '\\theta', '\\lambda', '\\mu', '\\pi', '\\sigma', 
        '\\phi', '\\omega', '\\infty', '\\pm', '\\mp', 
        '\\times', '\\div', '\\leq', '\\geq', '\\neq', '\\approx'
    ]
    
    if code in simple_symbols:
        return True
    
    return False


def convert_simple_inline_math(latex_code):
    """
    将简单的行内数学表达式转换为Unicode或HTML实体
    """
    # 常见的数学符号替换
    replacements = {
        '\\alpha': 'α', '\\beta': 'β', '\\gamma': 'γ', '\\delta': 'δ',
        '\\epsilon': 'ε', '\\theta': 'θ', '\\lambda': 'λ', '\\mu': 'μ',
        '\\pi': 'π', '\\sigma': 'σ', '\\phi': 'φ', '\\omega': 'ω',
        '\\infty': '∞', '\\sum': '∑', '\\prod': '∏', '\\int': '∫',
        '\\pm': '±', '\\mp': '∓', '\\times': '×', '\\div': '÷',
        '\\leq': '≤', '\\geq': '≥', '\\neq': '≠', '\\approx': '≈',
        '\\sqrt': '√', '\\cdot': '·'
    }
    
    result = latex_code
    for latex_sym, unicode_sym in replacements.items():
        result = result.replace(latex_sym, unicode_sym)
    
    # 处理简单的上标（单个字符）
    result = re.sub(r'([a-zA-Z0-9])\^([a-zA-Z0-9])', 
                   lambda m: f'{m.group(1)}<sup>{m.group(2)}</sup>', result)
    
    # 处理简单的下标（单个字符）
    result = re.sub(r'([a-zA-Z0-9])_([a-zA-Z0-9])', 
                   lambda m: f'{m.group(1)}<sub>{m.group(2)}</sub>', result)
    
    return result


def extract_and_replace_math(content):
    """
    提取LaTeX数学公式并替换为超高清PNG图片
    注意：需要先保护代码块内容，避免误处理
    """
    if not os.path.exists('images'):
        os.makedirs('images')
    
    # 第一步：保护代码块内容
    code_blocks = []
    code_block_placeholder = "___CODE_BLOCK_PLACEHOLDER_{}_____"
    
    # 匹配代码块 (```language\n...```)
    def save_code_block(match):
        nonlocal code_blocks
        placeholder = code_block_placeholder.format(len(code_blocks))
        code_blocks.append(match.group(0))
        return placeholder
    
    # 保护三个反引号代码块
    protected_content = re.sub(r'```[\s\S]*?```', save_code_block, content, flags=re.MULTILINE)
    
    # 保护单行代码块
    inline_code_blocks = []
    inline_code_placeholder = "___INLINE_CODE_PLACEHOLDER_{}_____"
    
    def save_inline_code(match):
        nonlocal inline_code_blocks
        placeholder = inline_code_placeholder.format(len(inline_code_blocks))
        inline_code_blocks.append(match.group(0))
        return placeholder
    
    # 保护行内代码
    protected_content = re.sub(r'`[^`\n]+`', save_inline_code, protected_content)
    
    # 第二步：处理数学公式
    math_counter = 0
    
    # 处理块级数学公式 ($$...$$)
    def replace_block_math(match):
        nonlocal math_counter
        math_counter += 1
        latex_code = match.group(1).strip()
        
        print(f"处理块级公式 {math_counter}: {latex_code[:50]}...")
        
        # 生成超高清PNG
        img_path = f'images/math_block_{math_counter}.png'
        if latex_to_image(latex_code, img_path, fontsize=20, dpi=800, is_inline=False):
            # 计算图片的实际像素高度
            with Image.open(img_path) as img:
                original_width = img.width
                original_height = img.height
                display_height = original_height // 4  # 1/4高度
            
            print(f"  块级公式图片尺寸: {original_width}x{original_height}px -> 显示高度: {display_height}px")
            
            with open(img_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            # 块级公式使用计算出的1/4高度，宽度自适应
            img_html = f'<div class="math-block"><img src="data:image/png;base64,{img_data}" alt="Math formula" style="display: block; margin: 10px auto; height: {display_height}px; width: auto;"></div>'
            return img_html
        else:
            return f'<div class="math-error">Error rendering: {latex_code}</div>'
    
    # 处理行内数学公式 ($...$)
    def replace_inline_math(match):
        nonlocal math_counter
        math_counter += 1
        latex_code = match.group(1).strip()
        
        print(f"处理行内公式 {math_counter}: {latex_code}")
        
        # 生成超高清PNG（行内公式使用大字体）
        img_path = f'images/math_inline_{math_counter}.png'
        if latex_to_image(latex_code, img_path, fontsize=20, dpi=800, is_inline=True):
            with open(img_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            # 行内公式限制显示尺寸
            img_html = f'<img src="data:image/png;base64,{img_data}" alt="Math formula" style="display: inline; vertical-align: middle; max-height: 1.2em; height: auto; width: auto;">'
            return img_html
        else:
            return f'<span class="math-error">Error: {latex_code}</span>'
    
    # 现在可以安全地处理数学公式，因为代码块已经被保护
    processed_content = re.sub(r'\$\$(.*?)\$\$', replace_block_math, protected_content, flags=re.DOTALL)
    processed_content = re.sub(r'(?<!\$)\$([^$\n]+?)\$(?!\$)', replace_inline_math, processed_content)
    
    # 第三步：恢复代码块内容
    # 恢复行内代码
    for i, inline_code in enumerate(inline_code_blocks):
        placeholder = inline_code_placeholder.format(i)
        processed_content = processed_content.replace(placeholder, inline_code)
    
    # 恢复代码块
    for i, code_block in enumerate(code_blocks):
        placeholder = code_block_placeholder.format(i)
        processed_content = processed_content.replace(placeholder, code_block)
    
    return processed_content


def convert_local_images_to_base64(md_content, base_dir):
    """
    将本地图片转换为base64编码
    """
    # 匹配 ![alt](path) 格式的图片链接
    img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    
    def replace_image(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        
        # 如果是相对路径，转换为绝对路径
        if not os.path.isabs(img_path):
            full_path = os.path.join(base_dir, img_path)
        else:
            full_path = img_path
        
        # 检查文件是否存在
        if os.path.exists(full_path):
            try:
                # 根据文件扩展名确定MIME类型
                _, ext = os.path.splitext(full_path)
                ext = ext.lower()
                mime_types = {
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.gif': 'image/gif',
                    '.bmp': 'image/bmp',
                    '.webp': 'image/webp'
                }
                
                mime_type = mime_types.get(ext, 'image/png')
                
                # 读取图片并转换为base64
                with open(full_path, 'rb') as img_file:
                    img_data = img_file.read()
                    img_base64 = base64.b64encode(img_data).decode('utf-8')
                    
                # 返回base64编码的图片
                return f'<img src="data:{mime_type};base64,{img_base64}" alt="{alt_text}" style="max-width:100%; height:auto;">'
                
            except Exception as e:
                print(f"处理图片失败: {full_path}, 错误: {e}")
                return match.group(0)  # 保持原样
        else:
            print(f"图片文件不存在: {full_path}")
            return match.group(0)  # 保持原样
    
    return re.sub(img_pattern, replace_image, md_content)


def md_to_html_with_math_images(md_file, html_file):
    """
    将包含数学公式的Markdown文件转换为HTML文件
    数学公式会被转换为高质量的图片
    """
    try:
        # 确保输出文件在output目录中
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        
        # 如果html_file没有指定路径，放到output目录
        if not os.path.dirname(html_file):
            html_file = os.path.join(output_dir, html_file)
        
        # 读取markdown文件
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 创建临时目录存储图片
        temp_dir = 'images'
        os.makedirs(temp_dir, exist_ok=True)
        
        print(f"处理数学公式...")
        
        # 获取markdown文件的目录，用于处理相对路径的图片
        base_dir = os.path.dirname(os.path.abspath(md_file))
        
        # 先转换本地图片为base64
        md_content = convert_local_images_to_base64(md_content, base_dir)
        
        # 提取并替换数学公式
        md_content_with_images = extract_and_replace_math(md_content)
        
        # 转换为HTML
        html_content = markdown(md_content_with_images, extensions=[
            'tables',
            'fenced_code',
            'codehilite'
        ], extension_configs={
            'codehilite': {
                'css_class': 'highlight',
                'use_pygments': True,
                'noclasses': True  # 内联样式，不依赖外部CSS
            }
        })
        
        # 从文件名生成标题
        title = os.path.splitext(os.path.basename(md_file))[0]
        
        # 创建完整的HTML文档用于调试
        debug_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown转换调试</title>
    <style>
        body {{
            font-family: "Times New Roman", "SimSun", serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            color: #333;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-top: 2em;
            margin-bottom: 1em;
        }}
        p {{
            margin-bottom: 1em;
            text-align: justify;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: "Courier New", monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border: 1px solid #ddd;
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
            background-color: #f4f4f4;
            border-radius: 5px;
            padding: 15px;
            overflow-x: auto;
            border: 1px solid #ddd;
            margin: 16px 0;
        }}
        .highlight pre {{
            background-color: transparent;
            border: none;
            padding: 0;
            margin: 0;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-left: 0;
            font-style: italic;
            color: #666;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        /* 数学公式样式 */
        .math-block {{
            text-align: center;
            margin: 20px 0;
            padding: 10px;
        }}
        .math-block img {{
            display: block;
            margin: 0 auto;
            width: auto;
            /* 高度由Python动态计算设置 */
            /* 保持高质量缩放 */
            image-rendering: high-quality;
            image-rendering: -webkit-optimize-contrast;
            -ms-interpolation-mode: bicubic;
        }}
        .math-inline {{
            display: inline;
        }}
        .math-inline img {{
            display: inline;
            vertical-align: middle;
            max-height: 1.2em;
            height: auto;
            width: auto;
            /* 保持高质量缩放 */
            image-rendering: high-quality;
            image-rendering: -webkit-optimize-contrast;
            -ms-interpolation-mode: bicubic;
        }}
        .math-error {{
            color: red;
            background-color: #ffe6e6;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: monospace;
        }}
        /* 优化高DPI图片显示 */
        img[src*="base64"] {{
            image-rendering: high-quality;
            image-rendering: -webkit-optimize-contrast;
            -ms-interpolation-mode: bicubic;
        }}
        /* 针对数学公式图片的特殊优化 */
        .math-block img, .math-inline img {{
            image-rendering: high-quality;
            image-rendering: -webkit-optimize-contrast;
            -ms-interpolation-mode: bicubic;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
        
        # 保存HTML文件
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(debug_html)
        
        print(f"转换完成: {html_file}")
        print(f"数学公式图片已保存到: {temp_dir}/")
        print("转换成功!")
        
        return True
        
    except Exception as e:
        print(f"转换失败: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法: python md2html_with_images.py <input.md> <output.html>")
        print("功能:")
        print("  - 支持数学公式转换为高清图片")
        print("  - 支持本地图片base64编码")
        print("  - 生成完整的HTML文档")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"输入文件不存在: {input_file}")
        sys.exit(1)
    
    if md_to_html_with_math_images(input_file, output_file):
        print("转换成功!")
    else:
        print("转换失败!")
        sys.exit(1) 