import os

print('请选择要合并的游戏CG：\n'
      '1.初恋1/1\n'
      '2.星織ユメミライ(Perfect Edition)\n'
      '3.銀色、遥か or 月の彼方で逢いましょう or Sweet Summer Rainbow\n'
      '\n'
      '由于解包出的CG鉴赏合成规则中缺少ex和ex2图层的匹配信息，因此选择合成方法3时'
      '可能会出现多余的图片或明显图层选择有问题的图片，还请自行删除，这点确实处理不了。\n'
      'Because the CG merge rule does not include the ex and ex2 layer matching information, '
      'when choosing the merge method 3, it may result in some extra unnecessary images or '
      'some CGs with obvious layer selection problems, please delete them manually.\n'
      '\n')
choice = input("请输入：")
if choice == '1':
    os.system('python ./CGscripts/初恋_CGmerge.py')
elif choice == '2':
    os.system('python ./CGscripts/星織_PECGmerge.py')
elif choice == '3':
    os.system('python ./CGscripts/銀遥_月彼_SSR_CGmerge.py')
else:
    print('输入错误！')

input('合并完成,按回车键退出')
