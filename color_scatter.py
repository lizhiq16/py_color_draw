'''
Author: Li ZhiQiang
Organization: JHL
Date: 2023/12/27
绘制彩红绿蓝渐变散点图
Since the data ranges of the two gradient parts are not the same, 
one color range of the drawing is scaled 
(so you have to manually move the uper tick 0.1 to the top of the color bar in the right).
'''

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import time


start = time.perf_counter()

# 从txt文件读取数据
#data = np.loadtxt('output2.txt', delimiter=' ')
#data1 = data[:, 0]
#data2 = data[:, 1]

with open('output.txt', 'r') as file:
    lines = file.readlines()
    data0 = [[float(item) for item in line.split()] for line in lines]
#    data0 = [line.split() for line in lines]    
#data = np.array(data0).astype(float)
data = np.array(data0)
#print("数组形状: ", data.shape)
#print("第6-8行内容: ", data[6:8])

mask = (data[:, 4] <= 2.5)
filtered_data = data[mask]
#print("数组形状: ", filtered_data.shape)

data1 = filtered_data[:, 3]
data2 = filtered_data[:, 4]

# 自定义x轴的范围
xmin, xmax = -0.25, 0.1
xscal = abs(xmin/xmax)

# 计算得出正负对称的data3，用来作为颜色的尺度
data3 = np.where(data1 < 0, data1, xscal * data1)

# 创建一个颜色映射
cmap_list = [(0, 0, 1), (0, 1, 0), (1, 0, 0)]  # 蓝、绿、红三种颜色
cmap = colors.LinearSegmentedColormap.from_list('Custom cmap', cmap_list, N=256)

# 创建散点图，并根据data3的大小设置颜色
sc = plt.scatter(data1, data2, c=data3, cmap=cmap, vmin=xmin, vmax=abs(xmin), s=0.5)

# 设置坐标轴范围和标题
plt.xlim(xmin-0.01, xmax+0.01)
plt.ylim(0, 2.5)
plt.xlabel(r'sign($\lambda_2$)$\rho$', fontsize=16)
#plt.xlabel('sign(λ2)ρ', fontsize=16, fontstyle='italic')
plt.ylabel('IRI(a.u.)', fontsize=16)

# 设置刻度文字大小
plt.tick_params(labelsize=13)

# 添加颜色条。 由于为了颜正确使用的data3对正向x进行了xscal，所得colorbar正向0.1的刻度需要调整至红色最上位置。
#plt.colorbar(sc, ticks=[-0.4, 0, 0.1], label='data3')
cbar = plt.colorbar(sc, ticks=[xmin, -0.15, 0, xmax, xscal * xmax])

# 设置颜色条刻度标签右对齐并设置字体大小
cbar.ax.yaxis.set_tick_params(labelright=True, labelsize=12)

# 设置图形大小（单位为cm转英寸）
fig = plt.gcf()
fig.set_size_inches(19.2/2.54, 14.84/2.54)

# 更新坐标轴以适应新的图形大小
plt.tight_layout()

end = time.perf_counter()
time = '{:,.3f}'.format(end-start)
print ("elapsed time(s):"+ str(time))

plt.show()

# 保存图片为指定PPi的PNG文件
#plt.savefig('color_scatter_plot2.png', dpi=300)

# 关闭图形窗口
plt.close()
