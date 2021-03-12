# {'Ship': 1356, 'Frigate': 484, 'Aircraft carrier': 299, 'Cargo vessel': 747, 'Destroyer': 765, 'Warship': 495, 'Submarine': 178, 'Amphibious ship': 534, 'Cruiser': 501}


import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"C:\Windows\Fonts\simhei.ttf", size=14) 



plt.bar(1, 747, label='Cargo vessel')
plt.bar(2, 765, label='Destroyer')
plt.bar(3, 178, label='Submarine')
plt.bar(4, 534, label='Amphibious ship')
plt.bar(5, 501, label='Cruiser')
plt.bar(6, 299, label='Aircraft carrier')
plt.bar(7, 484, label='Frigate')
plt.bar(8, 495, label='Warship')
plt.bar(9, 1356, label='Ship')

plt.legend()

plt.xlabel('class')
plt.ylabel('number')

plt.title(u'WHU-SDC舰船类别统计图', FontProperties=font)

plt.show()

