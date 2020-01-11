import time
import numpy as np

from keras import backend as K
from keras.applications import vgg16
from keras.preprocessing.image import load_img

from imageio import imwrite
from PIL import Image
from scipy.optimize import fmin_l_bfgs_b

from ml_deploy_demo.util.utils import preprocess_image, deprocess_images

# Part 1: Content loss
# Compute the loss of two feature inputs
def feature_reconstruction_loss(base, output):

	return K.sum(K.square(base - output))

# Part 2: Style loss
# Compute the Gram matrix of a given keras tensor
def gram_matrix(x):
	w, h, c = x.shape
	x = K.reshape(x, shape=(int(w*h), int(c)))

	return K.dot(K.transpose(x), x)

# Part 3: Style loss: layer's loss
# Compute the loss for a given layer
def style_reconstruction_loss(base, output):
	w, h = base.shape[:-1]
	G_base = gram_matrix(base)
	G_output = gram_matrix(output)
	l2_norm = K.sum(K.square(G_base - G_output))

	return l2_norm / (4*int(w*h)**2)

# Part 4: Total-variation regularization
# Add smoothness in the image using a total-variation regularizer
def total_variation_loss(x):
	term1 = K.sum(K.square(x[:, :-1, 1:, :] - x[:, :-1, :-1, :]))
	term2 = K.sum(K.square(x[:, 1:, :-1, :] - x[:, :-1, :-1, :]))

	return term1 + term2

# Part 5: Color preservation
# Helper function to convert RGB to grayscale
def rgb2gray(rgb):
	return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

# Helper function to convert grayscale to RGB
def gray2rgb(gray):
	w, h = gray.shape
	rgb = np.empty((w, h, 3), dtype=np.float32)
	rgb[:, :, 2] = rgb[:, :, 1] = rgb[:, :, 0] = gray
	return rgb

