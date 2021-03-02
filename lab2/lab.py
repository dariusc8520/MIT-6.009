#!/usr/bin/env python3

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
from PIL import Image

def get_pixel(image, x, y):
    """
    Retrieves the pixel value from image
    Will keep requested pixel values within the bounds of the image
    """
    y = y*image['width'] #Necessary to multiply by width for correct indexing in a list
    
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if x > image['width']-1:
        x =  image['width']-1
    if y > (image['height']-1)*image['width']:
        y = (image['height']-1)*image['width']
        
    return image['pixels'][x+y]


def set_pixel(image, c):
    """
    Should be called when you have an empty list you are updating with new values
    """
    image['pixels'].append(c)


def apply_per_pixel(image, func):
    """
    Applies a function to every pixel in an image
    """
    result = copy(image)
    for y in range(image['height']):
        for x in range(image['width']):
            color = get_pixel(image, x, y)
            newcolor = func(color)
            set_pixel(result, newcolor)
    return result


def inverted(image):
    """
    Inverts every pixel value in an image
    """
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
    offset = int(n//2) #Offset necessary for kernel index range
    #iterates through all pixels in image
    #Did not use apply per pixel because I had modifications to the index
    for y in range(image['height']):
        for x in range(image['width']):
            avg_value = 0
            #Iterates through indexs of the kernel
            for j in range(0-offset,offset+1):
                for i in range(0-offset,offset+1):
                    #Looks for pixel value with offsets from the kernel
                    color = get_pixel(image, x+i, y+j)
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
    result = copy(image)
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
    return round_and_clip_image(blurred_image)

def blur_kernel(n): 
    """
    Returns a kernel that is a list with n x n equal values of 1/(n*n)
    """
    return [1/(n*n)]*(n*n)

def sharpened(image, n):
    """
    Returns a sharpened image by taking the the difference between a scaled image and a blurred image
    Takes in an n value for the blur kernel
    """
    result = copy(image)
    
    blurred_image = blurred(image,n)
    scaled_image = [2*value for value in image['pixels']]
    result['pixels'] = [scaled-blur for scaled, blur in zip(scaled_image, blurred_image['pixels'])]
    return round_and_clip_image(result)

def edges(image):
    """
    Returns an image after applying a Sobel operator on the image
    The image will have edges highlighted
    """
    result = copy(image)
    kx = [-1, 0, 1, #Highlights differences in the x direction
          -2, 0, 2,
          -1, 0, 1]
    
    ky = [-1, -2, -1, #Highlights differences in the y direction
           0,  0,  0,
           1,  2,  1]
    #Applies the correlation to the image and squares each value in the pixel list
    ox2 = [value*value for value in correlate(image,kx)['pixels']] 
    oy2 = [value*value for value in correlate(image,ky)['pixels']]
    #Rounds the values after taking a squared summation
    result['pixels'] = [round(math.sqrt(ox2_val + oy2_val)) for ox2_val, oy2_val in zip(ox2,oy2)]
    return round_and_clip_image(result)
    
def copy(image):
    """
    Provides a shallow copy of the image to be worked with
    Returns a dictionary with the same height, width, and an empty pixels list
    """
    return {'height': image['height'], 'width': image['width'], 'pixels': [] }
# VARIOUS FILTERS
def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    raise NotImplementedError


def make_blur_filter(n):
    raise NotImplementedError


def make_sharpen_filter(n):
    raise NotImplementedError


def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """
    raise NotImplementedError


# SEAM CARVING

# Main Seam Carving Implementation

def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image.
    """
    raise NotImplementedError


# Optional Helper Functions for Seam Carving

def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    raise NotImplementedError


def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    raise NotImplementedError


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy
    function), computes a "cumulative energy map" as described in the lab 2
    writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    raise NotImplementedError


def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    raise NotImplementedError


def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    raise NotImplementedError


# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES

def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img = img.convert('RGB')  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_color_image(image, filename, mode='PNG'):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode='RGB', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
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


def save_greyscale_image(image, filename, mode='PNG'):
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
    pass
