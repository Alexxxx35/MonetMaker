from sklearn.cluster import KMeans
import numpy as np
from itertools import chain

def cluster_pixels (matrix : list) -> list :

    x, y, data_size = matrix.shape
    tmp = matrix.reshape((x*y,data_size))
    kmeans = KMeans(n_clusters=5,random_state=0).fit(tmp)  
    print( "CLUSTERING : DONE")
    #print(kmeans.labels_)
    #print(kmeans.cluster_centers_)
    for i,value in enumerate(tmp):
        group = kmeans.labels_[i]
        val = kmeans.cluster_centers_[group]
        #print(group , "   ", val)
        tmp[i] = val
        
    
    tmp = tmp.reshape((x,y,data_size))
    return tmp