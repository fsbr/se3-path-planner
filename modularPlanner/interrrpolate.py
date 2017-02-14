import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
x = np.arange(0,10)
y = np.exp(-x/3.0)

#based on my testing i think that interp a generator
f = interpolate.interp1d(x,y)
x1 = np.linspace(0,10, len(f))
plt.plot(x,y)
plt.plot(x1,f)
plt.show()
