import os

Curr_path = "E:/project870/20230901"

def combare_diff():

    all_line = []
    with open("E:/project870/20230901.txt", 'r') as file:
        for line in file:
            line = line.strip()
            # print(line)
            all_line.append(line)
    # 获取目录中所有文件列表
    # file_list = os.listdir(Curr_path)

    # 使用列表解析过滤出所有以.txt为扩展名的文件
    # txt_files = [file for file in file_list if not file.endswith('M.txt')]
    # 使用列表推导式获取文件夹中所有的.txt文件
    small_files = [f for f in os.listdir(Curr_path) if not f.endswith('M.txt') ]

    diff_count = 0
    exist_line = False
    # 遍历所有.txt文件并读取它们的内容
    for small_file in small_files:
        small_path = os.path.join(Curr_path, small_file)  # 获取完整文件路径
        with open(small_path, 'r') as file:
            for small_line in file:
                small_line = small_line.strip()
                exist_line = False
                for big_line in all_line:
                    if small_line.startswith(big_line[:5]):
                        exist_line = True
                        if big_line != small_line:
                            print(small_file,'Different')
                            print('5 mins:',small_line)
                            print('1  day:',big_line)
                            diff_count +=1
                            print()
                        continue
                if not exist_line:
                    print(small_file,'This record does not exist in the large file of one day')
                    print(small_line)
                    print()

    print(diff_count)


    # 遍历所有.txt文件并读取它们的内容
    # for txt_file in txt_files:
    #     file_path = os.path.join(Curr_path, txt_file)  # 获取完整文件路径
    #     with open(file_path, 'r') as file:
    #         for line in file:
    #             count += 1
    #             line = line.strip()
    #             if line not in all_line:
    #                 print(txt_file, line)


combare_diff()




