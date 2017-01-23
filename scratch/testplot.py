import pylab as plt
x = [0,1,2]
y = [90,40,65]
labels=['high','low', 37337]
plt.plot(x,y,'r')
plt.yticks(y,labels, rotation='vertical')
plt.show()
