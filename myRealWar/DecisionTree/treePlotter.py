# -*- coding: utf-8 -*-
# __author__ = "CHG"
# __createTime__ = '2016/12/14'
# Email: kwchenghong@gmail.com

import matplotlib.pyplot as plt

# 定义文本框和箭头格式,定义树格式的常量
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


# 绘制带箭头的注解，执行实际的绘制功能
def plotNode(nodeTxt,centerPt,parentPt,nodeType):

    '''
    # 该函数需要一个绘图区，这个区域由全局变量createPlot.ax1定义
    # python所有变量都是全局有效的
    :param nodeTxt:
    :param centerPt:
    :param parentPt:
    :param nodeType:
    :return:
    '''
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
                            xytext=centerPt, textcoords='axes fraction',
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)

# version1
# def createPlot():
#     '''
#     :return:
#     '''
#     fig = plt.figure(1, facecolor='white')  # 创建了一个新图形
#     fig.clf()                               # 并清空绘图区
#     createPlot.ax1 = plt.subplot(111, frameon=False)
#     # 在UI图区绘制两个代表不同类型的树节点
#     plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
#     plotNode('a leaf node', (0.8,0.1), (0.3, 0.8), leafNode)
#     plt.show()

# test PART1
# createPlot()

# 构造注解树
# 获取树的叶节点数目和树的层数


def getNumLeafs(myTree):
    '''
    该数据结构说明了如何在python字典中如何存储树信息
    第一个关键字是第一次划分数据集的类别标签，附带的数值表示子节点的数值
    从第一个关键字出发，我们可以遍历整棵树的所有子节点
    通过python提供的type（）函数可以判断子节点是否是字典类型，
        如果是字典类型，则该节点也是一个判断节点，递归调用get函数
    :param myTree:
    :return:
    '''
    numLeafs = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        # 测试节点类型是否为字典
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs


def getTreeDepth(myTree):
    '''
    达到子节点即从递归中返回，将计算树的深度加一
    :param myTree:
    :return:
    '''
    maxDepth = 0
    firstStr = myTree.keys()[0]
    secondDic = myTree[firstStr]
    for key in secondDic.keys():
        if type(secondDic[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDic[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth


def retrieveTree(i):
    '''
    构造函数retrieveTree输出预先存储的树的信息，避免每次测试代码时都要从数据中创建树的麻烦
    :param i:
    :return:
    '''
    listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                   {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}]
    return listOfTrees[i]


def plotMidText(cntrPt, parentPt, txtString):
    # 在
    xMid = (parentPt[0] - cntrPt[0])/ 2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)


def plotTree(myTree, parentPt, nodeTxt):
    '''
    该函数也是一个递归函数，
    树的宽度用于计算放置判断几点的位置是，主要的计算规则是将他放在所有叶子节点的中间，而不仅仅是她子节点的中间
    全局变量plotTree.xOff和plotTree.yOff最终已经绘制节点的位置，以及放置下一个节点的恰当位置

    另一个需要说明的问题
    绘制图形的X轴，Y轴的有效范围是0.0~1.0，
    为方便起见，给出的坐标值，绘制出的图形并没有xy左边
    通过计算树所包含的叶子节点数，划分图形的宽度，
    按照图形比例绘制树形图最大好处就是无需关心实际输出图形的大小
    一旦图形法身变化，函数会自动按照图形大小重新绘制
    如果以像素为单位绘制图形，缩放很复杂

    :param myTree:
    :param parentPt:
    :param nodeTxt:
    :return:
    '''
    # 计算树宽和高
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)

    firstStr = myTree.keys()[0]

    # 全局变量plotTree.totalW存储树的宽度，全局变量plotTree.totalD存储树的深度
    # 使用这两个变量计算树节点的摆放位置，这样可以将树绘制在水平为处置方向的垂直位置
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW,plotTree.yOff)

    #给出子节点的特征值，或者沿此分支向下的数据实例必须具有的特征值
    plotMidText(cntrPt, parentPt, nodeTxt)    # 计算父节点和子节点的中间位置，并向此添加简单的文本标签信息
    plotNode(firstStr, cntrPt, parentPt, decisionNode)

    secondDict = myTree[firstStr]

    # 按比例减少全局变量plotTree.yOff,并标注将要绘制子节点
    # 这些节点既可以是叶子节点，也可以是判断节点，此处只需要保存绘制图形的轨迹，
    # 因为是自顶往下绘制图形，所以需要递减y坐标值
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':

            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff,plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD


def createPlot(inTree):
    '''
    该函数是我们使用的主函数，
    创建绘图区，计算树形图的全局尺寸，调用plotTree()

    :param inTree:
    :return:
    '''
    fig = plt.figure(1, facecolor='white')  # 创建了一个新图形
    fig.clf()                               # 并清空绘图区
    axprops = dict(xticks=[], yticks=[])

    createPlot.ax1 = plt.subplot(111, frameon=False)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW;
    plotTree.yOff = 1.0;
    plotTree(inTree, (0.5, 1.0), ' ')
    plt.savefig('1.png')
    plt.show()
