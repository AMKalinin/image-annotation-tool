import h5py
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = 933120000
import math


with h5py.File('test.hdf', 'w') as hdf:
    hdf.copy()
    img = Image.open('/home/akalinin/Downloads/Telegram Desktop/fbig_most17_resize_1m.tif')
    # img = Image.open('/home/akalinin/Downloads/Безымянны.png')
    img_icon = img.resize((100,100))

    grp = hdf.create_group("task1")

    # task = grp.create_dataset('orig_img', data=np.asarray(img, dtype='uint8'))
    task = grp.create_dataset('icon_img', data=np.asarray(img_icon, dtype='uint8'))
    
    w = img.size[0]
    h = img.size[1]
    col_layer = 0
    while w>1000 or h>1000:
        col_layer += 1
        w /= 2
        h /= 2
    for i in range(col_layer):
        if i == 0:
            desc = 1
        else:
            desc = 2
        width = int(img.size[0]/(desc))
        height = int(img.size[1]/(desc))
        img = img.resize((width, height))
        
        layer = grp.create_group(f"layer_{i+1}")
        for sampl_h in range(math.ceil(height/256)):
            for sampl_w in range(math.ceil(width/256)):
                start_p = [sampl_w*256, sampl_h*256]
                end_p = [(sampl_w+1)*256, (sampl_h+1)*256]
                if ((sampl_w+1)*256) > width:
                    end_p[0] = width
                if ((sampl_h+1)*256) > height:
                    end_p[1] = height
                sample = img.crop((start_p[0],start_p[1], end_p[0], end_p[1]))
                layer.create_dataset(f'{sampl_h}:{sampl_w}', data=np.asarray(sample, dtype='uint8'))



# with h5py.File('test.hdf', 'r') as hdf:
#     grp = hdf.get('task1')
#     layer = grp.get('layer_1')
#     im00 = np.array(layer.get('0:0'))
#     im01 = np.array(layer.get('0:1'))
#     im02 = np.array(layer.get('0:2'))
#     im0010 = np.hstack((im00, im01,im02))

#     im10 = np.array(layer.get('1:0'))
#     im11 = np.array(layer.get('1:1'))
#     im12 = np.array(layer.get('1:2'))
#     im1011 = np.hstack((im10, im11, im12))
#     im_i = np.vstack((im0010, im1011))
# # plot
# fig, ax = plt.subplots()
# ax.imshow(im_i)

# plt.show()
