import numpy as np
from keras import backend as K
from keras.applications import vgg16
from keras.preprocessing.image import load_img, img_to_array

def time_function(f, *args):
	"""
	Call a function f with args and return the time
	(in seconds) that it took to execute.
	"""
	tic = time.time()
	f(*args)
	toc = time.time()
	return toc - tic

# util function to open, resize and format pictures into appropriate tensors
def preprocess_image(image_path, desired_dims):
	img = load_img(image_path, target_size=desired_dims)
	img = img_to_array(img)
	img = np.expand_dims(img, axis=0)
	img = vgg16.preprocess_input(img)
	return img

# util function to convert a tensor into a valid image
def deprocess_image(x, img_nrows, img_ncols):
	x = x.reshape((img_nrows, img_ncols, 3))
	# Remove zero-center by mean pixel
	x[:, :, 0] += 103.939
	x[:, :, 1] += 116.779
	x[:, :, 2] += 123.68
	# 'BGR'->'RGB'
	x = x[:, :, ::-1]
	x = np.clip(x, 0, 255).astype('uint8')
	return x
