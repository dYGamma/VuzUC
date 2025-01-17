import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


alpha_val = 4
beta_val = 9
gamma_val = 1.7
mu_val = 2.2
lambda_val = 3.12
delta_val = 0.7
rho_val = 0.5
T1_val = [1]
time_interval = 20
time_points = np.linspace(0, time_interval, 1000)
initial_conditions = [1, 1, 1]

def calc_psi(v2, v3):
    return v3 - rho_val * v2

def calc_u(v1, v2, v3, T1_val):
    return lambda_val * v3 - delta_val * v2 + rho_val * (mu_val * (v2 + v3) - beta_val * v1 * v3) - calc_psi(v2, v3) / T1_val

def no_control_system(t, vars):
    v1, v2, v3 = vars
    dv1_dt = alpha_val * v2 * v3 - gamma_val * v1
    dv2_dt = mu_val * (v2 + v3) - beta_val * v1 * v3
    dv3_dt = delta_val * v2 - lambda_val * v3
    return [dv1_dt, dv2_dt, dv3_dt]

def extract_macro_and_control(t, vars):
    v1, v2, v3 = vars
    psi_val = calc_psi(v2, v3)
    u_val = calc_u(v1, v2, v3, T1_val)
    return psi_val, u_val

def controlled_system(t, vars, T1_val):
    v1, v2, v3 = vars
    control_val = calc_u(v1, v2, v3, T1_val)
    dv1_dt = alpha_val * v2 * v3 - gamma_val * v1
    dv2_dt = mu_val * (v2 + v3) - beta_val * v1 * v3
    dv3_dt = delta_val * v2 - lambda_val * v3 + control_val
    return [dv1_dt, dv2_dt, dv3_dt]


sol_no_control = solve_ivp(no_control_system, [0, time_interval], initial_conditions, t_eval=time_points)
sol_with_control = solve_ivp(controlled_system, [0, time_interval], initial_conditions, t_eval=time_points, args=T1_val)

Y1_no_control, Y2_no_control, Y3_no_control = sol_no_control.y
Y1_with_control, Y2_with_control, Y3_with_control = sol_with_control.y

psi_with_control_vals = [extract_macro_and_control(ti, [Y1_with_control[i], Y2_with_control[i], Y3_with_control[i]])[0] for i, ti in enumerate(time_points)]
u_with_control_vals = [extract_macro_and_control(ti, [Y1_with_control[i], Y2_with_control[i], Y3_with_control[i]])[1] for i, ti in enumerate(time_points)]


plt.figure(figsize=(12, 10))

plt.plot(time_points, Y1_no_control, label='Y1')

plt.plot(time_points, Y2_no_control, label='Y2')

plt.plot(time_points, Y3_no_control, label='Y3')
plt.legend()
plt.show()

plt.figure(figsize=(12, 10))
plt.subplot(1, 3, 1)

plt.plot(Y1_no_control, Y2_no_control, label='Y1 vs Y2')
plt.title('Y1 vs Y2')
plt.legend()

plt.subplot(1, 3, 2)
plt.plot(Y2_no_control, Y3_no_control, label='Y2 vs Y3')
plt.legend()
plt.title('Y2 vs Y3')

plt.subplot(1, 3, 3)
plt.plot(Y1_no_control, Y3_no_control, label='Y1 vs Y3')
plt.title('Y1 vs Y3')
plt.legend()
plt.show()

plt.figure(figsize=(12, 10))
plt.plot(time_points, Y1_with_control, label='Y1 with control')

plt.plot(time_points, Y2_with_control, label='Y2 with control')

plt.plot(time_points, Y3_with_control, label='Y3 with control')

plt.legend()
plt.show()

T1_values = [0.01, 0.05, 0.1, 0.5, 0.85]
results = {T1: None for T1 in T1_values}
for T1 in T1_values:
    sol = solve_ivp(
        controlled_system,
        [0, time_interval],
        initial_conditions,
        t_eval=time_points,
        args=(T1,)
    )
    results[T1] = sol.y

