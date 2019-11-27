import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.font_manager import FontProperties
#MS明朝のフォントをフォントサイズ9として用いる（グラフの凡例とかに）
fp = FontProperties(fname='C:\WINDOWS\Fonts\msmincho.ttc', size=9)
import math

#振動の運動方程式の右辺（実際には加速度a）------------------------
"""
・gammaとomegaの大小関係によって、3種類の振動を起こす
(1)gamma = omega: 臨界振動
(2)gamma < omega: 減衰振動
(3)gamma > omega: 過減衰
・omegaと_omegaがほとんど同じとき、共振が起きる（時間に比例して振幅が増大していく）
→gammaが小さいと分かりやすい
"""
def a(t,x,v,gamma,omega,f0,_omega):
  return - 2*gamma*v - (omega**2)*x + f0*np.cos(_omega*t)
#---------------------------------------------------------


#振動の運動方程式のリープフロッグ法による計算-------------------------------------
"""
【関数名】
LeapFrog
【機能】
振動の運動方程式をリープフロッグ法により解く
【入力】
x0: 初期位置  v0: 初速度  t0: 時刻の初期値
gamma: 減衰係数  omega: 各速度
f0: 周期的な外力の振幅  _omega: 周期的な外力の各速度
n_step: ステップ数  dt: 時間の刻み幅
【出力】
ans_x:       位置の結果を格納する配列
ans_v:       速度の結果を格納する配列
【関数内で使う変数の役割】
x, v, t: 現在の位置、速度、時刻
v_half:  リープフロッグ法で現れる半ステップ後の速度
"""
def LeapFrog(x0, v0, t0, gamma, omega, f0, _omega, n_step, dt):
  #ループに入る前に初期値を現在の値としておく
  x = x0
  v = v0
  t = t0
  #ステップ毎の位置、速度を格納する配列
  ans_x = np.array([])
  ans_v = np.array([])
  #ans_xとans_vとtotal_energyに初期値を入れておく
  ans_x = np.c_[x0]
  ans_v = np.c_[v0]
  #n_stepの回数だけ繰り返す
  for _ in range(n_step):     #Pythonで'_'はこの変数計算には使いませんの意味（変数名'i'とかにすると警告出てうざいので）
    v_half = v + a(t,x,v,gamma,omega,f0,_omega) * (dt/2) 
    x      = x + v_half * dt
    v      = v_half + a(t,x,v,gamma,omega,f0,_omega) * (dt/2)
    #計算結果をansに格納
    ans_x = np.c_[ans_x,x]
    ans_v = np.c_[ans_v,v]
    #時刻を更新
    t += dt
  return ans_x, ans_v
#----------------------------------------------------------

def main():
  #パラメータ定義
  n_param = 6 #パラメータの組み合わせ数（実験の回数）
  x0 = np.full(n_param, 20) 
  v0 = np.full(n_param, 0) 
  t0 = 0.0
  gamma = np.array([0.05,0.01,0.5,0,0,0]) 
  omega = np.array([0.05,0.6,0.1,0.25,0.3,0.3]) 
  f0 = np.full(n_param, 0.05)
  _omega = np.array([0.3,0.3,0.3,0.25,0.3,0.35])
  n_step = 10000
  dt = 0.1

  #表示時のラベルと線の色
  label = ['臨界振動','減衰振動','過減衰','共振あり(ω,_ω=0.25)','共振あり(ω,_ω=0.3)','共振なし(ω=0.3,_ω=0.35)']
  color = ['red','blue','green','orange','purple','gray']
  
  #以降の繰り返し処理の中での関数LeapFrogの返り値をまとめて1つに入れておくための配列
  ans = []
  
  for i in range(n_param):
    #リープフロッグ法により数値的な解を計算する------------------------------
    ans_x, ans_v = LeapFrog(x0[i], v0[i], t0, gamma[i], 
                                  omega[i], f0[i], _omega[i], n_step, dt)
    ans.append(np.array([ans_x, ans_v]))
    #ここからはt-xグラフの表示関係----------------------------------------------------- 
    #横軸を時刻にする
    t_axis = np.arange(0, n_step+1)
    #y軸の範囲
    #plt.ylim(-10,10)
    #labelとcolorをあらかじめ用意した配列のものにしてplot
    #ans[i][0][0,:]は、i番目のパラメータの組み合わせでの計算結果(ans[i])
    #の位置(ans[i][0])の第1次元目の成分のステップごとの値の入った1次元配列
    plt.plot(t_axis*dt, ans[i][0][0,:], label=label[i], color=color[i])
    #凡例の表示（引数にはフォントを指定）
    plt.legend(prop = fp)
  #表示
  plt.show()
  #------------------------------------------------------------

  #アニメーション描画関係---------------------------------------------------------------
  graph_list = []
  fig = plt.figure() #データをplotするグラフを1つ用意する
  for j in range(n_step):
    tmp = []
    if j%30 != 0 : continue
    for i in range(n_param):
      #jステップ目における各パラメータの組み合わせでの位置をtmpに追加していく
      tmp.append(ans[i][0][0,:][j])
    graph = plt.scatter(np.arange(n_param), tmp, color=color)
    graph_list.append([graph])

  #アニメーションを描画(interval:フレームの切り替え間隔, repeat_delay: 繰り返し時の遅延)
  ani = animation.ArtistAnimation(fig, graph_list, interval=100, repeat_delay=500)

  plt.hlines(x0, 0, n_param-1, linestyle='solid', linewidth=0.5) #x=x0の補助線
  plt.hlines(0, 0, n_param-1, linestyle='dashed', linewidth=0.5) #x=0の補助線
  for i in range(n_param):
    plt.vlines(i, min(ans[i][0][0,:]), max(ans[i][0][0,:]), linestyle='solid', linewidth=0.5,
                label=label[i], color=color[i])             #各組合せの振れ幅を表す補助線
  plt.legend(prop=fp, bbox_to_anchor=(1.1, 0), loc='lower right', borderaxespad=0, fontsize=12)
  plt.show()  #表示
  ani.save("Vibration.gif", writer="imagemagick", fps=60)   #アニメーションをgifとして保存する
  #-------------------------------------------------------------------------------------------------
 
if __name__ == '__main__':
  main()