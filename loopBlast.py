import time
import os

time.sleep(1)

i=0
while (i < 120):
    i += 1
    os.system("wget https://admin.scaninsystem.com/upload.php &")
