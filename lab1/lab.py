#!/usr/bin/env python3

import math

from PIL import Image as Image

# NO ADDITIONAL IMPORTS ALLOWED!


def get_pixel(image, x, y):
    y = y*image['width']
    
    if x < 0:
        x = 0
        #print('x 0 edge')
    if y < 0:
        y = 0
        #print('y 0 edge')
    if x > image['width']-1:
        x =  image['width']-1
        #print('x max edge')
    if y > (image['height']-1)*image['width']:
        y = (image['height']-1)*image['width']
        #print('y max edge',y)
    #print(x+y)
    return image['pixels'][x+y]


def set_pixel(image, c):
    image['pixels'].append(c)


def apply_per_pixel(image, func):
    result = result = copy(image)
    for y in range(image['height']):
        for x in range(image['width']):
            color = get_pixel(image, x, y)
            newcolor = func(color)
            set_pixel(result, newcolor)
    return result


def inverted(image):
    return apply_per_pixel(image, lambda c: 255-c)


# HELPER FUNCTIONS

def correlate(image, kernel):
    """
    Compute the result of correlating the given image with the given kernel.

    The output of this function should have the same form as a 6.009 image (a
    dictionary with 'height', 'width', and 'pixels' keys), but its pixel values
    do not necessarily need to be in the range [0,255], nor do they need to be
    integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE
    Need two parts of information from kernel
    List of pixel values []
    Length = nxn
    Odd number of rows and columns
    Square (nxn)
    """
    result = result = copy(image)
    n = int(math.sqrt(len(kernel)))
    offset = int(n//2)
    
    for y in range(image['height']):
        for x in range(image['width']):
            avg_value = 0
            for i in range(0-offset,offset+1):
                for j in range(0-offset,offset+1):
                    color = get_pixel(image, x+j, y+i)
                    avg_value += kernel[((i+offset)*n)+j+offset]*color
            set_pixel(result, avg_value)
    return result

def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    result = result = copy(image)
    for value in image['pixels']:
        randc = round(value)
        if randc < 0:
            randc = 0
        if randc > 255:
            randc = 255
        set_pixel(result, randc)  
    return result

# FILTERS

def blurred(image, n):
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)
    kernel = blur_kernel(n)

    # then compute the correlation of the input image with that kernel
    blurred_image = correlate(image,kernel)

    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    # print('pre rounding number of pixels:', len(blurred_image['pixels']))
    return round_and_clip_image(blurred_image)

def blur_kernel(n): 
    return [1/(n*n)]*(n*n)

def sharpened(image, n):
    result = copy(image)
    
    blurred_image = blurred(image,n)
    scaled_image = [2*value for value in image['pixels']]
    result['pixels'] = [scaled-blur for scaled, blur in zip(scaled_image, blurred_image['pixels'])]
    return round_and_clip_image(result)

def edges(image):
    result = copy(image)
    
    kx = [-1, 0, 1,
          -2, 0, 2,
          -1, 0, 1]
    
    ky = [-1, -2, -1,
           0,  0,  0,
           1,  2,  1]
    
    ox2 = [value*value for value in correlate(image,kx)['pixels']]
    oy2 = [value*value for value in correlate(image,ky)['pixels']]
    result['pixels'] = [round(math.sqrt(ox2_val + oy2_val)) for ox2_val, oy2_val in zip(ox2,oy2)]
    return round_and_clip_image(result)
    
def copy(image):
    return {
        'height': image['height'],
        'width': image['width'],
        'pixels': []
    }

# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    #bluegill = load_image('test_images/bluegill.png')
    #save_image(inverted(bluegill),'test_results/inv_bluegill.png')
    
    # kernel = [0, 0, 0, 0, 0, 0, 0, 0, 0,
    #           0, 0, 0, 0, 0, 0, 0, 0, 0,
    #           1, 0, 0, 0, 0, 0, 0, 0, 0,
    #           0, 0, 0, 0, 0, 0, 0, 0, 0,
    #           0, 0, 0, 0, 0, 0, 0, 0, 0,
    #           0, 0, 0, 0, 0, 0, 0, 0, 0,
    #           0, 0, 0, 0, 0, 0, 0, 0, 0,
    #           0, 0, 0, 0, 0, 0, 0, 0, 0,
    #           0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    # pigbird = load_image('test_images/pigbird.png')
    # correlated = correlate(pigbird,kernel)
    # clipped = round_and_clip_image(correlated)
    # save_image(clipped,'test_results/correlated_pigbird.png')
    
    # cat = load_image('test_images/cat.png')
    # save_image(blurred(cat,5),'test_results/blurred_cat.png')
    
    # expected = {
    #     'height': 11,
    #     'width': 11,
    #     'pixels': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                0, 0, 0, 0, 28, 28, 28, 0, 0, 0, 0,
    #                0, 0, 0, 0, 28, 28, 28, 0, 0, 0, 0,
    #                0, 0, 0, 0, 28, 28, 28, 0, 0, 0, 0,
    #                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # }
    # save_image(expected,'test_results/centered_pixel_blur_03.png')
    
    python = load_image('test_images/python.png')
    save_image(sharpened(python,11),'test_results/sharpened_python.png')
    
    center = load_image('test_images/centered_pixel.png')
    save_image(edges(center),'test_results/edge_centered_pixel.png')