# Part 6: Style transfer
def style_transfer(base_img_path, style_img_path, output_img_path, convnet='vgg16',
	content_weight=3e-2, style_weights=(20000, 500, 12, 1, 1), tv_weight=5e-2, content_layer='block4_conv2',
	style_layers=['block1_conv1', 'block2_conv1', 'block3_conv1', 'block4_conv1', 'block5_conv1'],
	iterations=50, preserve_color=True):

	print('\nInitializing Neural Style model...')

	# Determine the image sizes. Fix the output size from the content image.
	width, height = load_img(base_img_path).size
	new_dims = (height, width)

	# Preprocess content and style images. Resizes the style image if needed.
	content_img = K.variable(preprocess_image(base_img_path, new_dims))
	style_img = K.variable(preprocess_image(style_img_path, new_dims))

	# Create an output placeholder with desired shape.
	# It will correspond to the generated image after minimizing the loss function.
	output_img = K.placeholder((1, height, width, 3))

	# Combine the three images into a single Keras tensor.
	# The first dimension of a tensor identifies the example/input.
	input_img = K.concatenate([content_img, style_img, output_img], axis=0)

	# Initialize the vgg16 model
	print('\tLoading {} model'. format(convnet.upper()))
	model = vgg16.VGG16(input_tensor=input_img, weights='imagenet', include_top=False)

	print('\tComputing losses...')
	# Get the symbolic outputs of each "key" layer (they have unique names).
	# The dictionary outputs an evaluation when the model is fed an input.
	outputs_dict = dict([(layer.name, layer.output) for layer in model.layers])

	# Extract features from the content layer.
	content_features = outputs_dict[content_layer]

	# Extract the activations of the base image and the output image.
	base_image_features = content_features[0, :, :, :] # 0 corresponds to base
	combination_features = content_features[2, :, :, :] # 2 corresponds to output

	# Calculate the feature reconstruction loss
	content_loss = content_weight * feature_reconstruction_loss(base_image_features, combination_features)

	# For each style layer compute style loss
	# The total style loss is the weighted sum of those losses
	temp_style_loss = K.variable(0.0) # This variable will be updated in the loop
	weight = 1.0 / float(len(style_layers))

	for i, layer in enumerate(style_layers):
		# Extract features of given layer.
		style_features = outputs_dict[layer]
		# Extract style and output activations from these features.
		style_image_features = style_features[1, :, :, :] # 1 corresponds to style image
		output_style_features = style_features[2, :, :, :] # 2 corresponds to generated image
		temp_style_loss = temp_style_loss + style_weights[i] * weight * \
						style_reconstruction_loss(style_image_features, output_style_features)
	style_loss = temp_style_loss

	# Compute total variational loss.
	tv_loss = tv_weight * total_variation_loss(output_img)

	# Composite loss.
	total_loss = content_loss + style_loss + tv_loss

	# Compute gradients of output img with respect to total_loss.
	print('\tComputing gradients...')
	grads = K.gradients(total_loss, output_img)
	outputs = [total_loss] + grads
	loss_and_grads = K.function([output_img], outputs)

	# Initialize the generated image from random choice
	x = np.random.uniform(0, 255, (1, height, width, 3)) - 128.

	# Loss function that takes a vectorized input iamge for the solver.
	def loss(x):
		x = x.reshape((1, height, width, 3))
		return loss_and_grads([x])[0]

	# Gradient function that takes a vectorized input image for the solver.
	def grads(x):
		x = x.reshape((1, height, width, 3))
		return loss_and_grads([x])[1].flatten().astype('float64')

	# Fit over the total iterations.
	for i in range(iterations+1):
		print('\n\tIteration: {}'.format(i+1))

		toc = time.time()
		x, min_val, info = fmin_l_bfgs_b(loss, x.flatten(), fprime=grads, maxfun=20)

		# Save current generated image.
		if i%10 == 0:
			img = deprocess_image(x.copy(), height, width)
			fname = output_img_path + '_at_iteration_%d.png' % (i)

			if preserve_color:
				# Luminosity only color preservation.
				content_image = load_img(base_img_path)
				original_image = np.clip(content_image, 0, 255)
				styled_image = np.clip(img, 0, 255)
				# Convert stylized RGB to grayscale
				styled_gray = rgb2gray(styled_image)
				styled_gray_rgb = gray2rgb(styled_gray)
				# Convert stylized grayscale into YCbCr
				styled_gray_ycc = np.array(Image.fromarray(styled_gray_rgb.astype(np.uint8)).convert('YCbCr'))
				# Convert original image into YCbCr
				original_ycc = np.array(Image.fromarray(original_image.astype(np.uint8)).convert('YCbCr'))
				# Recombine
				w, h, _ = original_image.shape
				combined_ycc = np.empty((w, h, 3), dtype=np.uint8)
				combined_ycc[..., 0] = styled_gray_ycc[..., 0]
				combined_ycc[..., 1] = original_ycc[..., 1]
				combined_ycc[..., 2] = original_ycc[..., 2]
				# Convert recombined image from YCbCr back to RGB
				img = np.array(Image.fromarray(combined_ycc, 'YCbCr').convert('RGB'))

			imwrite(fname, img)
			print('\t\tImage saved as', fname)

		tic = time.time()

		print('\t\tLoss: {:.2e}, Time: {} seconds'.format(float(min_val), float(tic-toc)))


if __name__ == '__main__':
    params = {
    	'base_img_path' : 'data/cat_frame1.png',
    	'style_img_path' : 'data/starry_night_small.jpg',
    	'output_img_path' : 'experiment_output/style_transfer/cat_frame1_starrynight',
    	'convnet' : 'vgg16',
    	'content_weight' : 300,
    	'style_weights' : (10, 10, 50, 10, 10),
    	'tv_weight' : 300,
    	'content_layer' : 'block4_conv2',
    	'style_layers' : ['block1_conv1',
    					  'block2_conv1',
    					  'block3_conv1',
    					  'block4_conv1',
    					  'block5_conv1'],
    	'iterations' : 50,
    	'preserve_color' : False
    }

    style_transfer(**params)
