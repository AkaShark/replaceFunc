import argparse
import os


def open_dir(path):
    files = os.listdir(path)
    for file in files:
        if not os.path.isdir(os.path.join(path, file)):
            if file != '.DS_Store':
                with open(os.path.join(path, file)) as f:
                    for line in f:
                        find_func(line, os.path.join(path, file))
        else:
            open_dir(os.path.join(path, file))


def find_func(line, path):
    for func in origin_funcs:
        is_find = func.find(line)
        if is_find is not None:
            # 找到之后可以记录path 可以进行参数的修改平写入path中
            print("找到了", path)
            break
        else:
            pass


def read_origin_func(path):
    with open(path) as f:
        for line in f:
            origin_funcs.append(line)


parser = argparse.ArgumentParser(description="input Project local")

parser.add_argument('file_local', type=str, help="project local", )
parser.add_argument('origin_func', type=str, help="origin func local", )

args = parser.parse_args()

file_local = args.file_local
origin_local = args.origin_func

origin_funcs = []

read_origin_func(origin_local)

open_dir(file_local)

