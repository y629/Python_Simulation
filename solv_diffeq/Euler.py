import matplotlib.pyplot as plt
import numpy as np


# dx/dt=x
def func1(x):
    return x

#dx/dt=a-bx
def func2(a, b, x):
    return a-b*x

n = 10000    # ステップ数
dt = 0.01   # tの刻み幅
x0 = 1.0    # 初期条件

# t, x の値を格納するリスト
t_list = []
x_list = []
st = []    # 解析解を格納するリスト

# t=0 では x=x0
t = 0.0
x = x0

# 値を格納する
t_list.append(t)
x_list.append(x)
st.append(10.0)

for i in range(n):
    f = func2(1.0,0.1,x)           # dx/dtの値を予め計算
    x = x + f * dt  # 前進Euler法による時間発展
    t = t + dt      # 時刻をdtだけ進める

    # 計算した x, t の格納
    t_list.append(t)
    x_list.append(x)
    st.append(10.0)

# グラフに結果を描画する。
plt.plot(t_list, x_list, label='simulation')
plt.plot(t_list, st, linestyle='dotted')
plt.xlabel('t')
plt.ylabel('x')
# 表示
plt.show()