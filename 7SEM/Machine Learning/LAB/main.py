import numpy as np
from matplotlib import pyplot as plt
def my_function(x):
  ### BEGIN YOUR CODE
  y1 = np.sqrt(1 - (np.abs(x) - 1) ** 2)
  y2 = np.arccos(1 - np.abs(x)) - np.pi
  return y1, y2
  ### END YOUR CODE
  ### BEGIN YOUR CODE


x = np.linspace(-2, 2, 1000)

### END YOUR CODE
y1, y2 = my_function(x)

### BEGIN YOUR CODE

y1 = np.where((1 - (np.abs(x) - 1) ** 2) >= 0, y1, np.nan)

# Построение графиков
plt.figure(figsize=(10, 6))

# График первой части функции
plt.plot(x, y1, label=r'$y_1 = \sqrt{1 - (|x| - 1)^2}$', color='blue')

# График второй части функции
plt.plot(x, y2, label=r'$y_2 = \arccos(1 - |x|) - \pi$', color='red')

# Оформление графика
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')  # Линия y = 0
plt.axvline(0, color='black', linewidth=0.8, linestyle='--')  # Линия x = 0
plt.legend(fontsize=12)
plt.title("График параметрической функции", fontsize=16)
plt.xlabel("x", fontsize=12)
plt.ylabel("y", fontsize=12)
plt.grid(True)

# Показ графика
plt.show()

### END YOUR CODE