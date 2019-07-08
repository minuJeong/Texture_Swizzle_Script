import numpy as np

import imageio as ii


test_img_diffuse = np.random.uniform(0, 255, (512, 512, 4)).astype(np.uint8)
test_img_normal = np.random.uniform(0, 255, (512, 512, 4)).astype(np.uint8)

test_img_diffuse[:, :, :] = (128, 32, 96, 255)
test_img_normal[:, :, :] = (196, 255, 128, 48)

ii.imwrite("textureSetA_D.png", test_img_diffuse)
ii.imwrite("textureSetA_N.png", test_img_normal)
