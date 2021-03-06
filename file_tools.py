# coding: utf-8
import struct
import network
from PIL import Image
import numpy as np
from array import array
import json


def convert_image(file):
    img = Image.open(file)
    img = img.resize((28, 28))
    img = img.convert("1")
    # img.save('img.png')
    img_list = np.ones((28 * 28), dtype=int)
    # print img.size
    i = 0
    for y in range(28):
        for x in range(28):
            if img.getpixel((x, y)):
                img_list[i] = 1
                # print '1',
            else:
                img_list[i] = 0
                # print ' ',
            i += 1
    return img_list


def get_num(file):
    img_list = convert_image(file)
    with open('data.json', 'r') as f:
        data = json.load(f)

    input_num = data['input_num']
    hidden_num = data['hidden_num']
    output_num = data['output_num']
    alpha = data['alpha']
    nw = network.NetWork(input_num, hidden_num, output_num, alpha)
    nw.hidden_weight = np.asarray(data['hidden'])
    nw.output_weight = np.asarray(data['output'])
    nw.hidden_theta = np.asarray(data['hidden_theta'])
    nw.output_theta = np.asarray(data['output_theta'])
    result = nw.get_output_result(img_list)
    print np.float64(result).round()
    dic = {
    0:np.array([1,0,0,0,0,0,0,0,0,0]),
    1:np.array([0,1,0,0,0,0,0,0,0,0]),
    2:np.array([0,0,1,0,0,0,0,0,0,0]),
    3:np.array([0,0,0,1,0,0,0,0,0,0]),
    4:np.array([0,0,0,0,1,0,0,0,0,0]),
    5:np.array([0,0,0,0,0,1,0,0,0,0]),
    6:np.array([0,0,0,0,0,0,1,0,0,0]),
    7:np.array([0,0,0,0,0,0,0,1,0,0]),
    8:np.array([0,0,0,0,0,0,0,0,1,0]),
    9:np.array([0,0,0,0,0,0,0,0,0,1]),
    }    
    num = np.argmax(result)
    j = json.dumps(dic[num].tolist())
    return json.dumps(num.tolist())


# 将文件中第x张图片解析成 01 列表，filename文件名 x =index， 返回一个list
def read_image(filename, index):
    f = open(filename, 'rb')
    buf = f.read()
    f.close()
    pos = 0
    magic, images, rows, columns = struct.unpack_from('>IIII', buf, pos)
    if index > images:
        return
    pos += struct.calcsize('>IIII')  # 跳过开头说明

    pos += struct.calcsize('>B') * rows * columns * index   # 设置索引

    arr = np.ones((rows * columns), dtype=float)
    # print arr
    i = 0
    for x in xrange(rows):
        for y in xrange(columns):
            v = struct.unpack_from('>B', buf, pos)[0]
            if v>0:
                arr[i] = 1
            else:
                arr[i] = 0
            pos += struct.calcsize('>B')
            i += 1
        # print '\n'

    # print arr
    return arr


# 解析图片的值,返回一个10位的01列表
def read_label(filename, index):
    dic = {
        0: np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        1: np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
        2: np.array([0, 0, 1, 0, 0, 0, 0, 0, 0, 0]),
        3: np.array([0, 0, 0, 1, 0, 0, 0, 0, 0, 0]),
        4: np.array([0, 0, 0, 0, 1, 0, 0, 0, 0, 0]),
        5: np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0]),
        6: np.array([0, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
        7: np.array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0]),
        8: np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
        9: np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1]),
    }
    f = open(filename, 'rb')
    buf = f.read()
    f.close()
    pos = 0
    magic, labels = struct.unpack_from('>II', buf, pos)
    if index > labels:
        return
    pos += struct.calcsize('>II')

    pos += struct.calcsize('>B') * index

    num = int(struct.unpack_from('>B', buf, pos)[0])

    # print num
    return dic[num]


if __name__ == '__main__':
    arr=read_image('train-images.idx3-ubyte',2)
    print arr
    # num = read_label('train-labels.idx1-ubyte',4)
    # print num
    # l = convert_image('17.png')
    # print l.size
    # for i in l:
    #     if i:
    #         print '1',
    #     else:
    #         print ' ',
