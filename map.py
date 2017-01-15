# i'm going to try some random map projections
:w
:q

# lets do equirectangular because I think that it's  
import numpy as np

def equirectangular():
    
    # def constants
    lam0 = 0
    rho1 = 0
    lam = np.linspace(-10,10)
    rho = np.linspace(-15,15)
    x = (lam - lam0)*np.cos(rho1)
    y = rho - rho1
    return x,y

if __name__ == "__main__":
    x1,y1 = equirectangular()
    print("x1",x1)
    print("y1",y1)
