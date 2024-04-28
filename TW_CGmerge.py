import os
from cgscripts.koi import main_koi
from cgscripts.hoshi import main_hoshi
from cgscripts.silver import main_silver

while True:
    print('请选择要合并的游戏CG：\n'
          '1.初恋1/1\n'
          '2.星織ユメミライ(Perfect Edition)\n'
          '3.銀色、遥か or 月の彼方で逢いましょう or Sweet Summer Rainbow\n'
          '\n'
          '由于解包出的CG鉴赏合成规则中缺少ex和ex2图层的匹配信息，因此选择合成方法3时'
          '不会对ex图层进行匹配，还请自行合成ex图层，这点确实处理不了。\n'
          'Because the CG merge rule does not include the ex and ex2 layer matching information, \n'
          'when choosing \'merge method 3\', the ex layer will not be matched, \n'
          'please merge them manually.\n'
          '\n')
    choice = input("请输入：")
    path = input("请输入解包出的CG文件夹路径（Please enter the path of the decompressed CG folder）：")
    
    if not os.path.exists(path):
        print('路径不存在！')
        continue  # 跳过当前循环，继续执行下一个循环

    output_path = input("请输入合并后的CG输出路径（Please enter the output path of the merged CG）：")
        
    if choice == '1':
        main_koi(path, output_path)
    elif choice == '2':
        main_hoshi(path, output_path)
    elif choice == '3':
        main_silver(path, output_path)
    else:
        print('输入错误！')

    again = input('是否继续执行任务？(y/n): ')
    if again.lower() != 'y':
        break  # 退出循环

input('按回车键退出')
