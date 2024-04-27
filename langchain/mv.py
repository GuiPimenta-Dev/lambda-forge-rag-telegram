import os
import shutil
from random import shuffle

source_folder = '/Users/guialves/personal_projects/lforge/lambda-forge-rag/langchain/python'
destination_folder = './Users/guialves/personal_projects/lforge/lambda-forge-rag/langchain/python3'

files = os.listdir(source_folder)
shuffle(files)
half = len(files) // 2

for file in files[:half]:
    shutil.move(os.path.join(source_folder, file), destination_folder)
