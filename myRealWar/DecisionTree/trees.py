# -*- coding: utf-8 -*-
# __author__ = "CHG"
# __createTime__ = '2016/12/13'
# Email: kwchenghong@gmail.com

from math import log
import operator
'''
ID3算法
可能出现一定的过度匹配问题（overfitting）
进行剪枝，去掉不必要的叶子节点
如果叶子节点只能增加少许信息，则可以删除该节点，并将它并入其他叶子节点中

第九章将使用另一个决策树构造算法CART
ID3算法无法直接处理数值型数据，尽管我们可以通过量化的方法将数值型数据转换为标称型数值
但是如果存在太多的特征划分，仍会面对许多问题
'''

def calcEntropy(dataset):
    numEntries = len(dataset)
    labelCounts = {}
    for featVec in dataset:
        currentLabel  = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    entropy = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        entropy -= prob*log(prob,2)
    return entropy


def createDataset():
    dataset =[[1,1,'maybe'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataset , labels


def splitDataset(dataset, axis, value):
    '''
    :param dataset:
    :param axis: feature to be classify
    :param value: value of feature
    :return:
    '''
    retDataset = []
    for featVec in dataset:
        if featVec[axis] == value:
            reduceFeatVec = featVec[:axis]
            reduceFeatVec.extend(featVec[axis+1:])
            retDataset.append(reduceFeatVec)
    return retDataset


def chooseBestFeatureToSplit(dataset):
    '''
    选取特征，划分数据集，计算出最好的划分数据集的特征
    :param dataset:
    :return:
    '''
    numFeatures = len(dataset[0])-1
    baseEntropy = calcEntropy(dataset)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        # 创建唯一分类标签列表
        featList = [example[i] for example in dataset]
        uniqueVals = set(featList)

        newEntropy = 0.0
        # 计算每种划分方式的信息熵
        for value in uniqueVals:
            subDataset = splitDataset(dataset,i,value)
            prob = len(subDataset)/float(len(dataset))
            newEntropy +=prob*calcEntropy(subDataset)
        infoGain = baseEntropy - newEntropy

        if infoGain > bestInfoGain:
            # 计算最好的信息增益
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature


def majorityCnt(classList):
    '''
    类似第二章classify部分的投票表决代码，函数使用分类名称的列表，然后创建键值为classList的唯一值的数据字典
    字典对象存储了classList中每个标签出现的频率。最后利用operator操作键值排序字典，并返回出现次数最多的分类名称
    :param classList:
    :return:
    '''
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


#创建树
def createTree(dataset, labels):
    '''

    :param dataset: 数据集
    :param labels: 标签列表（包含了数据集中所有特征的标签）
                    （算法本身并不需要这个变量，但是为了给数据明确的含义，将他作为输入参数）
    :return:
    '''
    classList = [example[-1] for example in dataset]   # 创建列表变量，包含所有的数据标签

    # 类别完全相同，则停止划分，返回该标签
    if classList.count(classList[0]) == len(classList):
        return classList[0]

    # 遍历所有特征时，返回出现次数最多的
    if len(dataset[0]) == 1:  # 使用完了所有特征，仍然不能将数据及划分成仅包含唯一类别的分组
        return majorityCnt(classList)

    bestFeat = chooseBestFeatureToSplit(dataset)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel : {}}  # 采用字典类型存储树的信息，将当前数据集选取的最好特征存储在变量bestFeat中，
                                   # 得到的列表就包含所有属性值

    #得到列表包含的所有属性值
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataset]
    uniqueVals = set(featValues)

    # 遍历当前选择特征包含的属性值，在每个数据结划分上递归调用函数createTree(),得到的返回值将被插入到字典变量myTree中
    # 函数终止执行时，字典中将潜逃很多代表子节点的字典数据
    for value in uniqueVals:
        subLabels = labels[:]  # 复制类标签，存储在新列表变量subLabels
                               # Python函数参数是列表类型时，参数按照引用方式传递
                               # 为保证每次调用函数createTree()时，不改变原始列表的内容，使用新变量代替原始列表
        myTree[bestFeatLabel][value] = createTree(splitDataset(dataset, bestFeat,value), subLabels)
    return myTree


def classifyTree(inputTree, featLabels, testVec):
    '''
    通过训练数据构造决策树
    比较测试数据与决策树上的数值，递归执行该过程知道进入叶子节点，
    最后将测试数据定义为叶子节点所属的类型
    该函数实际上也是一个递归函数

    在存储带有特征的数据会面临一个问题，程序无法确定数据集中的位置
    特征标签列表将帮助程序处理这个问题
    使用index方法查找当前列表中第一个匹配的firstStr变量的元素
    然后遍历整棵树，比较testVec变量中值与树节点的值，如果到达子节点，则返回当前节点的分类标签
    :param inputTree:
    :param featLabels:
    :param testVec:
    :return:
    '''
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)    #将标签字符串转换为索引
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classifyTree(secondDict[key],featLabels,testVec)
            else:
                classLabel = secondDict[key]
    return classLabel


# 决策树的存储
# 通过下面这两个方法storeTree和grabTree
# 这样将分类器存储在硬盘上，而不用每次对数据费雷重新学习一遍

def storeTree(inputTree, fileName):
    import pickle
    fw = open(fileName, 'w')
    pickle.dump(inputTree, fw)
    fw.close()


def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)
