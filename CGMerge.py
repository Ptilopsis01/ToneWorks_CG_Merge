import os

print('请选择要合并的游戏CG：\n'
      '1.初恋1/1\n'
      '2.星織ユメミライ(Perfect Edition)\n'
      '3.月の彼方で逢いましょう(Sweet Summer Rainbow)\n'
      '4.銀色、遥か(Caution: Unfixed bugs)\n')
choice = input("请输入：")
if choice == '1':
    os.system('python 初恋_CGmerge.py')
elif choice == '2':
    os.system('python 星織_PECGmerge.py')
elif choice == '3':
    os.system('python 月彼&SSR_CGmerge.py')
elif choice == '4':
    os.system('python 銀遥_CGmerge.py')
else:
    print('输入错误！')

input('合并完成,按回车键退出')
