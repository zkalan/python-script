#-*-encoding:utf-8-*-
import argparse
import numpy as np
from pca import pca, labelData2Matrix
from svd import svd
from mds import mds
from isomap import isomap

def distance(source, target):
    return np.matmul(source - target, (source - target).T)

def distanceMatrix(source, target):
    source_r = source.shape[0]
    target_r = target.shape[0]
    dist_matrix = np.zeros((target_r, source_r), dtype=np.float)
    for i in range(target_r):
        for j in range(source_r):
            dist_matrix[i,j] = distance(target[i,:], source[j,:]).real
    return dist_matrix

def prediction(dist_matrix, source_label, K):
    prediction = []
    for m in range(dist_matrix.shape[0]):
        index = np.argsort(dist_matrix[m, :])
        dict = {}
        for n in range(K):
            temp = source_label[index[n]]
            if temp in dict.keys():
                dict[temp] = dict[temp] + 1
            else :
                dict.update({temp: 1})
        prediction.append(max(dict, key=dict.get))
    return prediction

def kNN(train, label, test, K):
    return prediction(distanceMatrix(train, test), label, K)

if __name__=='__main__':
    '''
    train,label = labelData2Matrix('./two-datasets/splice-train30.txt')
    test, lable_ans = labelData2Matrix('./two-datasets/splice-test30.txt')
    label_pre = kNN(pca(train, 10), label, pca(test,10), 1)
    #label_pre = kNN(svd(train, 30), label, svd(test, 30), 1)
    #label_pre = kNN(mds(train, 10), label, mds(test, 10), 1)
    #label_pre = kNN(train, label, test, 1)
    #train_test = isomap(np.vstack((train, test)), 8, 10)
    train_iso = isomap(train, 8, 20)
    test_iso = isomap(test, 8, 20)
    #label_pre = kNN(train_test[:train.shape[0]], label, train_test[train.shape[0]], 1)
    label_pre = kNN(train_iso, label, test_iso, 1)
    correct = 0
    for r in range(len(lable_ans)):
        if lable_ans[r] == label_pre[r]:
            correct += 1
    print(correct)
    print('accuracy: ',correct/len(lable_ans))
    '''
    ## hyperparameters
    parser = argparse.ArgumentParser(description='机器学习作业一')
    parser.add_argument('-a', type=str, default='pca', help='降维方法')
    parser.add_argument('-k', type=int, default='10', help='将至K维')
    parser.add_argument('-train', type=str, default='', help='训练文件')
    parser.add_argument('-test', type=str, default='', help='测试文件')
    args = parser.parse_args()

    train, label = labelData2Matrix(args.train)
    test, lable_ans = labelData2Matrix(args.test)
    if args.a in ['pca']:
        label_pre = kNN(pca(train, args.k), label, pca(test, args.k), 1)
    elif args.s in ['svd']:
        label_pre = kNN(svd(train, args.k), label, svd(test, args.k), 1)
    elif args.a in ['isomap']:
        train_test = isomap(np.vstack((train, test)), 8, args.k)
        label_pre = kNN(train_test[:train.shape[0]], label, train_test[train.shape[0]], 1)
    correct = 0
    for r in range(len(lable_ans)):
        if lable_ans[r] == label_pre[r]:
            correct += 1
    print(correct)
    print('accuracy: ', correct / len(lable_ans))