import argparse
import os
import re

#读取函数列表文件 将要替换的函数名字写进数组
def read_origin_func():
    with open(need_change) as f:
        for line in f:
            need_change_func_name = line.replace('\n', '').replace('\r', '').replace(' ', '')
            need_change_func_name_array.append(need_change_func_name)
            open_dir(file_local, need_change_func_name)
        
    with open(fin_change) as f:
        for line in f:
            fin_change_func_name  = line.replace('\n', '').replace('\r', '').replace(' ', '')
            fin_change_func_name_array.append(fin_change_func_name)

    with open(fin_import_func) as f:
        for line in f:
            import_name = line.rstrip()
            fin_import_name_array.append(import_name)

    with open(origin_local) as f:
        for line in f:
            import_name = line.rstrip()
            import_name_array.append(import_name)
    
    #根据找到的路径去修改相应位置
    for path in change_path_array:
        change_func(path)
    
    #遍历其他文件（导入头文件没有使用方法的情况）
    for import_name in import_name_array:
        open_dir_import(file_local, import_name)
    
    log_file(log_local)
    
    
#创建日志
def log_file(path):
    f = open(path+"/log.txt","w")
    for str in log_change_func_array:
        f.write(str+"\n")
    f.close
    print("日志生成")



#打开文件 读取文件内容
def open_dir(path,funcName):
    files = os.listdir(path)
    for file in files:
        if not os.path.isdir(os.path.join(path, file)):
            if file != '.DS_Store':
                with open(os.path.join(path, file)) as f:
                    for line in f:
                        find_func(line, os.path.join(path, file),funcName)
                        
        else:
            open_dir(os.path.join(path, file),funcName)


#匹配条件
def find_func(line, path, funcName):
    #查看是否调用了相应方法并记录路径
    is_find = re.search(funcName,line)
    if is_find is not None:
        # 有相应的方法
        if path in change_path_array:
            print("已经记录路径不在重复记录")
        else:
            change_path_array.append(path)
            print("记录路径")
    else:
        pass

#打开文件 读取文件内容
def open_dir_import(path,funcName):
    files = os.listdir(path)
    for file in files:
        if not os.path.isdir(os.path.join(path, file)):
            if file != '.DS_Store':
                with open(os.path.join(path, file)) as f:
                    for line in f:
                        alter(os.path.join(path, file),funcName,"")
                        
        else:
            open_dir(os.path.join(path, file),funcName)


# 更换方法名和头文件
def change_func(path):
    funcName_conent = 0
    importName_conent = 0
    
    for funcName in need_change_func_name_array:
        #找到应该替换的方法 进行替换
        alter(path,funcName,fin_change_func_name_array[funcName_conent])
        funcName_conent = funcName_conent + 1
        
    for importName in import_name_array:
        #找到引入的头文件 进行替换
        alter(path,importName,fin_import_name_array[importName_conent])
        importName_conent = importName_conent + 1
          
            
    
# 替换字符串
def alter(file,old_str,new_str):
    
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
         for line in f:
             if old_str in line:
                 tmp = "将内容:"+old_str+"修改为:"+new_str+"----"+"操作路径为"+file
                 log_change_func_array.append(tmp)
                 line = line.replace(old_str,new_str)
                 if "@\"#" in line:
                    line = line.replace("@\"#","@\"")
                    tmp = "将内容:@\"#修改为:@\""+"----"+"操作路径为"+file
                 if "@\"0X" in line:
                    tmp = "将内容:@0X修改为:@\""+"----"+"操作路径为"+file
             file_data += line
             
    with open(file,"w",encoding="utf-8") as f:
         f.write(file_data)




parser = argparse.ArgumentParser(description="input Project local")
#第一个参数传入项目路径
parser.add_argument('file_local', type=str, help="project local", )
#第二个参数传入需要修改的引入头文件目录
parser.add_argument('origin_func', type=str, help="origin func local", )
#第三个参数传入需要更改之后引入头文件目录
parser.add_argument('fin_import_func', type=str, help="fin_import_func", )
#第四个参数传入需要更改的方法目录
parser.add_argument('need_change', type=str, help="need_change", )
#第五个参数传入更改之后的方法目录
parser.add_argument('fin_change', type=str, help="fin_change", )
#第六个参数日志生成的目录
parser.add_argument('log_local', type=str, help="log_local", )


args = parser.parse_args()

file_local = args.file_local
origin_local = args.origin_func
fin_import_func = args.fin_import_func
need_change = args.need_change
fin_change = args.fin_change
log_local = args.log_local

#引用的头文件数组
import_name_array = []
#更改之后的头文件数组
fin_import_name_array = []
#需要进行修改的路径数组
change_path_array = []
#需要更改的方法数组
need_change_func_name_array = []
#更改之后的方法数组
fin_change_func_name_array = []

#更换方法名和头文件日志数组
log_change_func_array = []

read_origin_func()


