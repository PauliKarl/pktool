import matplotlib.pyplot as plt
import numpy as np

def simple_bar_sdc():
    #  {'Warship': 526, 'Cruiser': 449, 'Destroyer': 799, 'Amphibious ship': 485, 'Ship': 2927, 'Cargo vessel': 5529, 'Command ship': 142, 'Aircraft carrier': 302, 'Frigate': 400, 'Loose pulley': 628, 'Submarine': 346, 'Hovercraft': 126, 'Motorboat': 2610, 'Fishing boat': 1414, 'Tugboat': 660, 'Engineering ship': 507}
    labels=('Cargo vessel','Other ship','Motorboat','Fishing boat','Destroyer','Tugboat','Loose pulley','Warship','Engineering ship','Amphibious ship','Cruiser','Frigate','Submarine','Aircraft carrier','Command ship','Hovercraft')
    Tval = (5529,2927,2610,1414,799,660,628,526,507,485,449,400,346,302,142,126)
    colors = ('blue','green','yellow','purple','cyan','brown','Red','orange','magenta','Lime','Teal','Maroon','#808080','#FFD7B4','#FFFAC8','#808000')

    for i in range(len(Tval)):
        plt.bar(i+1, Tval[i], label=labels[i],color=colors[i])
    plt.legend()
    plt.xlabel('category')
    plt.ylabel('instances number')
    plt.title('WHU-SDC dataset')

    plt.show()
    
def simple_bar():
    """简单柱状图
    """
    labels = ('Others', 'Dest.', 'Carg.', 'Amph.', 'Crui.','Frig.', 'Wars.', 'Subm.', 'Airc.', 'Comm.', 'Hove.', 'Loos.')
    Tval =(1369,672,573,382,359,303,304,299,250,113,113,13)
    colors = ('blue','green','yellow','purple','cyan','brown','Red','orange','magenta','Lime','Teal','Maroon',)
    for i in range(len(Tval)):
        plt.bar(i+1, data[i], label=labels[i],color=colors[i])

    plt.legend()
    plt.xlabel('class')
    plt.ylabel('instances number')
    plt.title('CLASSES  cover WHU-SDC dataset')

    plt.show()

def added_bar():
    """叠加柱状图
    """
    N = 12
    # xlabel = ('Other ship', 'Destroyer', 'Cargo vessel', 'Amphibious ship', 'Cruiser','Frigate', 'Warship', 'Submarine', 'Aircraft carrier', 'Command ship', 'Hovercraft', 'Loose pulley')
    xlabel = ('Others', 'Dest.', 'Carg.', 'Amph.', 'Crui.','Frig.', 'Wars.', 'Subm.', 'Airc.', 'Comm.', 'Hove.', 'Loos.')
    Tval =(1369,672,573,382,359,303,304,299,250,113,113,13)
    #{'Destroyer': 672, 'Warship': 304, 'Cruiser': 359, 'Amphibious ship': 382, 'Aircraft carrier': 250, 'Ship': 1369, 'Frigate': 303, 'Cargo vessel': 573, 'Command ship': 113, 'Submarine': 299, 'Loose pulley': 13, 'Hovercraft': 113}
    Test = (324,148,124,103,91,97,72,59,52,29,13,3)
    #{'Cargo vessel': 124, 'Destroyer': 148, 'Amphibious ship': 103, 'Ship': 324, 'Frigate': 97, 'Warship': 72, 'Cruiser': 91, 'Submarine': 59, 'Aircraft carrier': 52, 'Command ship': 29, 'Hovercraft': 13, 'Loose pulley': 3}
    ind = np.arange(N)    # the x locations for the groups
    width = 0.5       # the width of the bars: can also be len(x) sequence
    
    p1 = plt.bar(ind, Tval, width, color='Blue')#, yerr=menStd)
    p2 = plt.bar(ind, Test, width, color='Red',bottom=Tval)#, yerr=womenStd)
    # p3 = plt.bar(ind, M, width, bottom=d)

    plt.ylabel('Instances')
    plt.title('Instance with trainval and test')
    plt.xticks(ind, xlabel)

    plt.yticks(np.arange(0, 2000, 500))
    plt.legend((p1[0], p2[0]), ('trainval', 'test'))
    plt.show()

def polar_bar():
    #极轴饼图
    np.random.seed(19680801)
    N=10
    theta = np.linspace(0.0,2*np.pi,N,endpoint=False)
    radii = 100*np.random.rand(N)
    width = np.pi/8*np.random.rand(N)
    ax = plt.subplot(111,projection='polar')

    bars = ax.bar(theta,radii,width=width,bottom=0.5)

    for r, bar in zip(radii,bars):
        bar.set_facecolor(plt.cm.viridis(r/100.))
        bar.set_alpha(0.5)
    plt.show()
    
if __name__=="__main__":

    simple_bar_sdc()