fig, axes = plt.subplots(1, 3, figsize=(18, 5))  # 3 подграфика в строку

titles = ['Y1', 'Y2', 'Y3']

for i, ax in enumerate(axes):
    for T1 in T1_values:
        ax.plot(
            time_points,
            results[T1][i],
            label=f'T1 = {T1}',
            linestyle='--'
        )
    ax.set_title(titles[i])
    ax.legend()

plt.tight_layout()
plt.show()

plt.figure(figsize=(18, 12))

plt.subplot(3, 1, 1)
for T1 in T1_values:
    sol = solve_ivp(controlled_system, [0, time_interval], initial_conditions,
                    t_eval=time_points, args=(T1,))
    Y1, Y2, Y3 = sol.y
    plt.plot(Y1, Y2, label=f"T1 = {T1}")
plt.title("Y1 vs Y2")
plt.legend()

plt.subplot(3, 1, 2)
for T1 in T1_values:
    sol = solve_ivp(controlled_system, [0, time_interval], initial_conditions,
                    t_eval=time_points, args=(T1,))
    Y1, Y2, Y3 = sol.y
    plt.plot(Y2, Y3, label=f"T1 = {T1}")
plt.title("Y2 vs Y3")
plt.legend()

plt.subplot(3, 1, 3)
for T1 in T1_values:
    sol = solve_ivp(controlled_system, [0, time_interval], initial_conditions,
                    t_eval=time_points, args=(T1,))
    Y1, Y2, Y3 = sol.y
    plt.plot(Y1, Y3, label=f"T1 = {T1}")
plt.title("Y1 vs Y3")
plt.legend()

plt.tight_layout()
plt.show()


plt.figure(figsize=(18, 12))

for idx, T1 in enumerate(T1_values):
    sol = solve_ivp(controlled_system, [0, time_interval], initial_conditions,
                    t_eval=time_points, args=(T1,))
    Y1, Y2, Y3 = sol.y

    plt.subplot(3, len(T1_values), idx + 1)
    plt.plot(Y1, Y2, label=f"T1 = {T1}")
    plt.title(f"Y1 vs Y2")
    plt.legend()

    plt.subplot(3, len(T1_values), idx + len(T1_values) + 1)
    plt.plot(Y2, Y3, label=f"T1 = {T1}")
    plt.title(f"Y2 vs Y3")
    plt.legend()

    plt.subplot(3, len(T1_values), idx + 2 * len(T1_values) + 1)
    plt.plot(Y1, Y3, label=f"T1 = {T1}")
    plt.title(f"Y1 vs Y3")
    plt.legend()

plt.tight_layout()
plt.show()

plt.figure(figsize=(18, 12))

psi_vals_dict = {}
u_vals_dict = {}

time_interval = 6
time_points = np.linspace(0, time_interval, 1000)
for T1_val in T1_values:
    sol = solve_ivp(controlled_system, [0, time_interval], initial_conditions, t_eval=time_points, args=(T1_val,))
    Y1, Y2, Y3 = sol.y
    t_vals = sol.t

    psi_vals = []
    u_vals = []

    for t, vars in zip(t_vals, zip(Y1, Y2, Y3)):
        psi, u = extract_macro_and_control(t, vars)
        psi_vals.append(psi)
        u_vals.append(u)
    u_vals_clipped = np.clip(u_vals, -10, 20)
    psi_vals_dict[T1_val] = psi_vals
    u_vals_dict[T1_val] = u_vals_clipped

plt.subplot(2, 1, 1)
for T1_val in T1_values:
    plt.plot(t_vals, psi_vals_dict[T1_val], label=f"T1 = {T1_val}")
plt.title("$\psi(t)$")
plt.legend()

plt.subplot(2, 1, 2)
for T1_val in T1_values:
    plt.plot(t_vals, u_vals_dict[T1_val], label=f"T1 = {T1_val}")
plt.title("$u(t)$")
plt.legend()

plt.tight_layout()
plt.show()
