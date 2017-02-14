import pandas as pd
import numpy as np

s = pd.Series([0,1, np.nan, 3])
print(s)
print(s.interpolate())
