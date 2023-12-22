import numpy as np  
import numpy.random as npr

n = 10_000_000 # size r: 80 Mo

x = npr.uniform(0.0, 1.0, n)
y = npr.uniform(0.0, 1.0, n)

r = (x**2 + y**2 <= 1.0).astype(np.float64)
print(4.0 * np.mean(r))

# sigma = np.sqrt((np.pi/4)*(1-np.pi/4)/n )
# print(f"{4.0 * np.mean(r):.17f} ± {3*sigma:.5g}")
