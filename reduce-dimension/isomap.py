# -*-encoding:utf-8-*-
from mds import mds
from pca import labelData2Matrix
import numpy as np
from mds import mds
from collections import Counter

def distance(source, target):
    print(np.matmul(source - target, (source - target).T).__class__)
    return np.matmul(source - target, (source - target).T)


def distanceMatrix(source, target):
    source_r = source.shape[0]
    target_r = target.shape[0]
    dist_matrix = np.zeros((target_r, source_r), dtype=np.float)
    for i in range(target_r):
        for j in range(source_r):
            dist_matrix[i, j] = distance(target[i, :], source[j, :]).real
    return dist_matrix


# https://blog.csdn.net/Lwenjiyou_/article/details/79548577
def floyd(matrix):
    result_matrix = matrix.copy()
    count = matrix.shape[0]
    for i in range(count):
        for j in range(count):
            for k in range(count):
                if result_matrix[j, i] + result_matrix[i, k] < result_matrix[j, k]:
                    result_matrix[j, k] = result_matrix[j, i] + result_matrix[i, k]
    return result_matrix
'''
def transform(matrix):
    row = matrix.shape[0]
    for i in range(row):
        for j in range(row - i):
            if matrix[i,j+i] < np.inf:
                pass
            else:
                matrix[i, j+i] = 999999999999999
            if matrix[j+i, i] < np.inf:
                pass
            else:
                matrix[j+i, i] = 999999999999999
    return matrix

#https://blog.csdn.net/weixin_42705075/article/details/81515043
def max_list(lt):
    temp = 0
    for i in lt:
        if lt.count(i) > temp:
            max_str = i
            temp = lt.count(i)
    return max_str

def getSubgraph(matrix):
    matrix = transform(matrix)
    row = matrix.shape[0]
    flag = np.zeros(row, dtype=int)
    for i in range(row):
        num = 0 #i行样本能够到达的样本数量
        for j in range(row):
            if matrix[i, j] < np.inf:
                num += 1
        flag[i] = num
    max_num = max_list(flag)
    final_index = []
    for i in range(row):
        if flag[i] == max_num:
            final_index.append(i)
    return final_index
'''

def isomap(matrix, K, d):
    #init_adjacency_matrix = np.full((matrix.shape[0], matrix.shape[0]), fill_value=np.inf, dtype=np.float)
    init_adjacency_matrix = np.full((matrix.shape[0], matrix.shape[0]), fill_value=10**20, dtype=np.float)
    # 利用k近邻算法，初始化一个邻接矩阵
    init_dist_matrix = distanceMatrix(matrix, matrix)
    print('完成邻接矩阵计算')
    for m in range(init_dist_matrix.shape[0]):
        index = np.argsort(init_dist_matrix[m, :])
        for n in range(K + 1):  # 存在同一个样本到自己的情况，所以k近邻要加1
            init_adjacency_matrix[m, index[n]] = init_dist_matrix[m, index[n]].real
    print('完成将' + str(K) + '个近邻值赋值到无穷矩阵中')
    # 使用最短路径算法，获得新的邻接矩阵
    init_adjacency_matrix = floyd(init_adjacency_matrix)
    print('完成Floyd算法')
    #将不连通的较小子图视为噪声或者增大K进行试错
    #设置inf为一个足够大的数字，保证能够进行特征值分解
    # 调用mds算法，获得样本的低维坐标
    return mds(init_adjacency_matrix, d, 1)


if __name__ == '__main__':
    print('IsoMap')
    train, label = labelData2Matrix('./two-datasets/train.txt')
    test, lable_ans = labelData2Matrix('./two-datasets/test.txt')
    print(isomap(np.vstack((train, test)), 8, 3))
