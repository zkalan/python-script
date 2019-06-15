#-*-encoding:utf-8-*-
import numpy as np
from pca import labelData2Matrix

def topKEigen(eigenval, eigenvec, k):
    index = np.argsort(eigenval)
    return eigenval[index[:-k-1:-1]], eigenvec[:, index[:-k-1:-1]]

def svd(matrix, K):
    ma = np.matmul(matrix.T, matrix)
    #计算特征值和特征向量
    eigenval, eigenvec = np.linalg.eig(ma)
    #对于大于零的特征值，其平方根和特征值大小成正比
    #因此，前K大的特征值对应的奇异值最大，对应的特征值
    #构成右奇异矩阵，可用于降维
    prim_val, singular_vect = topKEigen(eigenval, eigenvec, K)
    return np.matmul(matrix, singular_vect)

if __name__=='__main__':

    print('SVD')
    train, label = labelData2Matrix('./two-datasets/splice-train.txt')
    ma = svd(train, 10)
    np.savetxt('./svd10.txt', ma)