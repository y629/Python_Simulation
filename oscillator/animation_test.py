#######
#2019/4/29 TanTan
#Animation easy
#######
 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
 
fig = plt.figure() #データをplotするグラフを1つ用意する
"""
plt.xlim(0, 200) #表示するx軸の範囲を設定
plt.ylim(0, 200) #表示するy軸の範囲を設定
plt.xlabel("x axis")   #x軸の説明
plt.ylabel("y axis")   #y軸の説明
plt.gca().set_aspect('equal', adjustable='box') #グラフ範囲を真四角する
 
graph_list = [] #各時刻でのグラフを全て格納する場所を用意する
for i in range(100): #100個のグラフを作成して、1つのアニメーションにする
    x = i       #xの値の変化
    y1 = i      #yの値の変化
    y2 = 2*i
    y3 = 3*i
    y4 = 4*i
    y5 = 5*i
    y6 = 6*i
    z = [y1,y2,y3,y4,y5,y6]
    graph = plt.scatter(np.full(len(z),x), z, color="black") #座標(x, y)に点をlen(z)個打ったグラフを作成
    graph_list.append([graph])               #上記のグラフをgraph_listへ格納する
 
ani = animation.ArtistAnimation(fig, graph_list, interval=10) #graph_list内のグラフを連続的に繋げて、200ms毎に表示するアニメーションにする
plt.show()  #アニメーションを表示する
ani.save("output_easy.gif", writer="imagemagick")   #アニメーションをgifとして保存する
"""
#2点(x0,y0),(x1,y1)を結ぶ直線
#plt.plot([x0,x1],[y0,y1])
plt.plot([1,10],[2,1000])
plt.show()