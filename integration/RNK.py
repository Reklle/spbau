import numpy as np
import matplotlib.pyplot as plt
Dt = 0.01               # timestep Delta t
Y_start = 20            # initial Y
P_start = 20            # initial P
t_start = 0             # starttime
t_end = 60              # endtimen_steps = int(round((t_end-t_start)/Dt))
n_steps = int(round((t_end-t_start)/Dt))    # number of timesteps
Y_arr = np.zeros(n_steps + 1)   # create an array of zeros for Y
P_arr = np.zeros(n_steps +1)    # create an array of zeros for P
t_arr = np.zeros(n_steps + 1)   # create an array of zeros for t
t_arr[0] = t_start              # add starttime to array
Y_arr[0] = Y_start              # add initial value of Y to array
P_arr[0] = P_start              # add initial value of P to array

# Euler's method
for i in range (1, n_steps + 1):
   Y = Y_arr[i-1]
   P = P_arr[i-1]
   t = t_arr[i-1]
   dYdt = -0.4*Y +0.02*P*Y
   dPdt = 0.8*P - 0.01*P*P-0.1*P*Y
   Y_arr[i] = Y + Dt*dYdt
   P_arr[i] = P + Dt*dPdt
   t_arr[i] = t + Dt     

# plotting the result
fig = plt.figure()                                  # create figure
plt.plot(t_arr, Y_arr, linewidth = 4, label = 'Y')    # plot Y to t
plt.plot(t_arr, P_arr, linewidth = 4, label = 'P')    # plot P to tplt.title('Title', fontsize = 12)    # add some title to your plot
plt.xlabel('t (in seconds)', fontsize = 12)
plt.ylabel('Y(t), P(t)', fontsize = 12)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)
plt.grid(True)                        # show grid
plt.axis([t_start, t_end, 0, 50])     # show axes measures
plt.legend()
plt.show()