import json
from pprint import pprint
from layer import Layer
data = json.load(open('model.json'))
nodeArray = data["nodeDataArray"]
linkArray = data["linkDataArray"]

layers = []

i = 0
while i < len(nodeArray):
	layers.append(Layer(nodeArray[i]))
	i+=1

def find_key(index):
	for lr in layers:
		if lr.get_index() == index:
			return lr


def find_type(type):
	for lr in layers:
		if lr.get_type() == type:
			return lr


#Получаем список слоев с которыми соединяем предыдущий слой
def get_to(index):
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
	list = []
	i = 0
	for lr in linkArray:
		if lr["to"] == index:
			layer = find_key(lr["from"])
			list.append(layer)
	if len(list) == 1:
		return list[0]
	return list
