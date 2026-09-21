'''
Author: Li ZhiQiang
Organization: JHL
Date: 2023/12/27
绘制红绿蓝渐变散点图 (修改版：使用 TwoSlopeNorm 自动适配横坐标非对称范围)
'''

import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

# 获取文件名（命令行第二个参数，若无则默认为 'output.txt'）
filename = sys.argv[1] if len(sys.argv) > 1 else 'output.txt'

# 检查文件是否存在
if not os.path.exists(filename):
    print(f"错误：找不到文件 '{filename}'！")
    sys.exit(1)

start = time.perf_counter()

# 使用 np.loadtxt 优化读取，内置支持连续任意空格分割
try:
    data = np.loadtxt(filename)
except Exception as e:
    print(f"读取文件 '{filename}' 失败：{e}")
    sys.exit(1)
#print("数组形状: ", data.shape)
#print("第6-8行内容: ", data[6:8])

mask = (data[:, 4] <= 2.5)
filtered_data = data[mask]
#print("数组形状: ", filtered_data.shape)

data1 = filtered_data[:, 3]
data2 = filtered_data[:, 4]

# 自定义x轴的范围
xmin, xmax = -0.25, 0.1

# 创建一个颜色映射：蓝 -> 绿 -> 红
cmap_list = [(0, 0, 1), (0, 1, 0), (1, 0, 0)]
cmap = colors.LinearSegmentedColormap.from_list('Custom cmap', cmap_list, N=256)

# 核心修改点：使用 TwoSlopeNorm 处理非对称数据范围
# vmin 为最小值，vcenter 为中间点(0)，vmax 为最大值
norm = colors.TwoSlopeNorm(vmin=xmin, vcenter=0.0, vmax=xmax)

# 创建散点图：直接传入原始数据 data1，并设置 norm 参数
sc = plt.scatter(data1, data2, c=data1, cmap=cmap, norm=norm, s=0.5)

# 设置坐标轴范围和标题
plt.xlim(xmin - 0.01, xmax + 0.01)
plt.ylim(0, 2.5)
plt.xlabel(r'sign($\lambda_2$)$\rho$', fontsize=16) #, fontstyle='italic')
plt.ylabel('IRI(a.u.)', fontsize=16)

# 设置刻度文字大小
plt.tick_params(labelsize=13)

# 添加颜色条：直接指定所需刻度即可，刻度和颜色会自动对齐
cbar = plt.colorbar(sc, ticks=[xmin, -0.12, 0, 0.05, xmax])

# 设置颜色条刻度标签右对齐并设置字体大小
cbar.ax.yaxis.set_tick_params(labelright=True, labelsize=12)

# 设置图形大小（单位为cm转英寸）
fig = plt.gcf()
fig.set_size_inches(19.2 / 2.54, 14.84 / 2.54)

# 更新坐标轴以适应新的图形大小
plt.tight_layout()

end = time.perf_counter()
print("elapsed time(s): {:.3f}".format(end - start))

plt.show()

# 保存图片为指定PPI的PNG文件
#plt.savefig('color_scatter_plot.png', dpi=300)

# 关闭图形窗口
plt.close()
