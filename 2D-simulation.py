# %%
import numpy as np
import matplotlib.pyplot as plt

N = 12      # number of magnets
n_theta = 101
theta_res = 1.57 / (n_theta - 1)
delta_theta = 0.01      # delta for differentiation
m = 23.08 * N / 1000
g = 9.8
R = 0.01
L = 0.01 * N
I = 0.25 * m * R**2 + 0.33 * m * L**2 + m * R**2
U_table = np.loadtxt(f"{N}cm.txt")


def getU(theta):
    theta_grid = np.floor(theta / theta_res).astype(int)
    k = (theta - theta_grid * theta_res) / theta_res
    return U_table[theta_grid][1] * (1 - k) + U_table[theta_grid + 1][1] * k


def torque(theta):
    delta_U = getU(theta + delta_theta) - getU(theta)
    return m * g * (-0.5 * L * np.sin(theta) + R * np.cos(theta)) - delta_U / delta_theta

# %%
theta = np.radians(89)     # initial angle
ang_v = 0
t = 0
dt = 0.001
epsilon = 0.01
dissipation = 0.92
result = np.array([[0, 0, 0, 0]])
latch = 0
n_latch = 0
TFF = 1
while t < 3:
    ang_a = torque(theta) / I
    if theta < epsilon and latch == 0:
        ang_v *= -dissipation
        #ang_v = 45.1442-49.39926*0.96851**abs(ang_v)
        #ang_v*=-1
        latch = 1
        TFF = not TFF
        
        n_latch += 1
    elif theta > epsilon:
        ang_v += ang_a * dt
        latch = 0
    else:
        ang_v += ang_a * dt

    theta += ang_v * dt
    # print(theta)
    t += dt
    result = np.append(result, [[t, theta * (TFF * 2 - 1), ang_v, ang_a]], axis=0)
# %%
temp = np.transpose(np.delete(result, 0, 0))
plt.plot(temp[0], temp[1])
plt.show()
print(n_latch)
np.savetxt(f"sim-{N}.csv", np.delete(result, 0, 0), delimiter=",")
path = r"數據暫存.txt"
h = 0.03
with open (path,'w') as f:
    for n in temp[1]:
        f.write(str(np.degrees(n))+"\n")
f.close()
# %%
#輸出某個時間點的各項參數(用於繪製動畫)
path = r"2D - Numerical Solution.txt"
h = 0.03
with open (path,'w') as f:
  f.write(str([R,L,h,1/dt])+"\n")
  for n in range(0,len(temp[0])):
      the = temp[1][n]
      if the >=0:
          x = R+L/2*np.sin(the)-R*np.cos(the)
          z = -R*np.sin(the)-L/2*np.cos(the)
          f.write(str([temp[0][n],x,0,z,temp[1][n],0,0])+"\n")
      else:
          x = -R-L/2*np.sin(abs(the))+R*np.cos(abs(the))
          z = -R*np.sin(abs(the))-L/2*np.cos(abs(the))
          f.write(str([temp[0][n],x,0,z,temp[1][n],0,0])+"\n")
f.close()

# #%%
# data = []
# Pot = getU(np.radians(85))
# while True:
#     a = eval(input())
#     if a == -1:
#         break
#     omega = ((getU(np.radians(a))-getU(0))*2/I)**0.5
#     data.append(omega)