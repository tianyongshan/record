import os
import shutil

# Get all directories in the current folder
directories = [d for d in os.listdir() if os.path.isdir(d)]

# Process each directory
for dir_name in directories:
    if dir_name.startswith('2024年'):
        # Extract the year and month
        new_dir_name = dir_name[:6]
        
        # Create the new directory if it doesn't exist
        if not os.path.exists(new_dir_name):
            os.makedirs(new_dir_name)
        
        # Move contents to the new directory
        for item in os.listdir(dir_name):
            shutil.move(os.path.join(dir_name, item), new_dir_name)
        
        # Remove the old directory
        os.rmdir(dir_name)

print("处理完成。")
