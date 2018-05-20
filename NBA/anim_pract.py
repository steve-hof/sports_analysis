import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation


ball_data = np.array([[18.66905, 25.09811, 3.82307],
                      [18.62729, 25.11722, 3.95278],
                      [18.51251, 25.15848, 4.06811],
                      [18.49461, 25.2866, 4.41862],
                      [18.42623, 25.31528, 4.69615],
                      [18.37218, 25.16831, 4.68956],
                      [18.36018, 25.15535, 5.01618],
                      [18.46825, 25.2354, 5.22848],
                      [18.46782, 25.19683, 5.30094],
                      [18.56269, 25.01828, 5.49274]])
no_z = ball_data[:, :2]
cleaned_ball_data = no_z.T

fig = plt.figure()
# ax = plt.axes(xlim=(18, 19), ylim=(25, 26))
ax = plt.axes(xlim=(0, 100), ylim=(0, 50))

patch = plt.Circle((18, 25), .1, fc='r')


def init():
    ax.add_patch(patch)
    return patch,


def animate(i):
    # patch.set_width(.05)
    # patch.set_height(.05)
    x = cleaned_ball_data[0, i]
    y = cleaned_ball_data[1, i]
    # patch.set_xy([cleaned_ball_data[0, i], cleaned_ball_data[1, i]])
    # patch._angle = -np.rad2deg(yaw[i])
    patch.center = (x, y)
    return patch,


anim = animation.FuncAnimation(fig, animate,
                               init_func=init,
                               frames=len(cleaned_ball_data[0]),
                               interval=700,
                               blit=True)
plt.show()
