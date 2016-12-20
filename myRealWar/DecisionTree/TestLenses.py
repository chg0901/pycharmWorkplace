# -*- coding: utf-8 -*-
# __author__ = "CHG"
# __createTime__ = '2016/12/21'
# Email: kwchenghong@gmail.com

import trees
import treePlotter

fr = open('lenses.txt')
lenses = [inst.strip().split('\t') for inst in fr.readlines()]
lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
lensesTree = trees.createTree(lenses, lensesLabels)
print lensesTree
treePlotter.createPlot(lensesTree)
