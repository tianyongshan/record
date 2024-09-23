import subprocess

for port in range(9050, 9058):
    command = f'"C:\\Users\\12703\\Desktop\\chrome-win64\\chrome-win64\\chrome.exe" -remote-debugging-port={port} --user-data-dir="C:\\Users\\12703\\AppData\\Roaming\\Google\\Chrome\\User Data\\Default{port}"'
    subprocess.Popen(command, shell=True)
