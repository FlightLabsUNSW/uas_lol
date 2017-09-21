import os
import shutil


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            if not (".exe" in item):
                shutil.copy2(s, d)


copytree("C:/Users/simon/Documents/test_images", "D:/images")
