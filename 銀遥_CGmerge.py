from PIL import Image
import os
import shutil
import fnmatch
# 银遥有bug，勿用

file_path = './cg/'
if not os.path.exists('./output/'):
    os.makedirs('./output/')
save_path = './output/'
all_file = fnmatch.filter(os.listdir(file_path), '*.png')
txt_path = fnmatch.filter(os.listdir(file_path), '*.txt')

# 确定路径

n = 0
while n < len(txt_path):
    def read_txt():  # 循环读取txt文件
        with open('./cg/' + str(txt_path[n]), 'r', encoding='utf-16 LE') as infile:
            merge_list = []
            for line in infile:
                file_name = line.strip("\n")
                if file_name != '':
                    merge_list.append(file_name)
            print(merge_list)
            return merge_list


    def ex2_judge(num):
        if num < 3:
            return 0
        elif num == 3:
            return 1
        elif num == 4:
            return 2


    cg_list = read_txt()
    length = len(cg_list) - 2
    status = []  # 标记cg是否已合成
    cg_ex = []  # 标记是否有ex图层
    j = 0
    del cg_list[0]
    del cg_list[0]
    while j < length:
        status.append(False)
        cg_ex.append(0)
        if 'ex' in cg_list[j]:  # 如有ex图层，分为ex、ex1、ex1+ex2三种情况
            if cg_list[j][-2:] == 'ex':
                cg_ex[j] = 1
                del cg_list[j]
                length = length - 1
            elif cg_list[j][-3:] == 'ex1' and cg_list[j + 1][-3:] != 'ex2':
                cg_ex[j] = 2
                del cg_list[j]
                length = length - 1
            elif cg_list[j][-3:] == 'ex1' and cg_list[j + 1][-3:] == 'ex2':
                cg_ex[j] = 3
                del cg_list[j]
                del cg_list[j]
                length = length - 2
        j = j + 1
    print(cg_list)
    j = 0
    while j < len(all_file):
        all_file[j] = all_file[j].lower()
        j = j + 1
    j = 0
    while j < length:
        for i in all_file:
            if i == cg_list[j] + '.png':
                old_dir = os.path.join(file_path, i)
                new_dir = os.path.join(save_path, cg_list[j] + '.png')
                shutil.copy(old_dir, new_dir)
                print(i, 'COPY SUCCESS\n')
                status[j] = True
                break
            else:
                continue
        # 直接移动已有的图片
        if not status[j]:
            print(cg_list[j], 'is merging...')
            print(cg_ex[j])
            name1, name2, full_index = cg_list[j].split('_', 2)
            index1 = int(full_index[0:2]) - 1
            index2 = 0
            index3 = 0
            if len(full_index) >= 4:
                index2 = int(full_index[2:4]) - 1
            if len(full_index) >= 6:
                index3 = int(full_index[4:6]) - 1
            base = Image.new('RGBA', (1280, 720), (0, 0, 0, 0))
            face1 = Image.new('RGBA', base.size, (0, 0, 0, 0))
            face2 = Image.new('RGBA', base.size, (0, 0, 0, 0))
            for i in all_file:  # 找到合成所需的CG图层
                all_parts = i.split('_')
                part1 = all_parts[0]
                part2 = all_parts[1]
                part3 = ''
                m = 0
                if len(all_parts) >= 3:
                    m = 2
                    while m < len(all_parts):
                        part3 = part3 + all_parts[m]
                        m = m + 1
                if part2 == name2:
                    if part3 == 'base#%03d.png' % index1:
                        base = Image.open(file_path + i)
                        print(part3, 'BASE FOUND')
                    elif part3 == 'base.png':
                        base = Image.open(file_path + i)
                        print(part3, 'BASE FOUND')
                    elif part3 == 'face#%03d.png' % index2:
                        face1 = Image.open(file_path + i)
                        print(part3, 'FACE1 FOUND')
                    elif part3 == 'face2#%03d.png' % index3:
                        face2 = Image.open(file_path + i)
                        print(part3, 'FACE2 FOUND')
            base = base.convert('RGBA')
            if cg_ex[j] == 0:  # 判断是否有ex图层
                base.alpha_composite(face1, (0, 0))
                base.alpha_composite(face2, (0, 0))
                base.save(save_path + cg_list[j] + '.png')
                print(cg_list[j] + '.png MERGE COMPLETE\n')
            if cg_ex[j] == 1 or cg_ex[j] == 2 or cg_ex[j] == 3:
                if full_index[4:6] == '':
                    index3 = index2
                for i in all_file:
                    ex1 = Image.new('RGBA', base.size, (0, 0, 0, 0))
                    ex2 = Image.new('RGBA', base.size, (0, 0, 0, 0))
                    all_parts = i.split('_')
                    part1 = all_parts[0]
                    part2 = all_parts[1]
                    part3 = ''
                    if len(all_parts) >= 3:
                        m = 2
                        while m < len(all_parts):
                            part3 = part3 + all_parts[m]
                            m = m + 1
                    if part2 == name2 and 'ex' in part3 and 'ex2' not in part3:
                        if (part3 == 'ex.png' or 'ex#' in part3) and cg_ex[j] == 1:
                            ex1 = Image.open(file_path + i)
                            print(part3, 'EX FOUND')
                            base.alpha_composite(face1, (0, 0))
                            base.alpha_composite(face2, (0, 0))
                            temp = base.copy()
                            temp.alpha_composite(ex1, (0, 0))
                            temp.save(save_path + cg_list[j] + part3.replace('#0', ''))
                            print(cg_list[j] + part3, 'MERGE COMPLETE\n')
                        elif part3 == 'ex1#%03d.png' % index3 and cg_ex[j] == 2:
                            ex1 = Image.open(file_path + i)
                            print(part3, 'EX1 FOUND')
                            base.alpha_composite(face1, (0, 0))
                            temp = base.copy()
                            temp.alpha_composite(ex1, (0, 0))
                            temp.save(save_path + cg_list[j] + '.png')
                            print(cg_list[j], 'MERGE COMPLETE\n')
                        elif part3 == 'ex1#%03d.png' % index3 and cg_ex[j] == 3:
                            ex1 = Image.open(file_path + i)
                            print(part3, 'EX1 FOUND')
                            base.alpha_composite(face1, (0, 0))
                            temp = base.copy()
                            temp.alpha_composite(ex1, (0, 0))
                            for k in all_file:
                                all_parts_temp = k.split('_')
                                part1_temp = all_parts_temp[0]
                                part2_temp = all_parts_temp[1]
                                part3_temp = ''
                                if len(all_parts_temp) >= 3:
                                    m = 2
                                    while m < len(all_parts_temp):
                                        part3_temp = part3_temp + all_parts_temp[m]
                                        m = m + 1
                                if part2_temp == name2 and \
                                        (part3_temp == 'ex2#%03d.png' % ex2_judge(index3) or part3_temp == 'ex2.png'):
                                    ex2 = Image.open(file_path + k)
                                    print(part3_temp, 'EX2 FOUND')
                                    temp2 = temp.copy()
                                    temp2.alpha_composite(ex2, (0, 0))
                                    temp2.save(save_path + cg_list[j] + part3_temp.replace('#0', ''))
                                    print(cg_list[j] + part3 + part3_temp, 'MERGE COMPLETE\n')
            status[j] = True
        # 找到图片素材并合成输出
        j = j + 1
    n = n + 1

print('COMPLETED!')
