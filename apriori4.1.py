'''
Apriori算法
包：apyori.apriori
数据：trd_saletran表中用户代理键(sk_invpty),产品代理键(sk_product)
需注意：
1）由于Apriori算法假定项集中的项是按字典序排序的，
 而集合本身是无序的，所以必要时需要进行set和list的转换；
2)由于要使用字典（support_data）记录项集的支持度，需要用项集作为key，
 而可变集合无法作为字典的key，因此在合适时机应将项集转为固定集合frozenset。
2018.3.9
'''

# import pdb

import csv
from apyori import apriori

upfile = open('userProduct.csv', 'r')  # 用户产品对应表
updata = csv.reader(upfile)
upnfile = open('userproductName_2.csv',
               'r', encoding='gbk')  # 用户产品名表
upndata = csv.reader(upnfile)

obj = {}  # 用户-产品list

for line in updata:
    line = list(line)
    key = line[0]  # 用户
    prod = line[1]  # 产品

    if key not in obj:
        obj[key] = []

    obj[key].append(prod)
# for循环用于合并相同用户购买的多个产品并形成字典 {用户A:[产品1,产品2...]}
# print (obj)

upfile.close()


product = obj.values()  # 提取产品编号

# 设置参数：
minSupport = 0.003
minConfidence = 0.08
minLift = 1

print('我们设置的最小支持度:', minSupport, '最小置信度:', minConfidence, '最小提升度:', minLift)

rules = apriori(product, min_support=minSupport,
                min_confidence=minConfidence, min_lift=minLift)

# 关联规则中支持度(support)指项集{X,Y}在总项集里出现的概率，即X和Y同时出现的概率：
# Support(X→Y) = P(X,Y) / P(I) = P(X∪Y) / P(I) = num(XUY) / num(I)
# 置信度(confidence)指含有X的项集中，含有Y的可能性：
# Confidence(X→Y) = P(Y|X)  = P(X,Y) / P(X) = P(XUY) / P(X)
# 提升度（lift）指含有X的条件下，同时含有Y的概率与Y总体发生的概率之比 ：
# Lift(X→Y) = P(Y|X) / P(Y)
# min_support (float)--最小支持度，可用来筛选项集
# min_confidence (float)--最小可信度，可用来筛选项集
# min_lift (float)--最小提升度，可用来筛选项集
# help(apriori)

results = list(rules)
# result里每一个项集的属性介绍：
# items – 项集，frozenset对象，可迭代取出子集。
# support – 支持度，float类型。
# confidence – 置信度或可信度， float类型。
# ordered_statistics – 存在的关联规则

# 关联规则中元素的属性：
# items_base – 关联规则中的分母项集
# items_add - 关联规则中的分子项集
# confidence – 上面的分母规则所对应的关联规则的可信度
# lift - 上面的分母规则所对应的关联规则的提升度

# print(results) #可输出所有关联规则详情

objPno = {}  # 产品编号-产品名表
objUno = {}  # 用户编号-用户名表

for row in upndata:
    row = list(row)
    pno = row[0]  # 产品编码
    pn = row[1]  # 产品名
    uno = row[2]  # 用户编码
    un = row[3]  # 用户名

    objPno[pno] = pn
    objUno[uno] = un

upnfile.close()


def reverseKeyAndValue(normalDict):  # 函数：调换产品、用户的key和value，用于input内容的检索
    return dict((k, v) for v, k in normalDict.items())

objPnoR = reverseKeyAndValue(objPno)
objUnoR = reverseKeyAndValue(objUno)


def getPnoByPname(productName):  # 产品名检索产品编号
    return objPnoR[productName]


def getPnameByPno(productPno):  # 产品编号检索产品名
    return objPno[productPno]


def getUnoByUname(userName):  # 用户名检索用户编号
    return objUnoR[userName]


def getUnameByUno(userUno):  # 用户编号检索用户名
    return objUno[userUno]


addObj = {}


# 通过产品名获取推荐产品 开始
productName = input("您已购买的产品是：")
# productName = '安信广富安发'
print('\n')

# 输入推荐产品数 开始
productNo = getPnoByPname(productName)
# count = '1'


