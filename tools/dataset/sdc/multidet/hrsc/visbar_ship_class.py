# {'Ship': 1356, 'Frigate': 484, 'Aircraft carrier': 299, 'Cargo vessel': 747, 'Destroyer': 765, 'Warship': 495, 'Submarine': 178, 'Amphibious ship': 534, 'Cruiser': 501}


import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=14) 



plt.bar(1, 747, label='Cargo vessel', color='yellow')
plt.bar(2, 765, label='Destroyer',color='green')
plt.bar(3, 178, label='Submarine',color='orange')
plt.bar(4, 534, label='Amphibious ship',color='purple')
plt.bar(5, 501, label='Cruiser',color='cyan')
plt.bar(6, 299, label='Aircraft carrier',color='magenta')
plt.bar(7, 484, label='Frigate',color='brown')
plt.bar(8, 495, label='Warship',color='red')
plt.bar(9, 1356, label='Ship',color='blue')

plt.legend()

plt.xlabel('class')
plt.ylabel('number')

plt.title(u'WHU-SDC舰船类别统计图', FontProperties=font)

plt.show()

