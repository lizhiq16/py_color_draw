'''
Athor: Li ZhiQiang
Organization: JHL
Date: 2023/12/27
绘制彩红绿双色渐变填充图
'''

import matplotlib.pyplot as plt
import numpy as np

# 从文件中读取波长和数据
with open('spectrum_data.txt', 'r') as file:
    lines = file.readlines()
    data = [line.split() for line in lines]
    wavelengths, intensities = zip(*[(float(line[0]), float(line[1])) for line in data])

# 自定义彩虹渐变填充方案
num_points = len(wavelengths)
colors = np.zeros((num_points, 4))  # 创建一个RGBA颜色的数组

# 定义颜色渐变规则（这里示例为红、绿双色的渐变）
colors[:, 0] = np.linspace(1, 0, num_points)  # 红色通道，从1到0
colors[:, 1] = np.linspace(0, 1, num_points)  # 绿色通道，从0到1
#colors[:, 2] = np.linspace(0, 0, num_points)  # 蓝色通道，全为0
colors[:, 3] = np.ones(num_points)  # Alpha通道，全为1（不透明）

# 绘制曲线和彩虹渐变填充
plt.plot(wavelengths, intensities, 'k-')  # 绘制黑色曲线
plt.fill_between(wavelengths, intensities, color='none', edgecolor='none', alpha=0.3)

# 填充渐变色
for i in range(num_points - 1):
    plt.fill_between(wavelengths[i:i+2], intensities[i:i+2], color=colors[i])

# 调整坐标轴范围
plt.ylim(0,)
plt.xlim(380, 780)
#plt.xlim(np.min(wavelengths), np.max(wavelengths))
plt.xlabel('Wavelength(nm)', fontsize=12)
plt.ylabel('Intensity(a.u.)', fontsize=12)

# 设置图形大小（单位为cm转英寸）
fig = plt.gcf()
fig.set_size_inches(19.2/2.54, 14.84/2.54)

plt.show()
