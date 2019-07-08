"""
MIT License
===========

Copyright (c) 2019 NexonGT Co.,Ltd

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Texture Channel Swizzler
========================

Requirements
---
- numpy==1.16.3
- imageio==2.5.0
- Pillow==6.1.0

Written and tested on
---
- Windows 10
- Python 3.7

How to use
---

Copy/move "swizzle.py" script into target textures directory and run with Python 3.7
Make sure texture sets are following naming conventions.
- diffuse texture ends with "*_D.[ext]".
- normal texture ends with "*_N.[ext]".
- each texture set must have matching names before _D/_N.
- upper/lower case can matters.
*[ext] is image file extension

Also, each texture set pair required to have matching resolution.


date: 7/8/2019
author: minu jeong
"""

import os

import numpy as np
import imageio as ii
from PIL import Image


def read_img(path):
    try:
        img = ii.imread(path)
        if img is not None:
            return img

    except Exception as e_general:
        try:
            # In case python can't read TGA directly from imageio,
            # try again to read with Pillow
            img = np.array(Image.open(path))
            if img is not None:
                return img

        except Exception as e_tga:
            print(e_tga)
            return None

        print(e_general)
        return None


class TextureInfo(object):

    def __init__(self, image, tag, extension, path):
        super(TextureInfo, self).__init__()

        self.image = image
        self.tag = tag
        self.extension = extension
        self.path = path


def process_pairs(diffuse_info, normal_info):
    if diffuse_info is None or normal_info is None:
        return None, None

    if diffuse_info.tag != normal_info.tag:
        print("diffuse and normal tex info tags are not matching")
        return None, None

    TAG = diffuse_info.tag
    print("processing TAG {}...".format(TAG))

    diffuse = diffuse_info.image
    normal = normal_info.image

    new_diffuse = np.ones(diffuse.shape).astype(np.uint8)
    new_normal = np.ones(normal.shape).astype(np.uint8)

    # ADD CUSTOM RULES HERE

    # copy diffuse RGB to new diffuse RGB
    new_diffuse[:, :, 0: 3] = diffuse[:, :, 0: 3]

    # diffuse A to new normal B
    new_normal[:, :, 2] = diffuse[:, :, 3]

    # normal R to new diffuse A
    new_diffuse[:, :, 3] = normal[:, :, 0]

    # normal G to new normal A
    new_normal[:, :, 3] = normal[:, :, 1]

    # normal B to new normal A
    new_normal[:, :, 3] = normal[:, :, 1]

    # normal A to normal G
    new_normal[:, :, 1] = normal[:, :, 3]

    ii.imwrite(diffuse_info.path, new_diffuse)
    ii.imwrite(normal_info.path, new_normal)

    print("...TAG {} is done!".format(TAG))


def main():
    matching_set = {}

    for filename in os.listdir("./"):
        img = read_img(filename)
        if img is None:
            continue

        splitted = filename.split(".")

        diffuse = None
        normal = None

        if splitted[-2].endswith("_D"):
            diffuse = img

        elif splitted[-2].endswith("_N"):
            normal = img

        if diffuse is None and normal is None:
            print("can't decide if file {} is diffuse normal.. skipped.".format(filename))
            continue

        tag = "_".join(filename.split("_")[:-1])
        extension = filename.split(".")[-1]
        path = "./{}".format(filename)
        if tag not in matching_set:
            matching_set[tag] = {}

        if diffuse is not None:
            matching_set[tag]["diffuse"] = TextureInfo(diffuse, tag, extension, path)

        elif normal is not None:
            matching_set[tag]["normal"] = TextureInfo(normal, tag, extension, path)

    for tag, pair in matching_set.items():
        process_pairs(pair["diffuse"], pair["normal"])


if __name__ == "__main__":
    main()
