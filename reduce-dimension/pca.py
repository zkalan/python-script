#-*-encoding:utf-8-*-
import numpy as np
import os.path

def matrixInfo(matrix):
    print("数据类型", type(matrix))  # 打印数组数据类型
    print("数组元素数据类型：", matrix.dtype)  # 打印数组元素数据类型
    print("数组元素总数：", matrix.size)  # 打印数组尺寸，即数组元素总数
    print("数组形状：", matrix.shape)  # 打印数组形状
    print("数组的维度数目", matrix.ndim)  # 打印数组的维度数目

def labelData2Matrix(filepath):
    list_matrix = []
    label = []
    with open(filepath, 'r', encoding='utf-8') as tr:
        file_data = tr.readlines()
        for line in file_data:
            temp = list(map(np.float, line.strip().split(',')))
            list_matrix.append(temp[:-1])
            label.append(temp[-1:][0])
    return np.array(list_matrix, order='F'), label

def centralizeData(matrix):
    [r_num, c_num] = matrix.shape
    for c in range(c_num):
        column = 0
        for key in matrix[:, c]:
            column += key
        column = column/r_num
        for r in range(r_num):
            matrix[r, c] = matrix[r, c] - column
    return matrix

def covariance(matrix):
    [row, column] = matrix.shape
    return np.matmul(matrix.T, matrix)/(row-1)

def normalize(arr):
    row, column = arr.shape
    for c in range(column):
        mean = np.mean(arr[:, c])
        mx = max(arr[:, c])
        mn = min(arr[:, c])
        for r in range(row):
            arr[r,c] = (arr[r,c] - mean)/(mx - mn)
    return arr

def topKEigen(eigenval, eigenvec, k):
    index = np.argsort(eigenval)
    return eigenval[index[:-k-1:-1]], normalize(eigenvec[:, index[:-k-1:-1]])

def pca(matrix, K):
    #对所有样本进行中心化
    centralized_matrix = centralizeData(matrix)
    #计算样本协方差矩阵
    matrix_cov = covariance(centralized_matrix)
    #对协方差矩阵进行特征值分解
    eigenval, eigenvec = np.linalg.eig(matrix_cov)
    # 取最大的K个特征值对应的特征向量构成投影矩阵
    prim_val, prim_vect = topKEigen(eigenval, eigenvec, K)
    return np.matmul(matrix, prim_vect)

if __name__ == '__main__':
    '''
    matrix, label = labelData2Matrix('./two-datasets/splice-train.txt')
    #对所有样本进行中心化
    centralized_matrix = centralizeData(matrix)
    print(matrixInfo(centralized_matrix))
    #计算样本协方差矩阵
    #matrix_cov = np.cov(centralized_matrix, rowvar=False)
    matrix_cov = covariance(centralized_matrix)
    print(matrixInfo(matrix_cov))
    np.savetxt('./file-cov3.txt',matrix_cov)
    #对协方差矩阵进行特征值分解
    eigenval, eigenvec = np.linalg.eig(matrix_cov)
    # 取最大的K个特征值对应的特征向量构成投影矩阵
    a,b = topKEigen(eigenval, eigenvec, 10)
    #np.savetxt('./file.txt', b)
    
    value10, vector10 = pca('./two-datasets/splice-train.txt', 10)
    value20, vector20 = pca('./two-datasets/splice-train.txt', 20)
    value30, vector30 = pca('./two-datasets/splice-train.txt', 30)
    np.savetxt('./pca10.txt', vector10)
    np.savetxt('./pca20.txt', vector20)
    np.savetxt('./pca30.txt', vector30)
    '''
    matrix, label = labelData2Matrix('./two-datasets/splice-train.txt')
    value10, vector10 = pca(matrix, 10)
    matrix, label = labelData2Matrix('./two-datasets/splice-train.txt')
    print(matrix)
    ma = np.matmul(matrix, vector10)
    print(ma.shape)