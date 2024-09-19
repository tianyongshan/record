import os

# Define the directory containing the files
directory = '.'

# Open (or create) the output file to write the prefixes
with open('prefixes.txt', 'w', encoding='utf-8') as output_file:
    # Loop through each file in the directory
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            # Find the position of the character ':' or '：'
            pos = filename.find(':')
            if pos == -1:  # If ':' is not found, look for '：'
                pos = filename.find('：')
            
            # If one of the characters was found
            if pos != -1:
                # Extract the prefix
                prefix = filename[:pos]
                # Write the prefix to the output file
                output_file.write(prefix + '\n')