def getRecommentByPno(productNo):  # 已购产品编码检索推荐产品编号

    for RelationRecord in results:
        record = list(RelationRecord.items)
        stat = list(RelationRecord.ordered_statistics)  # 关联规则

        for i in stat:
            if len(record) == 2:  # 只需要考虑两项频繁项集
                itemBase = str(list(i[0])[0])  # 将frozenset转为set再转成字符串
                itemAdd = str(list(i[1])[0])
                conf = i[2]
                # print(itemBase,itemAdd,conf)
                # print(type(productNo))
                # print(type(itemBase))

                if itemBase == productNo:

                    addObj[itemAdd] = conf  # 字典：{itemAdd：conf}
                    # print(addObj)          #遍历形成：{k1:v1,k2:v2}
                    global addObjRList
                    addObjRList = sorted(
                        addObj.items(), key=lambda x: x[1], reverse=True)
                    '''lambda:传递sorted函数的key参数
                    按照value置信度倒序排列，形成[(k1,v1),(k2,v2)] 为元组列表
                    如果写作key=lambda item:item[0]的话则是选取第一个元素作为比较对象，
                    也就是key值作为比较对象。lambda x:y中x表示输出参数，y表示lambda函数的返回值），
                    所以采用这种方法可以对字典的value进行排序。
                    注意排序后的返回值是一个list，而原字典中的名值对被转换为了list中的元组'''
                    # print(addObjRList)

    return addObjRList

# 将推荐产品编号列表转换成按照置信度排序的


# 输入推荐个数参数 开始
# 当count小于LenRWL时调用这个函数：
recommentNo = []
recommentListKey = []
recommentListPname = []


def OutputCountLessThanLenRWL(recommentConfiOrderList, count):

    # recommentConfiOrderList = getRecommentByPno(productNo)
    for r in recommentConfiOrderList:
        recommentNo.append(r)
        countConfiOrderList = recommentConfiOrderList[0:count]
        # 排序前count项的编号和置信度
    for r in countConfiOrderList:
        recommentListKey.append(r[0])
    # print(recommentListKey)  # 提取编号
    for r in recommentListKey:  # 通过编号获取产品名
        recommentListPname.append(getPnameByPno(r))

    return recommentListPname


recommentConfiOrderList = []
# 判断输入内容是否标准的函数

isAllowInput = True


def start():
    # try把输入的各种数字转化为整型
    try:
        count = input('请输入需要推荐产品个数(请输入一个整数，默认为1)：')
        count = int(count)
    # 如果不是数字，默认为一，继续执行下面两个if比较，并且调用函数
    except Exception:
        count = 1
        print('您的输入不是一个正确的整数!')
        print('默认输出一个推荐产品:')
    if count <= 0:
        print('您的输入小于等于0')
        print('默认输出一个推荐产品:')
        count = 1
    recommentConfiOrderList = getRecommentByPno(productNo)
    print(recommentConfiOrderList)
    # 将getRecommentByPno结果赋值给一个变量，获得推荐产品编号和置信度排序列表recommentConfiOrderList
    if count <= len(recommentConfiOrderList):
        productList = OutputCountLessThanLenRWL(recommentConfiOrderList, count)
        return productList
    else:
        print('Oops~ 没有这么多产品推荐哦！换个小于等于%d的数试试吧~' % len(recommentConfiOrderList))
        start()
        # 数字过大时提示并重新调用判断函数


productList = start()
print('购买这个产品的用户还买了：')
print(productList)
print('\n')
# 通过产品名获取推荐产品 结束


# 通过用户编号检索已购买产品 开始
# userUno = input('请输入您的用户编号：')
userUno = '16687798'
boughtPNoList = obj[userUno]
boughtPNameList = []


def getBoughtPnameListByUno(userUno):
    for no in boughtPNoList:
        boughtPNameList.append(getPnameByPno(no))
    # print(boughtPNoList) #['127', '508', '128']
    return boughtPNameList


# 通过用户已购买列表为其推荐产品 开始
print(getUnameByUno(userUno), '您已购买了以下产品：')
print(getBoughtPnameListByUno(userUno))
print('\n')
print('同样买了这些产品的用户还买了：')


def getPnameByUserBoughtPnoList(boughtPNoList):
    # 获取到所有的推荐列表
    recommentList = []
    pnoDict = {}
    recommentKeyNameList = []
    for pno in boughtPNoList:
        recommentKeyList = getRecommentByPno(pno)
        for r in recommentKeyList:
            pnoDict[r[0]] = True
        # recommentList.append(recommentKeyList)
    pnoList = pnoDict.keys()
    for n in pnoList:
        recommentKeyNameList.append(getPnameByPno(n))

    return recommentKeyNameList


print(getPnameByUserBoughtPnoList(boughtPNoList))
