from keras.layers import Activation, BatchNormalization, Reshape, RepeatVector, Permute, Input, \
	Dense, Conv1D, Conv2DTranspose, Conv3D, Conv2D, Dropout, \
	 Flatten, UpSampling2D, Deconvolution2D, UpSampling1D, UpSampling3D, \
	MaxPooling1D, MaxPooling2D, MaxPooling3D, AveragePooling1D, \
	AveragePooling2D, AveragePooling3D, GlobalMaxPooling1D, GlobalMaxPooling2D, \
	GlobalAveragePooling1D, GlobalAveragePooling2D, LocallyConnected1D, \
	LocallyConnected2D, Add, Subtract, Multiply, Average, Maximum, Concatenate, Dot, \
	GaussianNoise, GaussianDropout, AlphaDropout
from keras.optimizers import Adam, SGD, RMSprop, Adadelta, Adagrad


class Layer:

	get_from = None

	prev = False
	next = False
	layers = None

	list = None
	type = None
	name = None
	key = None
	fields = None
	block = None

	def __init__(self, list, get_from):
		self.list = list
		self.get_from = get_from
		self.type = self.set("type")
		self.name = self.set("name")
		self.key = self.set("key")
		self.fields = self.set("fields")
		self.create_layer()

	def __str__(self):
		return self.type

	def get_index(self):
		return self.key

	def len(self):
		return None

	def set_link(self, i):
		i+=1
		if i > 300:
			return
		if self.prev is True:
			return self.block
		if self.next is True:
			return
		self.layers = self.get_from(self.key)
		if type(self.layers) == list:
			self.layers = [n.set_link(i) for n in self.layers]
			self.prev = True
		else:
			self.layers = self.layers.set_link(i)

			self.prev = True

		self.block = self.block(self.layers)
		return self.block

	def get_block(self):
		return self.block

	def get_type(self):
		return self.type

	def set(self, value):
		try:
			value = self.list[value]
		except Exception:
			value = None
		return value

	def create_layer(self):
		if self.type == "Dense":
			self.block = Dense(units=int(self.gff("units")), activation=self.gff("activation"))
		elif self.type == "Input":
			self.block = Input(shape=self.get_int(self.gff("shape")))
		elif self.type == "Dropout":
			self.block = Dropout(rate=float(self.gff("rate")))
		elif self.type == "Flatten":
			self.block = Flatten()
		elif self.type == "Reshape":
			self.block = Reshape(target_shape=int(self.gff("rate")))
		elif self.type == "Permute":
			self.block = Permute(dims=self.get_int(self.gff("dims")))
		elif self.type == "RepeatVector":
			self.block = RepeatVector(n=int(self.gff("dims")))
		#CONVOLUTIONAL
		elif self.type == "Conv1D":
			self.block = Conv1D(filters=int(self.gff("filters")), kernel_size=self.get_int(self.gff("kernel_size")),
								activation=self.get_act(self.gff("activation")), strides=self.get_int(self.gff("strides")),
								padding=self.gff("padding"))
		elif self.type == "Conv2D":
			self.block = Conv2D(filters=int(self.gff("filters")), kernel_size=self.get_int(self.gff("kernel_size")),
								activation=self.get_act(self.gff("activation")), strides=self.get_int(self.gff("strides")),
								padding=self.gff("padding"))
		elif self.type == "Conv2DTranspose":
			self.block = Conv2DTranspose(filters=int(self.gff("filters")), kernel_size=self.get_int(self.gff("kernel_size")),
								activation=self.get_act(self.gff("activation")), strides=self.get_int(self.gff("strides")),
								padding=self.gff("padding"))
		elif self.type == "Conv3D":
			self.block = Conv3D(filters=int(self.gff("filters")), kernel_size=self.get_int(self.gff("kernel_size")),
								activation=self.get_act(self.gff("activation")), strides=self.get_int(self.gff("strides")),
								padding=self.gff("padding"))
		elif self.type == "UpSampling1D":
			self.block = UpSampling1D(size=self.get_int(self.gff("size")))
		elif self.type == "UpSampling2D":
			self.block = UpSampling2D(size=self.get_int(self.gff("size")))
		elif self.type == "UpSampling3D":
			self.block = UpSampling3D(size=self.get_int(self.gff("size")))
		#POOLING
		elif self.type == "MaxPooling1D":
			self.block = MaxPooling1D(pool_size=self.get_int(self.gff("pool_size")),
									  strides=self.get_int(self.gff("strides")), padding=self.gff("padding"))
		elif self.type == "MaxPooling2D":
			self.block = MaxPooling2D(pool_size=self.get_int(self.gff("pool_size")),
									  strides=self.get_int(self.gff("strides")), padding=self.gff("padding"))
		elif self.type == "MaxPooling3D":
			self.block = MaxPooling3D(pool_size=self.get_int(self.gff("pool_size")),
									  strides=self.get_int(self.gff("strides")), padding=self.gff("padding"))
		elif self.type == "AveragePooling1D":
			self.block = AveragePooling1D(pool_size=self.get_int(self.gff("pool_size")),
									  strides=self.get_int(self.gff("strides")), padding=self.gff("padding"))
		elif self.type == "AveragePooling2D":
			self.block = AveragePooling2D(pool_size=self.get_int(self.gff("pool_size")),
									  strides=self.get_int(self.gff("strides")), padding=self.gff("padding"))
		elif self.type == "AveragePooling3D":
			self.block = AveragePooling3D(pool_size=self.get_int(self.gff("pool_size")),
									  strides=self.get_int(self.gff("strides")), padding=self.gff("padding"))
		elif self.type == "GlobalMaxPooling1D":
			self.block = GlobalMaxPooling1D()
		elif self.type == "GlobalMaxPooling2D":
			self.block = GlobalMaxPooling2D()
		elif self.type == "GlobalAveragePooling1D":
			self.block = GlobalAveragePooling1D()
		elif self.type == "GlobalAveragePooling2D":
			self.block = GlobalAveragePooling2D()
		#Locally Connected
		elif self.type == "LocallyConnected1D":
			self.block = LocallyConnected1D(filters=int(self.gff("filters")), kernel_size=self.get_int(self.gff("kernel_size")),
								activation=self.get_act(self.gff("activation")), strides=self.get_int(self.gff("strides")),
								padding=self.gff("padding"))
		elif self.type == "LocallyConnected2D":
			self.block = LocallyConnected2D(filters=int(self.gff("filters")), kernel_size=self.get_int(self.gff("kernel_size")),
								activation=self.get_act(self.gff("activation")), strides=self.get_int(self.gff("strides")),
								padding=self.gff("padding"))
		#MERGE LAYERS
		elif self.type == "Add":
			self.block = Add()
		elif self.type == "Subtract":
			self.block = Subtract()
		elif self.type == "Multiply":
			self.block = Multiply()
		elif self.type == "Average":
			self.block = Average()
		elif self.type == "Maximum":
			self.block = Maximum()
		elif self.type == "Concatenate":
			self.block = Concatenate()
		elif self.type == "Dot":
			self.block = Dot()

		#NORMALISATION LAYER
		elif self.type == "BatchNormalization":
			self.block = BatchNormalization(axis=int(self.gff("axis")), center=bool(self.gff("center")),
											momentum=float(self.gff("momentum")), epsilon=float(self.gff("epsilon")),
											scale=bool(self.gff("scale")))
		#NOISE LAYERS
		elif self.type == "GaussianNoise":
			self.block = GaussianNoise(stddev=self.get_float(self.gff("stddev")))
		#NOISE LAYERS
		elif self.type == "GaussianDropout":
			self.block = GaussianDropout(rate=self.get_float(self.gff("rate")))
		elif self.type == "AlphaDropout":
			self.block = AlphaDropout(rate=self.get_float(self.gff("rate")), seed=int(self.gff("rate")))


		#Get value from field
	def gff(self, value):
		i = 0
		while i<len(self.fields):
			if self.fields[i]["name"] == value:
				break
			i+=1
		try:
			value = self.fields[i]["value"]
		except Exception:
			value = None
		return value

	def get_int(self, list):
		if list=="None":
			return None
		dims = tuple( int(item) for item in list.split(','))
		if len(dims) == 1:
			return dims[0]
		return dims

	def get_float(self, value):
		if value=="None":
			return None
		return float(value)

	def get_act(self, activation):
		return activation