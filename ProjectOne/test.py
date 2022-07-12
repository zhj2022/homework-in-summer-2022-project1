import sklearn
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ARI import adjusted_rand_score


def unique(list):
    new_list = []
    for i in range(len(list)):
        if list[i] not in new_list:
            new_list.append(list[i])
    return new_list


def list_to_numlist(list):
    list_unique = unique(list)
    list_unique_len = len(list_unique)
    num_list = []
    for i in list:
        for j in range(list_unique_len):
            if list_unique[j] == i:
                num_list.append(j)
    return num_list


poi_vector = np.load('poi_vector(step=5km).npy')
poi = pd.read_excel('shanghai_poi.xls')
poi_tagz = poi['tagz']
tag = list_to_numlist(poi_tagz)


k_means = KMeans(n_clusters=24, random_state=0)
k_means.fit(poi_vector)
tag_pred = k_means.predict(poi_vector)
print(adjusted_rand_score(tag, tag_pred))


# pca = PCA(n_components=2)
# pca.fit(poi_vector)
# poi_vector_reduced = pca.transform(poi_vector)
#
# plt.scatter(poi_vector_reduced[:, 0], poi_vector_reduced[:, 1], c=tag)
# plt.xlim(-2, 0)
# plt.ylim(-2, 2)
# plt.show()
#
# plt.scatter(poi_vector_reduced[:, 0], poi_vector_reduced[:, 1], c=tag_pred)
# plt.xlim(-2, 0)
# plt.ylim(-2, 2)
# plt.show()
# 可视化过程
