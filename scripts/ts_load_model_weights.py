import caffe
import numpy as np 

caffe.set_mode_gpu()

# make sure the train data for the 2 different nets are different (e.g. train for trained_VGG and val for new_VGG
# because caffe will bug out otherwise

trained_alexnet = caffe.Net("Teacher-Student-Training/imagenet/alexnet-VGG/")

trained_VGG = caffe.Net("Teacher-Student-Training/imagenet/alexnet-VGG/vgg16_original.prototxt", "VGG_ILSVRC_16_layers.caffemodel", caffe.TRAIN)

new_ts_VGG = caffe.Net("Teacher-Student-Training/imagenet/alexnet-VGG/vgg16_original2.prototxt", caffe.TRAIN)



# we load all but fc8 for the VGG student
mapping = {"conv1_1" : "conv1_1",
		   "conv1_2" : "conv1_2",
		   "conv2_1" : "conv2_1",
		   "conv2_2" : "conv2_2",
		   "conv3_1" : "conv3_1",
		   "conv3_2" : "conv3_2",
		   "conv3_3" : "conv3_3",
		   "conv4_1" : "conv4_1",
		   "conv4_2" : "conv4_2",
		   "conv4_3" : "conv4_3",
		   "conv5_1" : "conv5_1",
		   "conv5_2" : "conv5_2",
		   "conv5_3" : "conv5_3",
		   "fc6" : "fc6",
		   "fc7" : "fc7"}

for i in range(0, len(mapping)):
	trained = mapping.keys()[i]
	new = mapping.values()[i]
	new_VGG.params[new][0].data[...] = trained_VGG.params[trained][0].data[...]
	new_VGG.params[new][1].data[...] = trained_VGG.params[trained][1].data[...]
	print "mapped %s to %s" % (trained, new)

new_VGG.save("preloaded_ts_VGG.caffemodel")