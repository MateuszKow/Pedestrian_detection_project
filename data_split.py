import random
import glob
import os
import shutil

#kopiowanie plikow do katalogow
def copyfiles(fil, root_dir):
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]
    # image
    src = fil
    dest = os.path.join(root_dir, image_dir, f"{filename}.png")
    shutil.copyfile(src, dest)
    # label
    src = os.path.join(label_dir, f"{filename}.txt")
    dest = os.path.join(root_dir, label_dir, f"{filename}.txt")
    if os.path.exists(src):
        shutil.copyfile(src, dest)

# nazwy katalogow
label_dir = "labels/"
image_dir = "images/"
lower_limit = 0
#lista obrazkow
files = glob.glob(os.path.join(image_dir, '*.png'))
#losu losu
random.shuffle(files)
#podzial danych
folders = {"train": 0.8, "val": 0.1, "test": 0.1}
check_sum = sum([folders[x] for x in folders])
assert check_sum == 1.0, "Split proportion is not equal to 1.0"

print(files)

for folder in folders:
    #tworzenie osobnych folderow
    os.mkdir(folder)
    temp_label_dir = os.path.join(folder, label_dir)
    os.mkdir(temp_label_dir)
    temp_image_dir = os.path.join(folder, image_dir)
    os.mkdir(temp_image_dir)
    limit = round(len(files) * folders[folder])
    for fil in files[lower_limit:lower_limit + limit]:
        copyfiles(fil, folder)
    lower_limit = lower_limit + limit
