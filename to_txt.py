import os
import logging
from tqdm import tqdm

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 白名单目录
whitelist = ['柏杨']

def process_directory(root_dir, output_file):
    chapter_num = 1
    for top_dir in whitelist:
        dir_path = os.path.join(root_dir, top_dir)
        if not os.path.isdir(dir_path):
            logging.warning(f"目录 {dir_path} 不存在，跳过")
            continue

        output_file.write(f"第{chapter_num}章 {top_dir}\n")
        section_num = 1

        for root, dirs, files in os.walk(dir_path):
            dirs.sort()  # 确保子目录按字母顺序处理
            files.sort()  # 确保文件按字母顺序处理

            relative_path = os.path.relpath(root, dir_path)
            is_subdirectory = relative_path != '.'

            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as md_file:
                        content = md_file.read()

                    if is_subdirectory:
                        output_file.write(f"第{section_num}节 {os.path.splitext(file)[0]}[{os.path.basename(root)}]\n")
                    else:
                        output_file.write(f"第{section_num}节 {os.path.splitext(file)[0]}\n")
                    output_file.write(content + "\n\n")
                    section_num += 1

        chapter_num += 1

def main():
    root_directory = '.'  # 当前目录
    output_filename = '柏杨.txt'

    with open(output_filename, 'w', encoding='utf-8') as output_file:
        process_directory(root_directory, output_file)

    logging.info(f"合并完成，输出文件: {output_filename}")

if __name__ == "__main__":
    main()
