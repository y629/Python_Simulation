import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 描画関係
fig = plt.figure()
ax = Axes3D(fig)

# const
p = 10
r = 28
b = 8/3
dt = 0.01
t_0 = 0
t_1 = 100
X_0 = np.array([2, 2, 2])
Y_0 = np.array([2, 2, 2])

# function
def RungeKutta(t, X):
  k_1 = LorenzEquation(t, X)
  k_2 = LorenzEquation(t + dt/2, X + k_1*dt/2)
  k_3 = LorenzEquation(t + dt/2, X + k_2*dt/2)
  k_4 = LorenzEquation(t + dt, X + k_3*dt)
  X_next = X + dt/6*(k_1 + 2*k_2 + 2*k_3 + k_4)
  return X_next

def Euler(t, X):
  X_next = X + dt * LorenzEquation(t, X)
  return X_next

def LorenzEquation(t, X):
  x = X[0]
  y = X[1]
  z = X[2]
  return np.array([-p*x + p*y, -x*z + r*x - y, x*y - b*z])

# main process
t = t_0
X = X_0
Y = Y_0
data = np.r_[X]
data2= np.r_[Y]

while t < t_1:
  X = RungeKutta(t, X)
  Y = Euler(t, Y)
  t += dt
  data = np.c_[data, X]
  data2 = np.c_[data2, Y]

ax.plot(data[0,:], data[1,:], data[2,:])
ax.plot(data2[0,:], data2[1,:], data2[2,:])
print(data)
plt.show()
