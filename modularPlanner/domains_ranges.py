# I'm not sure if this is the most productive thing that I can be doing.

import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(-4*np.pi, 4*np.pi)
x = np.arctan(t)
plt.plot(t,x)
plt.title('arctangent')
plt.show()

x1 = np.arcsin(t)
plt.plot(t,x1)
plt.title('arcsin')
plt.show()
print('x1', x1)
