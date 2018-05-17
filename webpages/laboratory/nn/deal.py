import numpy as np

import manage as mn
print(mn.get_root())
arr = np.array([0,1,2,3,4,5,6,7])
np.save("test.npy", arr)
arr = np.array2string(arr)

fil = open("test.npy", 'w')
fil.write(arr)
fil.close()
print('file was added')
arr = np.load("test.npy")
print(arr)
print(type(arr))
