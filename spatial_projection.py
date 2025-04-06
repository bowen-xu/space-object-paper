from nal.truth import Truth
import matplotlib.pyplot as plt
import numpy as np
from bell_function import gbellmf


vs = []
ds = []
for d in np.linspace(0, 1, 100):
    v = Truth(d, d, 1).e
    vs.append(v)
    ds.append(d)



a = 4
c = 0
b = 0.2*2*a
xs = np.linspace(-20, 20, 500)
ys = []
for x in xs:
    y = gbellmf(x, a, b, c)
    y = Truth(y, y, 1).e
    ys.append(y)

plt.figure(figsize=(12, 2))
plt.subplot(1, 2, 1)
plt.plot(ds, vs)
plt.subplot(1, 2, 2)
plt.plot(xs, ys)
plt.show()