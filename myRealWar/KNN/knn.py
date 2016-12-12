# -*- coding: utf-8 -*-
# __author__ = "CHG"
# Email: kwchenghong@gmail.com

from numpy import *
import operator
'''
K-近邻算法是分类数据最简单有效的算法
是基于实例的学习
使用算法时，必须有接近实际数据的训练样本数据
必须保存全部数据集，如果训练数据集较大，必须使用大量的存储空间
由于必须对数据集中每个数据计算距离值，实际使用非常耗时

另一个区缺陷是无法给出任何数据的基础结构信息
因此无法知道平均实力样本和典型实例样本具有什么特征
'''
# 手写识别测试代码
from os import listdir

#PART1

def createDataset():

    group = array([[1.0, 1.1],[1.0, 1.0], [0,0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


'''
kNN: k Nearest Neighbors

Input:      inX: vector to compare to existing dataset (1xN)
            dataSet: size m data set of known vectors (NxM)
            labels: data set labels (1xM vector)
            k: number of neighbors to use for comparison (should be an odd number)

Output:     the most popular class label

'''


def classifyKnn(inX, dataset, labels, k):

    datasetSize = dataset.shape[0]

    # calculate the distance(Euclidean)
    diffMat = tile(inX, (datasetSize, 1))-dataset
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5

    sortedDistIndicies = distances.argsort()

    classCount = {}

    # choose the points with minimum distances
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0)+1

    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)

    return sortedClassCount[0][0]


# PART2


def file2matrix(filename):

    fr = open(filename)
    numberOfLines = len(fr.readlines())         # get the number of lines in the file
    returnMat = zeros((numberOfLines,3))        # prepare matrix to return
    classLabelVector = []                       # prepare labels return
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()                     # delete '\n'
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector


# PART3 归一化
def autoNorm(dataset):

    minVals = dataset.min(0)                    # 擦参数0使得函数可以列中选出最小值，而不是从当前行中
    maxVals = dataset.max(0)
    ranges = maxVals-minVals
    normDataset = zeros(shape(dataset))
    m = dataset.shape[0]                        # 此处是中括号
    normDataset = dataset-tile(minVals,(m,1))   # 使用tile函数将变量内容制成输入矩阵同样大小的矩阵
    normDataset = normDataset/tile(ranges,(m,1))
    return normDataset,ranges,minVals


# PART4 测试算法：作为完整程序验证分类器
def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    persentTats = float(raw_input("percentage of time spent playing video games?"))
    ffMiles = float(raw_input("liters of ice cream consumed per years?"))
    iceCream = float(raw_input("liters of ice ceram consumed per year?"))
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    # print datingDataMat
    # print datingLabels
    normMat, ranges, minVals = autoNorm(datingDataMat)
    # print normMat
    inArr = array([ffMiles, persentTats, iceCream])
    classifierResult = classifyKnn(((inArr-minVals)/ranges), normMat, datingLabels, 3)



# 字体识别
# 文本图像数据转换为1024矩阵
def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect


# 手写识别测试代码
# from os import listdir
# 列出给定目录的文件名

'''
文件9_45.txt的分类是9，是数字9的第45个实例


该算法执行效率较低
算法需要为每个测试向量做2000次距离计算，每个距离计算包括了1024个维度浮点计算，总计要执行900次
此外，还要为测试向量准备2M的存储空间

K决策树是k-近邻算法的优化版，可以节省大量的计算开销，减少存储空间和计算时间的开销
'''

def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')  # 获取目录内容
    m = len(trainingFileList)
    trainingMat = zeros((m, 1024))
    for i in range(m):
        # 从文件名解析分类数字
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])

        hwLabels.append(classNumStr)
        trainingMat[i, :] = img2vector('trainingDigits/%s' % fileNameStr)

    testFileList = listdir('testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])

        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classifyKnn(vectorUnderTest, trainingMat, hwLabels, 3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
        if (classifierResult != classNumStr):
            errorCount += 1.0
    print "\n the total number of errors is: %d" % errorCount
    print "\n tje total error rate is : %f "%(errorCount/float(mTest))

