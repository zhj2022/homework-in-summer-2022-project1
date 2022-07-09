import numpy as np

data = np.load('arrive_point_array.npz', allow_pickle=True)

for item in data.files:
    np.save("arrive_point_array.npy", data[item])
