
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


def mesh_to_mask(mesh,box_size):
    """Transform a numpy array to another numpy array but with each cell repeated box_size times
    Useful when we have a navigation mesh or a maze where each value in the numpy array represents one cell
    and we want to convert to image where each value is a pixel, ie each value is repeated box_size pixel times


    Args:
        mask (np.ndarray): A numpy array with 0 and 1 representing obstacles
        box_size (int): the size for each square cell in the grid
    """

    w,h = mesh.shape
    new_w,new_h = w * box_size,h*box_size
    mask = np.zeros((new_w,new_h))

    for x in range(w):
        for y in range(h):
            index = np.s_[x*box_size:(x+1)*box_size,y*box_size:(y+1)*box_size]
            mask[index] = mesh[x,y]

    mask = mask.astype(np.int8)
    return mask



def mask_to_mesh(mask,box_size,threshold = None):

    width = mask.shape[0] // box_size
    height = mask.shape[1] // box_size
    mesh = np.zeros((width,height))

    for x in range(width):
        for y in range(height):
            index = np.s_[x*box_size:(x+1)*box_size,y*box_size:(y+1)*box_size]
            submask_mean = mask[index].mean()

            if threshold is None:
                mesh[x,y] = submask_mean
            else:
                assert 0 < threshold < 1
                mesh[x,y] = int(submask_mean > threshold)

    return mesh
