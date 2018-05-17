import json
from .optimizer import Optimizer
from .layer import Layer
from keras import Model

def find_key(index):
	global data
	global nodeArray
	global linkArray
	global layers

	for lr in layers:
		if lr.get_index() == index:
			return lr

def find_type(type):
	global data
	global nodeArray
	global linkArray
	global layers

	for lr in layers:
		if lr.get_type() == type:
			return lr

#Получаем список слоев с которыми соединяем предыдущий слой
def get_to(index):
	global data
	global nodeArray
	global linkArray
	global layers

	list = []
	i = 0
	for lr in linkArray:
		if lr["from"] == index:
			layer = find_key(lr["to"])
			list.append(layer)
	if len(list) == 1:
		return list[0]
	return list

#Получаем список слоев с которыми соединяем предыдущий слой
def get_from(index):
	global data
	global nodeArray
	global linkArray
	global layers

	list = []
	i = 0
	for lr in linkArray:
		if lr["to"] == index:
			layer = find_key(lr["from"])
			list.append(layer)
	if len(list) == 1:
		return list[0]
	return list

def create_model(table_json):
	global data
	global nodeArray
	global linkArray
	global layers
	global optimizer
	global epochs
	global loss
	data = json.loads(table_json)
	nodeArray = data["nodeDataArray"]
	linkArray = data["linkDataArray"]

	i = 0
	while i < len(nodeArray):
		obj = nodeArray[i]
		try:
			if obj["type"] == "Optimizer":
				optimizer = Optimizer(obj, get_from).get_opt()
			elif obj["type"] == "Setting":
				loss = obj["loss"]
				epochs = int(obj["epochs"])
			else:
				layers.append(Layer(obj, get_from))
		except:
			pass
		i += 1

	inp = find_type("Input")
	inp.prev = True
	end = find_type("End")
	end.next = True
	out = get_from(end.get_index())
	out.set_link(0)
	model = Model(inputs=inp.get_block(), outputs=out.get_block())

	model.compile(loss=loss, optimizer=optimizer, metrics=['accuracy'])

	return (model, epochs)

data = None
nodeArray = None
linkArray = None
optimizer = None
epochs = 1
loss = "mse"
layers = []

