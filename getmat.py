import scipy.io as sio
'''# python创建一个mat文件
x = [[1, 2, 3], [4, 5, 6]]
y = [4, 5, 6]
z = [7, 8, 9]
sio.savemat('saveddata.mat', {'x': x,'y': y,'z': z}'''

f = open('./MARS1202/test_name.txt')   # 修改文件名
x = []
y = [1]
i = 1
z = '0001'

# 读入第一行，以免与循环发生冲突
content = f.readline()
id = content[0:4]
cam = content[5]

while True:
    content = f.readline()
    if content == '':
        break
    i = i + 1
    z2 = content[7:11]
    t = content[12:15]
    # print(z2)
    if z2 != z or t == '001':
        z = z2
        y.append(i-1)
        if not id == "00-1":  # 对id为-1的情况单独考虑
            y.append(int(id))
        else:
            y.append(-1)
        y.append(int(cam))
        id = content[0:4]
        cam = content[5]
        x.append(y)
        y = [i]
# 最后一个tracklet还没有写入循环就退出了
y.append(i)
y.append(int(id))
y.append(int(cam))
x.append(y)
#print(x)
sio.savemat('tracks_test_info.mat', {'track_test_info': x})  # 修改输出文件名


