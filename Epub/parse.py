import zipfile
import os
import re
from bs4 import BeautifulSoup

def sanitize_text(text):
    # 清除特殊字符，替换空格和换行符为下划线
    text = re.sub(r'[<>:"/\\|?*]', '_', text)  # 替换文件名中的特殊字符
    text = re.sub(r'\s+', '_', text)  # 替换多个空白字符为下划线
    return text.strip('_')  # 去掉开头和结尾的下划线

def get_second_line(content):
    # 获取文本的第二行
    lines = content.splitlines()
    return lines[1] if len(lines) > 1 else ""  # 如果有第二行则返回，否则返回空字符串

def optimize_content(content):
    # 替换 ; 和 ； 为 .
    content = content.replace(';', '.').replace('；', '.')
    return content

def parse_epub(file_path, output_dir):
    # 确保文件存在
    if not os.path.exists(file_path):
        print("文件不存在:", file_path)
        return

    # 使用 zipfile 打开 EPUB 文件
    with zipfile.ZipFile(file_path, 'r') as ebook:
        # 遍历每个文件
        for item in ebook.namelist():
            # 找到 XHTML 文件
            if item.endswith('.xhtml') or item.endswith('.html'):
                with ebook.open(item) as file:
                    # 读取并解析 HTML 内容
                    soup = BeautifulSoup(file.read(), 'lxml')

                    # 获取章节标题（如果需要的话）
                    title = soup.find(['h1', 'h2', 'h3'])
                    title_text = title.get_text(strip=True) if title else "无标题"

                    # 获取章节内容
                    content = soup.get_text(separator='\n', strip=True)
                    
                    # 获取章节内容的第二行
                    second_line = get_second_line(content)
                    
                    # 清理第二行文本
                    sanitized_second_line = sanitize_text(second_line)
                    
                    # 限制内容长度，截取部分内容
                    max_length = 100  # 设置最大长度
                    if len(sanitized_second_line) > max_length:
                        sanitized_second_line = sanitized_second_line[:max_length] + '...'  # 添加省略号
                    
                    # 输出拆分内容
                    print(sanitized_second_line)

                    # 准备写入 Markdown 文件
                    md_file_name = sanitize_text(sanitized_second_line) + '.md'  # 使用标题作为文件名
                    md_file_path = os.path.join(output_dir, md_file_name)

                    # 优化内容（替换 ; 和 ； 为 .）
                    optimized_content = optimize_content(content)
                    
                    # 写入文件
                    with open(md_file_path, 'w', encoding='utf-8') as md_file:
                        md_file.write(f"# {sanitized_second_line}\n\n")
                        md_file.write(optimized_content)  # 写入保留换行的内容
                        
                    print(f"章节 '{sanitized_second_line}' 内容已写入文件: {md_file_path}\n")
                    print(f"章节 '{sanitized_second_line}' 内容:\n{optimized_content}\n")
                    print("=" * 80)  # 分隔符

# 示例使用
epub_file_path = '宪在：生活中的宪法踪迹.epub'   
output_directory = 'output_md_files'  # 指定输出目录
os.makedirs(output_directory, exist_ok=True)  # 创建输出目录（如果不存在）
parse_epub(epub_file_path, output_directory)
