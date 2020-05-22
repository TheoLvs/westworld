
import numpy as np

def image3d_to_mask(img,threshold = 0.5):
    mask = 1 - np.int8((np.max(img,axis = 2) / 255 ) > threshold)
    return mask


def snap_mask_to_grid(mask,box_size,threshold = 0.5):

    new_mask = np.copy(mask)
    width = mask.shape[0] // box_size
    height = mask.shape[1] // box_size

    for x in range(width):
        for y in range(height):
            index = np.s_[x*box_size:(x+1)*box_size,y*box_size:(y+1)*box_size]
            submask = mask[index]
            if submask.mean() > threshold:
                new_mask[index] = 1
            else:
                new_mask[index] = 0

    return new_mask


def mask_to_image3d(mask):
    return np.repeat((1 - mask[:,:,np.newaxis])*255,3,axis = 2)


def aggregate_mask_to_grid(mask,box_size,threshold = None):

    width = mask.shape[0] // box_size
    height = mask.shape[1] // box_size
    new_mask = np.zeros((width,height))

    for x in range(width):
        for y in range(height):
            index = np.s_[x*box_size:(x+1)*box_size,y*box_size:(y+1)*box_size]
            submask_mean = mask[index].mean()

            if threshold is None:
                new_mask[x,y] = submask_mean
            else:
                assert 0 < threshold < 1
                new_mask[x,y] = int(submask_mean > threshold)

    return new_mask
