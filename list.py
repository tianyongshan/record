import os

current_dir = 'D:\\.NewStart\\record'
folders = [f"'{folder}'" for folder in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, folder))]
result = ', '.join(folders)

print(result)
