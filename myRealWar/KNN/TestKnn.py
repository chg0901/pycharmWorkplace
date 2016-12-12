# -*- coding: utf-8 -*-
# __author__ = "CHG"
# Email: kwchenghong@gmail.com

import knn
from numpy import *
import operator

# # PART1
# group, labels = knn.createDataset()
# print group
# print labels
#
# print knn.classifyKnn([0, 0], group, labels, 3)

# # PART2
# datingDataMat, datinglabels = knn.file2matrix('datingTestSet2.txt')
# print datingDataMat[0:20]
# print datinglabels[0:20]

# # plt
# import matplotlib
# import matplotlib.pyplot as plt
# fig = plt.figure()
# ax = fig.add_subplot(211)
# # ax.scatter(datingDataMat[:,1],datingDataMat[:,2])
# ax.scatter(datingDataMat[:,1],datingDataMat[:,2],15.0* array(datinglabels), 15.0*array(datinglabels))
# ax.axis([-2,25,-0.2,2.0])
# plt.xlabel('Percentage of Time Spent Playing Video Games')
# plt.ylabel('Liters of Ice Cream Consumed Per Week')
# # plt.show()

# # 看到2.2.3准备数据：归一化数值
# normMat, ranges, minVals = knn.autoNorm(datingDataMat)
# print normMat
# print ranges
# print minVals


# # 找对象分类
# knn.classifyPerson()


# # 手写识别数字
#
# # 识别单个文件内容
# testVector = knn.img2vector('testDigits/0_13.txt')
# print testVector[0, 0:31]
# print testVector[0, 32:63]

knn.handwritingClassTest()

