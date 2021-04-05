import matplotlib.pyplot as plt
import numpy as np

class VisBar(object):
    def __init__(self,xlabel=None,ylabel=None,title=None):
        super(VisBar,self).__init__()
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.legend = None
    def simple_bar(self,data,dataLength,labels,colors=None):
        assert isinstance(data,(list,tuple,np.ndarray)), "data Type must be one of (list,tuple,np.ndarray)"
        if labels is not None:
            self.legend = True
            # plt.xticks(ind, labels)        
        ind = np.arange(dataLength)
        # plt.xticks(ind, labels)

        for i in range(dataLength):
            plt.bar(i+1,data[i],color=colors[i],label=labels[i])

        self.show_()
    
    def show_(self):
        if self.legend:
            plt.legend()
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.title(self.title)
        plt.show()