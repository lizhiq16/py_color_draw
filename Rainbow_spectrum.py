'''
Athor: Li ZhiQiang
Organization: JHL
Date: 2023/12/27
绘制彩虹色填充光谱图
'''

import matplotlib.pyplot as plt
import numpy as np
import re
from scipy.interpolate import interp1d

# 从文件中读取波长和光强数据，原数据可以采用逗号或者空格分隔
with open('spectrum_data1.txt', 'r') as file:
    lines = file.readlines()
    data = [[float(item) for item in re.split(r'[ ,]+', line)] for line in lines]
    wavel0, intens0 = zip(*[(line[0],line[1]) for line in data])

#为了增加效果，用scipy.interpolate的interp1d插值
f = interp1d(wavel0, intens0, kind='cubic')	# kind=zero, linear, quadratic, cubic
wave_num=int(2*abs(wavel0[0]-wavel0[-1])+1)
wavelengths=np.linspace(wavel0[0],wavel0[-1],wave_num)
intensities=f(wavelengths)

# 自定义彩虹渐变填充方案
num_points = len(wavelengths)
colors = np.zeros((num_points, 3))  # 创建一个RGB颜色的数组

# 根据波长范围确定颜色渐变
i = 0
while i < num_points:
    wavelength = wavelengths[i]
    if wavelength < 380:
        count = 0
        while i + count < num_points and wavelengths[i + count] < 380:
            count += 1
        colors[i:i + count] = (255, 255, 255)
        i += count
    elif 380 <= wavelength < 400:
        count = 0
        while i + count < num_points and 380 <= wavelengths[i + count] < 400:
            count += 1
        colors[i:i + count] = np.linspace((97, 0, 97), (131, 0, 181), count)
        i += count
    elif 400 <= wavelength < 440:
        count = 0
        while i + count < num_points and 400 <= wavelengths[i + count] < 440:
            count += 1
        colors[i:i + count] = np.linspace((131, 0, 181), (0, 0, 255), count)
        i += count
    elif 440 <= wavelength < 490:
        count = 0
        while i + count < num_points and 440 <= wavelengths[i + count] < 490:
            count += 1
        colors[i:i + count] = np.linspace((0, 0, 255), (0, 255, 255), count)
        i += count
    elif 490 <= wavelength < 510:
        count = 0
        while i + count < num_points and 490 <= wavelengths[i + count] < 510:
            count += 1
        colors[i:i + count] = np.linspace((0, 255, 255), (0, 255, 0), count)
        i += count
    elif 510 <= wavelength <= 576:
        count = 0
        while i + count < num_points and 510 <= wavelengths[i + count] <= 576:
            count += 1
        colors[i:i + count] = np.linspace((0, 255, 0), (255, 255, 0), count)
        i += count
    elif 576 < wavelength < 584:
        count = 0
        while i + count < num_points and 576 < wavelengths[i + count] < 584:
            count += 1
        colors[i:i + count] = (255, 255, 0)
        i += count    
    elif 584 <= wavelength < 650:
        count = 0
        while i + count < num_points and 584 <= wavelengths[i + count] < 650:
            count += 1
        colors[i:i + count] = np.linspace((255, 255, 0), (255, 0, 0), count)
        i += count
    elif 650 <= wavelength < 700:
        count = 0
        while i + count < num_points and 650 <= wavelengths[i + count] < 700:
            count += 1
        colors[i:i + count] = (255, 0, 0)
        i += count
    elif 700 <= wavelength < 780:
        count = 0
        while i + count < num_points and 700 <= wavelengths[i + count] < 780:
            count += 1
        colors[i:i + count] = np.linspace((255, 0, 0), (100, 0, 0), count)
        i += count
    elif wavelength >= 780:
        count = 0
        while i + count < num_points and wavelengths[i + count] >= 780:
            count += 1
        colors[i:i + count] = (255, 255, 255)
        i += count

# 绘制曲线和底色填充
plt.plot(wavelengths, intensities, 'k-')  # 绘制黑色曲线
# plt.fill_between(wavelengths, intensities, color='none', edgecolor='none', alpha=0.3)

# 仅在380-780波长范围内填充彩虹渐变色
for i in range(num_points - 1):
    plt.fill_between(wavelengths[i:i+2], intensities[i:i+2], color=colors[i] / 255, alpha=1)

# 调整坐标轴范围
plt.ylim(0,)
plt.xlim(380, 780)
#plt.xlim(np.min(wavelengths), np.max(wavelengths))
plt.xlabel('Wavelength(nm)', fontsize=12)
plt.ylabel('Intensity(a.u.)', fontsize=12)

# 更新坐标轴以适应新的图形大小
plt.tight_layout()

#plt.show()

# 保存图片为指定PPi的PNG文件
plt.savefig('Rainbow_spectrum.png', dpi=300)

# 关闭图形窗口
plt.close()
