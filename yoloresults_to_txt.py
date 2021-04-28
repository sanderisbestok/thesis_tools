import os
import sys

ROOT_DIR = "../results/yolov5"

for dir_name in os.listdir(ROOT_DIR):
    for file_name in os.listdir(os.path.join(ROOT_DIR, dir_name)):
        
        with open(os.path.join(ROOT_DIR, dir_name, file_name), "r") as reading_file:
    
            new_file_content = ""
            for line in reading_file:
                stripped_line = line.strip()
                stripped_line = stripped_line.split()
                
                stripped_line.insert(1, stripped_line.pop(5))
                
                stripped_line = " ".join(stripped_line)
                
                new_line = stripped_line.replace("0 ", "1 ")
                new_file_content += new_line +"\n"

            with open(os.path.join(ROOT_DIR, dir_name, file_name), "w") as writing_file:
                writing_file.write(new_file_content)