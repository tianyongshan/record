import zipfile
import os
import re
from bs4 import BeautifulSoup

def sanitize_text(text):
    # 清除特殊字符，替换空格和换行符为下划线
    text = re.sub(r'[<>:"/\\|?*]', '_', text)  # 替换文件名中的特殊字符
    text = re.sub(r'\s+', '_', text)  # 替换多个空白字符为下划线
    return text.strip('_')  # 去掉开头和结尾的下划线

def get_line(content, line_number):
    # 获取指定行内容，line_number 从0开始
    lines = content.splitlines()
    return lines[line_number] if len(lines) > line_number else ""  # 返回指定行

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

                    # 获取章节内容
                    content = soup.get_text(separator='\n', strip=True)

                    # 获取章节的第二行和第三行
                    second_line = get_line(content, 1)  # 获取第二行
                    third_line = get_line(content, 2)   # 获取第三行
                    
                    # 合并第二行和第三行作为标题
                    merged_title = f"{second_line} {third_line}".strip()
                    
                    # 清理合并后的文本
                    sanitized_title = sanitize_text(merged_title)
                    
                    # 限制标题长度，截取部分内容
                    max_length = 30  # 设置最大长度
                    if len(sanitized_title) > max_length:
                        sanitized_title = sanitized_title[:max_length] + '...'  # 添加省略号
                    
                    # 输出拆分内容
                    print(sanitized_title)
                    
                    # 准备写入 Markdown 文件
                    md_file_name = f"{sanitized_title}.md"  # 使用合并后的标题作为文件名
                    md_file_path = os.path.join(output_dir, md_file_name)

                    # 优化内容（替换 ; 和 ； 为 .）
                    optimized_content = optimize_content(content)

                    # 写入文件，同时保留换行
                    with open(md_file_path, 'w', encoding='utf-8') as md_file:
                        md_file.write(f"# {sanitized_title}\n\n")  # 写入标题
                        # 将内容中多余的换行符和连续空行处理为 Markdown 的换行
                        md_file.write(optimized_content.replace('\n', '\n\n'))  # 保留换行
                        
                    print(f"章节 '{sanitized_title}' 内容已写入文件: {md_file_path}\n")
                    print(f"章节内容:\n{optimized_content}\n")
                    print("=" * 80)  # 分隔符

# 示例使用
epub_file_path = '《王小波作品大全集（套装15册）》.epub'   
output_directory = 'output_md_files'  # 指定输出目录
os.makedirs(output_directory, exist_ok=True)  # 创建输出目录（如果不存在）
parse_epub(epub_file_path, output_directory)
