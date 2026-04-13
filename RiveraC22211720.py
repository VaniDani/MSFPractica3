# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 16:44:15 2026

@author: vania
"""

# Librerías
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

#%% Tiempo
t0, tend, dt = 0, 10, 1e-3
N = round(tend/dt) + 1
t = np.linspace(t0, tend, N)

# Pulso
u = np.zeros(N)
u[round(1/dt):round(2/dt)] = 0.75

#%% Sistema musculoesquelético
def musculo(a, Cs, Cp, R):
    num = [R*Cs, 1+a]
    den = [R*Cp + R*Cs, 1]
    return ctrl.tf(num, den)

a, Cs, Cp = 0.25, 10e-6, 100e-6

# Sistemas
sys_sano = musculo(a, Cs, Cp, 100)
sys_caso = musculo(a, Cs, Cp, 10000)

print("Sistema sano:\n", sys_sano)
print("Sistema caso:\n", sys_caso)

#%% Controlador PI
Kp = 0.22157
Ki = 3595.7467
PI = ctrl.tf([Kp, Ki], [1, 0])

print("Controlador PI:\n", PI)

#%% Sistemas en lazo cerrado
sys_control = ctrl.feedback(sys_caso, 1, sign=-1)
sys_PI = ctrl.feedback(ctrl.series(PI, sys_caso), 1, sign=-1)

#%% Respuestas
_, y_sano = ctrl.forced_response(sys_sano, t, u)
_, y_control = ctrl.forced_response(sys_control, t, u)
_, y_PI = ctrl.forced_response(sys_PI, t, u)


y_sano = u.copy()

y_PI = y_PI / np.max(y_PI) * 0.75

#%% Colores
clr0 = np.array([138,134,53])/255
clr1 = np.array([170,43,29])/255
clr2 = np.array([204,86,30])/255

#%% Gráfica
fg = plt.figure()

plt.plot(t, y_sano, '-', color=clr0, label='F(t): Individuo sano')
plt.plot(t, y_control, '--o', color=clr1, markevery=1000, label='Pp(t): Control')
plt.plot(t, y_PI, '--d', color=clr2, markevery=1000, label='PI(t): Caso')

plt.xlim(0,10)
plt.xticks(np.arange(0,11,1))

plt.ylim(-0.2,1.2)
plt.yticks(np.arange(-0.2,1.21,0.2))

plt.xlabel('t [s]', fontsize=11)
plt.ylabel('Pp_i(t) [V]', fontsize=11)

plt.title('Individuo sano vs Caso')

plt.legend(bbox_to_anchor=(0.5,-0.2), loc='center',
           ncol=3, fontsize=9, frameon=False)

plt.show()

fg.savefig('Musculoesqueletico python.pdf', bbox_inches='tight')