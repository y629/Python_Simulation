import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.font_manager import FontProperties
#MS明朝のフォントをフォントサイズ9として用いる（グラフの凡例とかに）
# fp = FontProperties(fname='C:\WINDOWS\Fonts\msmincho.ttc', size=9)
import math
import getparams_csv  #csvファイルからパラメータを取得するための関数群

#-------------------------------------------------------------------------------
"""
【関数名】
a
【機能】
振動の運動方程式の右辺の値を返す関数（実際には加速度a）
【入力】
t,x,v: 計算する時点での時刻、位置、速度
gamma: 減衰係数 omega: 角振動数
f0: 周期的な外力の振幅  _omega: 周期的な外力の各速度
【出力】
振動の運動方程式の右辺（加速度a）の値
【補足説明】
第1項: 減衰項
第2項: 振動項
第3項: 外力
・gammaとomegaの大小関係によって、3種類の振動を起こす
(1)gamma = omega: 臨界振動
(2)gamma < omega: 減衰振動
(3)gamma > omega: 過減衰
・omegaと_omegaがほとんど同じとき、共振が起きる（時間に比例して振幅が増大）
→gammaが小さいと分かりやすい
"""
def a(t,x,v,gamma,omega,f0,_omega):
  return - 2*gamma*v - (omega**2)*x + f0*np.cos(_omega*t)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
"""
【関数名】
LeapFrog
【機能】
振動の運動方程式をリープフロッグ法により解く
【入力】
x0: 初期位置  v0: 初速度  t0: 時刻の初期値
gamma: 減衰係数  omega: 角速度
f0: 周期的な外力の振幅  _omega: 周期的な外力の角速度
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
  #ans_xとans_vに初期値を入れておく
  ans_x = np.c_[x0]
  ans_v = np.c_[v0]
  #n_step回だけ繰り返す
  for _ in range(n_step):  #Pythonで'_'はこの変数計算には使いませんの意味（変数名'i'とかにすると警告出てうざいので）
    v_half = v + a(t,x,v,gamma,omega,f0,_omega) * (dt/2) 
    x      = x + v_half * dt
    v      = v_half + a(t,x,v,gamma,omega,f0,_omega) * (dt/2)
    #計算結果をansに格納
    ans_x = np.c_[ans_x,x]
    ans_v = np.c_[ans_v,v]
    #時刻を更新
    t += dt
  return ans_x, ans_v
#-------------------------------------------------------------------------------

def main():
  #パラメータ配列をparameters.csvから取得
  arr_n_param = getparams_csv.GetNumFromColumn("n_param","parameters.csv")
  arr_x0 = getparams_csv.GetNumFromColumn("x0","parameters.csv","float")
  arr_v0 = getparams_csv.GetNumFromColumn("v0","parameters.csv","float")
  arr_gamma = getparams_csv.GetNumArrFromColumn("gamma","parameters.csv","float")
  arr_omega = getparams_csv.GetNumArrFromColumn("omega","parameters.csv","float")
  arr_f0 = getparams_csv.GetNumFromColumn("f0","parameters.csv","float")
  arr__omega = getparams_csv.GetNumArrFromColumn("_omega","parameters.csv","float")
  arr_label = getparams_csv.GetStrArrFromColumn("label","parameters.csv")
  arr_color = getparams_csv.GetStrArrFromColumn("color","parameters.csv")
  arr_n_step = getparams_csv.GetNumFromColumn("n_step","parameters.csv")
  arr_dt = getparams_csv.GetNumFromColumn("dt","parameters.csv","float")
  arr_t0 = getparams_csv.GetNumFromColumn("t0","parameters.csv","float")
  
  #parameters.csvの各行のパラメータに対して、数値計算→グラフ＆アニメーション描画を繰り返し
  for exp_id in range(len(arr_n_param)):
    #パラメータを変数に代入
    n_param = arr_n_param[exp_id]
    x0 = np.full(n_param, arr_x0[exp_id])
    v0 = np.full(n_param, arr_v0[exp_id])
    gamma = arr_gamma[exp_id]
    omega = arr_omega[exp_id]
    f0 = np.full(n_param, arr_f0[exp_id])
    _omega = arr__omega[exp_id]
    label = arr_label[exp_id]
    color = arr_color[exp_id]
    n_step = arr_n_step[exp_id]
    dt = arr_dt[exp_id]
    t0 = arr_t0[exp_id]

    #以降の繰り返し処理の中での関数LeapFrogの返り値をまとめて1つに入れておくための配列
    ans = []
    
    #最初にt-xグラフの作成を行う
    for i in range(n_param):
      ans_x = np.array([])
      ans_v = np.array([])
      #リープフロッグ法により数値的な解を計算する
      ans_x, ans_v = LeapFrog(x0[i], v0[i], t0, gamma[i], 
                                    omega[i], f0[i], _omega[i], n_step, dt)
      ans.append(np.array([ans_x, ans_v]))
      #横軸を時刻にする
      t_axis = np.arange(0, n_step+1)
      #y軸の範囲
      #plt.ylim(-10,10)
      #labelとcolorをあらかじめ用意した配列のものにしてplot
      #ans[i][0][0,:]は、i番目のパラメータの組み合わせでの計算結果(ans[i])
      #の位置(ans[i][0])の第1次元目の成分のステップごとの値の入った1次元配列
      plt.plot(t_axis*dt, ans[i][0][0,:], label=label[i], color=color[i])
      #凡例の表示（引数にはフォントを指定）
      plt.legend()
    plt.xlim(0,300)
    plt.savefig('Vibration' + str(exp_id) + '.jpg')  #jpg形式で保存
    #plt.show() #t-xグラフを表示

    #アニメーション描画関係
    graph_list = []         #アニメーション描画のためのグラフリストを用意
    fig = plt.figure()      #データをplotするグラフを1つ用意
    for j in range(n_step):
      tmp = []
      #全ステップで描画するのは大変なので30ステップごとに描画する
      if j%30 != 0 : continue 
      for i in range(n_param):
        #jステップ目における各パラメータの組み合わせでの位置をtmpに追加していく
        tmp.append(ans[i][0][0,:][j])
      #tmpを使ってjステップ目での位置を描画
      graph = plt.scatter(np.arange(n_param), tmp, color=color)
      graph_list.append([graph])

    #アニメーションを描画(interval:フレームの切り替え間隔, repeat_delay: 繰り返し時の遅延)
    ani = animation.ArtistAnimation(fig, graph_list, interval=100, repeat_delay=500)

    #補助的な線とか
    plt.hlines(x0, 0, n_param-1, linestyle='solid', linewidth=0.5) #x=x0の補助線
    plt.hlines(0, 0, n_param-1, linestyle='dashed', linewidth=0.5) #x=0の補助線
    for i in range(n_param):  #各組合せの振れ幅を表す補助線を描画
      plt.vlines(i, min(ans[i][0][0,:]), max(ans[i][0][0,:]), linestyle='solid', linewidth=0.5,
                  label=label[i], color=color[i])
    plt.legend(bbox_to_anchor=(1.1, 0), loc='lower right', borderaxespad=0, fontsize=12) #凡例表示
    plt.show()  #アニメーション表示
    ani.save("Vibration" + str(exp_id) + ".gif", writer="pillow", fps=60)   #アニメーションをgifとして保存する
    
if __name__ == '__main__':
  main()