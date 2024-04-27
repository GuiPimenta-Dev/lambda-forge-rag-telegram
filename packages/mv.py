import os
import shutil
from random import shuffle

source_folder = '/Users/guialves/personal_projects/lforge/lambda-forge-rag/packages/python'
destination_folder = './second-half'

files = os.listdir(source_folder)
shuffle(files)
half = len(files) // 2

for file in files[:half]:
    try:
        shutil.move(os.path.join(source_folder, file), destination_folder)
    except:
        pass

