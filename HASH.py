# -*- coding: utf-8 -*-
import os

import cv2
import numpy as np
import time
import matplotlib.pyplot as plt


# 均值哈希算法
def aHash(img):
    # 缩放为8*8
    # img = cv2.imread(imgFile)
    img = cv2.resize(img, (8, 8), interpolation=cv2.INTER_CUBIC)
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(8):
        for j in range(8):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / 64
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(8):
        for j in range(8):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'

    return hash_str


def pHash(img):
    img_list = []
    # 加载并调整图片为32x32灰度图片
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = cv2.imread(imgFile, 0)
    img = cv2.resize(img, (64, 64), interpolation=cv2.INTER_CUBIC)

    # 创建二维列表
    h, w = img.shape[:2]
    vis0 = np.zeros((h, w), np.float32)
    vis0[:h, :w] = img  # 填充数据

    # 二维Dct变换
    vis1 = cv2.dct(cv2.dct(vis0))
    # cv.SaveImage('a.jpg',cv.fromarray(vis0)) #保存图片
    vis1.resize(32, 32)

    # 把二维list变成一维list
    img_list = vis1.flatten()

    # 计算均值
    avg = sum(img_list) * 1. / len(img_list)
    avg_list = ['0' if i > avg else '1' for i in img_list]

    # 得到哈希值
    return ''.join(['%x' % int(''.join(avg_list[x:x + 4]), 2) for x in range(0, 32 * 32, 4)])


# def hammingDist(s1, s2):
# #assert len(s1) == len(s2)
#     return 1 - sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)])*1. / (32*32/4)

# 计算汉明距离
def hammingDist(s1, s2):
    # assert len(s1) == len(s2)
    hd = 0
    length = len(s1)
    for i in range(length):
        if s1[i] != s2[i]:
            hd += 1

    return hd


# 比较
def diff(pic1, pic2):
    print("[AHash]")
    hash1 = aHash(pic1)
    hash2 = aHash(pic2)
    hd1 = hammingDist(hash1, hash2)
    print("[Hamming Distance]: " + hd1.__str__())

    if hd1 == 0:
        print("[Two Pictures Are The Same]")
    elif hd1 < 5:
        print("[Two Pictures Are Highly Similar]")
    elif hd1 <= 10:
        print("[Two Pictures Are Lowly Similar]")
    else:
        print("[Two Pictures Are Different]")

    print("[PHash]")
    hash1 = pHash(pic1)
    hash2 = pHash(pic2)
    hd2 = hammingDist(hash1, hash2)
    print("[Hamming Distance]: " + hd2.__str__())

    if hd2 == 0:
        print("[Two Pictures Are The Same]")
    elif hd2 < 5:
        print("[Two Pictures Are Highly Similar]")
    elif hd2 <= 10:
        print("[Two Pictures Are Lowly Similar]")
    else:
        print("[Two Pictures Are Different]")

    print("[End Of Execution]")

    return


#################################
# me = "/Users/xc5/Desktop/DeepLearningShortCourse/me.jpeg"
# cat = cv2.imread("/Users/xc5/Desktop/DeepLearningShortCourse/cat.jpeg")
#
# # plt.imshow(me)
# # plt.show()
# # plt.imshow(cat)
# # plt.show()
#
# diff(me, me)
# diff(me, cat)

data_dir = './thumbnails/'

# Saving Hashs
##########################################
counter = 0
ahashes_dir = './index/ahashes.txt'
phashes_dir = './index/phashes.txt'

# for file in os.listdir(data_dir):
#     print("executing " + counter.__str__(), " picture")
#     img = cv2.imread(data_dir + file)
#     ahash_str = aHash(img)
#     with open(ahashes_dir, 'a') as f:
#         f.write(file + ' ' + ahash_str + '\n')
#     f.close()
#
#     phash_str = pHash(img)
#     with open(phashes_dir, 'a') as f:
#         f.write(file + ' ' + phash_str + '\n')
#     f.close()
#     counter += 1

##########################################

def query(mode, img):
    if mode == 'ahash':
        this_hash = aHash(img)
        # print("[This AHash]", this_hash)
        ahashes = open('./index/ahashes.txt')
        # print(ahashes)

        count = 0
        for index, line in enumerate(ahashes):
            count += 1
        print(count)
        ahashes.close()

        ahash_map = {}
        ahashes = open('./index/ahashes.txt')
        for i in range(count):
           content = ahashes.readline()
           # print("[Content]", content)
           contents = content.split(' ')
           # print("[Name]", contents[0])
           # print("[AHash]", contents[1])
           ahash_map[contents[0]] = hammingDist(this_hash, contents[1])

        ahash_map = sorted(ahash_map.items(), key=lambda d: d[1])
        # print("[AHash Map]", ahash_map)
        ahashes.close()

        res_list = []
        for i in range(5):
            res_list.append(ahash_map[i][0])
        print(res_list)
        return res_list
    elif mode == 'phash':
        this_hash = pHash(img)
        print("[This PHash]", this_hash)
        phashes = open('./index/phashes.txt')
        # print(phashes)

        count = 0
        for index, line in enumerate(phashes):
            count += 1
        print(count)
        phashes.close()

        phash_map = {}
        phashes = open('./index/phashes.txt')
        for i in range(count):
            content = phashes.readline()
            # print("[Content]", content)
            contents = content.split(' ')
            # print("[Name]", contents[0])
            # print("[PHash]", contents[1])
            phash_map[contents[0]] = hammingDist(this_hash, contents[1])

        phash_map = sorted(phash_map.items(), key=lambda d: d[1])
        # print("[PHash Map]", phash_map)
        phashes.close()

        res_list = []
        for i in range(5):
            res_list.append(phash_map[i][0])
        print(res_list)
        return res_list


# src = cv2.imread("./thumbnails/001.ak47_001_0001.jpg")
# query('phash', src)
