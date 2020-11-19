import argparse
import os
import re

def open_dir(path, funcName):
    files = os.listdir(path)
    for file in files:
        if not os.path.isdir(os.path.join(path, file)):
            if file != '.DS_Store':
                with open(os.path.join(path, file)) as f:
                    for line in f:
                        find_func(line, os.path.join(path, file), funcName)

        else:
            open_dir(os.path.join(path, file), funcName)

def find_func(line, path, funcName):
        is_find = re.search(funcName,line)
#        print("内部便利方法名",funcName)
        if is_find is not None:
            # 找到之后可以记录path 可以进行参数的修改平写入path中
            print("使用了方法的类是:", path)
            if funcName in use_func_name_array:
                print("又一次使用方法:", funcName)
            else:
                use_func_name_array.append(funcName)
                print("第一次使用方法:", funcName)
            
        else:
            pass
#读取函数列表文件 将要替换的函数名字写进数组
def read_origin_func(path):
    i = 0
    with open(path) as f:
        for line in f:
            print("遍历次数", i)
            i=i+1
            funcNAME = line.replace('\n', '').replace('\r', '').replace(' ', '')
            print("查找的方法名称",funcNAME)
            open_dir(file_local, funcNAME)
            
    print()


parser = argparse.ArgumentParser(description="input Project local")
#第一个参数传入项目路径
parser.add_argument('file_local', type=str, help="project local", )
#第二个参数传入配置文件路径
parser.add_argument('origin_func', type=str, help="origin func local", )

args = parser.parse_args()

file_local = args.file_local
origin_local = args.origin_func
use_func_name_array = []
read_origin_func(origin_local)