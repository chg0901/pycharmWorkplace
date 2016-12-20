# -*- coding: utf-8 -*-
# __author__ = "CHG"
# __createTime__ = '2016/12/13'
# Email: kwchenghong@gmail.com

import trees

import treePlotter

# # 创建决策树
# dataset,labels = trees.createDataset()
# print dataset
# # [[1, 1, 'maybe'], [1, 1, 'yes'], [1, 0, 'no'], [0, 1, 'no'], [0, 1, 'no']]
# print trees.calcEntropy(dataset)
#
# # splitDataset(dataset, axis, value):
# #     '''
# #     :param dataset:
# #     :param axis: feature to be classify
# #     :param value: value of feature
# #     :return:
# #     '''
# # print trees.splitDataset(dataset,0,1)
# # print trees.splitDataset(dataset,0,0)
#
# myTree = trees.createTree(dataset, labels)
# print myTree
# # {'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'maybe'}}}}


# #绘制决策树
# #print treePlotter.retrieveTree(1)
# myTree = treePlotter.retrieveTree(0)
# print treePlotter.getNumLeafs(myTree)
# print treePlotter.getTreeDepth(myTree)
# treePlotter.createPlot(myTree)
# myTree['no surfacing'][3] = 'maybe'
# print myTree
# treePlotter.createPlot(myTree)

# # 决策树分类
# dataset,labels = trees.createDataset()
# print dataset
# print labels
#
# myTree = treePlotter.retrieveTree(0)
# print myTree
# trees.storeTree(myTree, 'classifierStorage.txt')
# print trees.grabTree('classifierStorage.txt')
# treePlotter.createPlot(myTree)
# print trees.classifyTree(myTree, labels, [1, 1])
# print trees.classifyTree(myTree, labels, [1, 0])
# print trees.classifyTree(myTree, labels, [0, 1])
# print trees.classifyTree(myTree, labels, [0, 0])


# trees.storeTree(myTree, 'classifierStorage.txt')
# print trees.grabTree('classifierStorage.txt')
tree = trees.grabTree('classifierStorage.txt')
print type(tree)  # <type 'dict'>