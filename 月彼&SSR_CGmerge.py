from PIL import Image
import os
import shutil
import fnmatch

file_path = './cg/'
if not os.path.exists('./output/'):
    os.makedirs('./output/')
save_path = './output/'
all_file = fnmatch.filter(os.listdir(file_path), '*.png')
txt_path = fnmatch.filter(os.listdir(file_path), '*.txt')


# 确定路径

n = 0
while n < len(txt_path):
    def read_txt():
        with open('./cg/' + str(txt_path[n]), 'r', encoding='utf-16 LE') as infile:
            merge_list = []
            for line in infile:
                file_name = line.strip("\n")
                if file_name != '':
                    merge_list.append(file_name)
            print(merge_list)
            return merge_list

    # 循环读取txt文件

    cg_list = read_txt()
    length = len(cg_list) - 2
    status = []  # 标记cg是否已合成
    cg_ex = []  # 标记是否有ex图层
    j = 0
    del cg_list[0]
    del cg_list[0]
    while j < length:
        status.append(False)
        cg_ex.append(False)
        if 'ex' in cg_list[j]:
            cg_ex[j - 1] = True
            del cg_list[j]
            length = length - 1
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
            name1, name2, full_index = cg_list[j].split('_', 2)
            index1 = int(full_index[0:2]) - 1
            index2 = 100
            index3 = 100
            if len(full_index) >= 4:
                index2 = int(full_index[2:4]) - 1
            if len(full_index) >= 6:
                index3 = int(full_index[4:6]) - 1
            base = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
            face1 = Image.new('RGBA', base.size, (0, 0, 0, 0))
            face2 = Image.new('RGBA', base.size, (0, 0, 0, 0))
            for i in all_file:  # 找到合成所需的CG图层
                all_parts = i.split('_')
                part1 = all_parts[0]
                part2 = all_parts[1]
                part3 = ''
                if len(all_parts) >= 3:
                    m = 2
                    while m < len(all_parts):
                        part3 = part3 + all_parts[m]
                        m = m + 1
                if part2 == name2:
                    if part3 == 'base%03d.png' % index1 or part3 == 'base#%03d.png' % index1:
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
            base.alpha_composite(face1, (0, 0))
            base.alpha_composite(face2, (0, 0))
            if base != Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)):
                base.save(save_path + cg_list[j] + '.png')
                print(cg_list[j] + '.png MERGE COMPLETE\n')
            else:
                print('merge error')
            if cg_ex[j]:  # 如果有ex图层
                k = 0
                for i in all_file:
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
                    if part2 == name2 and 'ex' in part3:
                        ex = Image.open(file_path + i)
                        print(part3, 'EX FOUND')
                        temp = base.copy()
                        temp.alpha_composite(ex, (0, 0))
                        if temp != Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)):
                            temp.save(save_path + cg_list[j] + 'ex%02d.png' % (k + 1))
                            print(cg_list[j] + part3, 'MERGE COMPLETE\n')
                        else:
                            print('merge error')
                        k = k + 1
            status[j] = True
        # 找到图片素材并合成输出
        j = j + 1
    n = n + 1

print('COMPLETED!')