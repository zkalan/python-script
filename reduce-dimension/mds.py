#-*-encoding:utf-8-*-
from pca import labelData2Matrix
import numpy as np

def topKEigen(eigenval, eigenvec, k):
    index = np.argsort(eigenval)
    return eigenval[index[:-k-1:-1]], eigenvec[:, index[:-k-1:-1]]

def distance(source, target, order='R'):
    return np.matmul(source-target, (source-target).T)

def distanceMatrix(matrix):
    row, column = matrix.shape
    dist_Matrix = np.zeros((row, row), dtype=np.float)
    for i in range(row):
        for j in range(row):
            dist_Matrix[i,j] = distance(matrix[i, :], matrix[j, :]).real
    return dist_Matrix

def mds(matrix, d, type=0):
    row = matrix.shape[0]
    if type == 0:
        dist_Matrix = distanceMatrix(matrix)
    else:
        dist_Matrix = matrix
    #完成对mds算法的输入
    B = np.zeros((row, row), dtype=np.float)
    A = np.zeros((d, d), dtype=np.float)
    matrix_mean = np.mean(dist_Matrix)
    for i in range(row):
        for j in range(row):
            B[i, j] = -0.5*(matrix_mean + dist_Matrix[i, j] - np.mean(dist_Matrix[i, :]) - np.mean(dist_Matrix[:, j]))
    eigenval, eigenvect = np.linalg.eig(B)
    val, vect = topKEigen(eigenval, eigenvect, d)
    for i in range(d):
        print(val[i])
        A[i, i] = (val[i]**(1/2)).real
    print('完成mds算法')
    return np.matmul(vect, A)

if __name__=='__main__':
    train, label = labelData2Matrix('./two-datasets/splice-train.txt')
    np.savetxt('mds10.txt',mds(train, 2))
