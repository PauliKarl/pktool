# #{'航母': 305, '军舰': 1403, '商船': 540, '船': 624, '潜艇': 104}
# #(Aircraft carrier)、军舰(Warcraft)、商船(Merchant Ship)、潜艇(submarine)和其他(other ship)
# import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties
# font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=14)  
# plt.bar(1, 305, label='Aircraft carrier')
# plt.bar(2, 1403, label='Warcraft')
# plt.bar(3, 540, label='Merchant Ship')
# plt.bar(4, 104, label='Submarine')
# plt.bar(5, 624, label='Other Ship')
# # params

# # x: 条形图x轴
# # y：条形图的高度
# # width：条形图的宽度 默认是0.8
# # bottom：条形底部的y坐标值 默认是0
# # align：center / edge 条形图是否以x轴坐标为中心点或者是以x轴坐标为边缘
# plt.legend()
# plt.xlabel('class')
# plt.ylabel('number')
# plt.title(u'HRSC舰船多类别统计图', FontProperties=font)
# plt.show()

#####xview

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=14) 

plt.bar(1, 305, label='Maritime Vessel')
plt.bar(2, 1403, label='Motorboat')
plt.bar(3, 540, label='Sailboat')
plt.bar(4, 104, label='Tugboat')
plt.bar(5, 624, label='Barge')
plt.bar(6, 624, label='Fishing Vessel')
plt.bar(7, 624, label='Ferry')
plt.bar(8, 624, label='Yacht')
plt.bar(9, 624, label='Container Ship')
plt.bar(10, 624, label='Oil Tanker')
# params
##{'Maritime Vessel', 'Motorboat', 'Sailboat', 'Tugboat', 'Barge', 'Fishing Vessel', 'Ferry', 'Yacht', 'Container Ship','Oil Tanker'}
# x: 条形图x轴
# y：条形图的高度
# width：条形图的宽度 默认是0.8
# bottom：条形底部的y坐标值 默认是0
# align：center / edge 条形图是否以x轴坐标为中心点或者是以x轴坐标为边缘
plt.legend()
plt.xlabel('class')
plt.ylabel('number')
plt.title(u'xView舰船多类别统计图', FontProperties=font)
plt.show()
