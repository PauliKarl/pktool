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
    N = 16
    # {'Cargo vessel': 4398, 'Ship': 2375, 'Motorboat': 1809, 'Fishing boat': 937, 'Destroyer': 659, 'Tugboat': 559, 'Loose pulley': 509, 'Warship': 409, 'Engineering ship': 374, 'Amphibious ship': 380, 'Cruiser': 359, 'Frigate': 301, 'Submarine': 288, 'Aircraft carrier': 249, 'Hovercraft': 113, 'Command ship': 114}
    xlabel = ('Carg.', 'Ship', 'Moto.', 'Fish.', 'Dest.','Tugb.', 'Loos.', 'Wars.', 'Engi.', 'Amph.', 'Crui.', 'Frig.','Subm.','Airc.','Hove.','Comm.')

    # {'Cargo vessel': 1131, 'Ship': 552, 'Motorboat': 801, 'Fishing boat': 477, 'Destroyer': 140, 'Tugboat': 101, 'Loose pulley': 119, 'Warship': 117, 'Engineering ship': 133, 'Amphibious ship': 105, 'Cruiser': 90, 'Frigate': 99, 'Submarine': 58, 'Aircraft carrier': 53, 'Hovercraft': 13, 'Command ship': 28}
    Tval =(4398,2375,1809,937,659,559,509,409,374,380,359,301,288,249,113,114)
    Test = (1131,552,801,477,140,101,119,117,133,105,90,99,58,53,13,28)

    ind = np.arange(N)    # the x locations for the groups
    width = 0.5       # the width of the bars: can also be len(x) sequence
    
    p1 = plt.bar(ind, Tval, width, color='Blue')#, yerr=menStd)
    p2 = plt.bar(ind, Test, width, color='Red',bottom=Tval)#, yerr=womenStd)
    # p3 = plt.bar(ind, M, width, bottom=d)

    plt.ylabel('Instances')
    plt.title('Instance with trainval and test')
    plt.xticks(ind, xlabel)

    plt.yticks(np.arange(0, 5500, 500))
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

    # simple_bar_sdc()
    added_bar()