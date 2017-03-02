# coding: utf-8
import network
from PIL import Image
import numpy as np
import struct
import file_tools
import json

def main():
    input_num = 28*28
    hiden_num = 80
    output_num = 10
    alpha = 0.3
    nw = network.NetWork(input_num, hiden_num, output_num, alpha)
    process = 0
    tran_num = 59999 # 训练样本数
    best_square = 1.0
    best_hiden = None
    best_output = None

    error_list = []
    best_list = []
    for i in xrange(tran_num):
        img_list = file_tools.read_image('train-images.idx3-ubyte',i)
        expect_list = file_tools.read_label('train-labels.idx1-ubyte',i) 
        nw.tranning(img_list,expect_list)
        error_list.append(nw.error_squared)
        if nw.error_squared < best_square:
            best_square = nw.error_squared
            best_hiden = nw.hiden_weight
            best_output = nw.output_weight
        best_list.append(best_square)
        if i % int(tran_num/100) == 0:         
            print str(process)+'%'+' best_square = '+str(best_square)
            process+=1

    best_data = {
    'input_num': input_num,
    'hiden_num': hiden_num,
    'output_num':output_num,
    'hiden':best_hiden.tolist(),
    'output':best_output.tolist(),
    'hiden_theta':nw.hiden_theta.tolist(),
    'output_theta':nw.output_theta.tolist(),
    }

    last_data = {
    'input_num': input_num,
    'hiden_num': hiden_num,
    'output_num':output_num,
    'hiden':nw.hiden_weight.tolist(),
    'output':nw.output_weight.tolist(),
    'hiden_theta':nw.hiden_theta.tolist(),
    'output_theta':nw.output_theta.tolist(),
    }

    error_data = {
    'error_list': error_list,
    'best_list' : best_list,
    }

    with open('best_data.json','w') as f:
        json.dump(best_data,f)

    with open('last_data.json','w') as f:
        json.dump(last_data,f)

    with open('error_data.json','w') as f:
        json.dump(error_data,f)

if __name__ == '__main__':
    main()