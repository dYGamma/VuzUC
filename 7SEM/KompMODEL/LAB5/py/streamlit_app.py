import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Define constants
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

# Define functions
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

# Streamlit UI
st.title('Control System Simulation')

# Create input widgets for parameters
T1_val = st.slider("Choose T1 value", 0.01, 1.0, 0.1)
time_interval = st.slider("Choose Time Interval", 10, 100, 20)
initial_conditions = [
    st.slider(f"Initial condition for Y1", 0.0, 10.0, 1.0),
    st.slider(f"Initial condition for Y2", 0.0, 10.0, 1.0),
    st.slider(f"Initial condition for Y3", 0.0, 10.0, 1.0)
]

# Compute solutions with and without control
time_points = np.linspace(0, time_interval, 1000)
sol_no_control = solve_ivp(no_control_system, [0, time_interval], initial_conditions, t_eval=time_points)
sol_with_control = solve_ivp(controlled_system, [0, time_interval], initial_conditions, t_eval=time_points, args=(T1_val,))

Y1_no_control, Y2_no_control, Y3_no_control = sol_no_control.y
Y1_with_control, Y2_with_control, Y3_with_control = sol_with_control.y

# Plot the results with Streamlit
st.subheader("No Control System - Variables vs Time")
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(time_points, Y1_no_control, label='Y1')
ax.plot(time_points, Y2_no_control, label='Y2')
ax.plot(time_points, Y3_no_control, label='Y3')
ax.legend()
st.pyplot(fig)

st.subheader("With Control System - Variables vs Time")
fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(time_points, Y1_with_control, label='Y1 with control')
ax.plot(time_points, Y2_with_control, label='Y2 with control')
ax.plot(time_points, Y3_with_control, label='Y3 with control')
ax.legend()
st.pyplot(fig)

# Phase plot of variables
st.subheader("Phase Plot - No Control System")
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

axes[0].plot(Y1_no_control, Y2_no_control, label='Y1 vs Y2')
axes[0].set_title('Y1 vs Y2')
axes[1].plot(Y2_no_control, Y3_no_control, label='Y2 vs Y3')
axes[1].set_title('Y2 vs Y3')
axes[2].plot(Y1_no_control, Y3_no_control, label='Y1 vs Y3')
axes[2].set_title('Y1 vs Y3')

for ax in axes:
    ax.legend()

st.pyplot(fig)

# Control response with multiple T1 values
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

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
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

st.pyplot(fig)
