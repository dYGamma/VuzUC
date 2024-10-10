# 1. Импорт необходимых библиотек
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GRU, SimpleRNN  # Добавлено: SimpleRNN
from sklearn.model_selection import GridSearchCV
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.linear_model import LinearRegression  # Добавлено: LinearRegression
import joblib
import os  # Добавлено: для работы с файлами
from datetime import datetime  # Добавлено: для записи времени в файл

# 2. Загрузка данных
column_names = ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model_year', 'origin', 'car_name']
column_names_filtred = ['mpg','cylinders','weight']
df = pd.read_csv('V10.txt', delim_whitespace=True, names=column_names)

# 3. Разведочный анализ данных (EDA)
# a. Описательная статистика
print(df.describe())
print(df.info())

# b. Визуализация
# Одномерная
df.hist(figsize=(12, 8))
plt.show()

# Создание одномерных графиков плотности для данных в df
df[column_names_filtred].plot(kind='density', subplots=True, layout=(1, 3), sharex=False, legend=True, fontsize=12, figsize=(12, 4))
plt.show()

# Многомерная
sns.pairplot(df)
plt.show()

# 4. Очистка данных
# Преобразование 'horsepower' в числовой тип и заполнение пропущенных значений медианой
df['horsepower'] = pd.to_numeric(df['horsepower'], errors='coerce')
df['horsepower'] = df['horsepower'].fillna(df['horsepower'].median())
df['hppercil'] = df['horsepower'] / df['cylinders']
# Удаление столбца 'car_name', так как он не влияет на предсказание расхода топлива
df.drop(columns=['car_name'], inplace=True)

# 5. Анализ корреляций
plt.figure(figsize=(10, 8))
sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm')
plt.show()

# 6. Создание признаков
# Использование OneHotEncoder для категориальных признаков
categorical_features = ['cylinders', 'model_year', 'origin']
continuous_features = ['displacement', 'horsepower', 'weight', 'acceleration']

# Преобразование категориальных и числовых признаков
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), continuous_features),
        ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_features)
    ])

# 7. Разделение данных на обучающую, тестовую и валидационную выборки
X = df.drop(columns=['mpg'])
y = df['mpg']
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)  # Изменено: тестовая + валидационная
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)  # Разделение на тестовую и валидационную

# Создание пайплайна для обработки данных
pipeline = Pipeline(steps=[('preprocessor', preprocessor)])

# Предобработка данных с использованием пайплайна
X_train_processed = pipeline.fit_transform(X_train)
X_val_processed = pipeline.transform(X_val)  # Добавлено: валидационная выборка
X_test_processed = pipeline.transform(X_test)

# 8. Модель 1: Полносвязная нейронная сеть
model_fc = Sequential()
model_fc.add(Dense(128, input_dim=X_train_processed.shape[1], activation='relu'))
model_fc.add(Dense(64, activation='relu'))
model_fc.add(Dense(1))
model_fc.compile(optimizer='adam', loss='mse', metrics=['mae'])

history_fc = model_fc.fit(X_train_processed, y_train, validation_data=(X_val_processed, y_val), epochs=100, batch_size=32)

# 9. Модель 2: Нейронная сеть на основе GRU
# Изменение формы данных для подачи в GRU
X_train_gru = X_train_processed.reshape((X_train_processed.shape[0], 1, X_train_processed.shape[1]))
X_val_gru = X_val_processed.reshape((X_val_processed.shape[0], 1, X_val_processed.shape[1]))  # Добавлено
X_test_gru = X_test_processed.reshape((X_test_processed.shape[0], 1, X_test_processed.shape[1]))

model_gru = Sequential()
model_gru.add(GRU(128, input_shape=(1, X_train_processed.shape[1]), return_sequences=True))
model_gru.add(GRU(64))
model_gru.add(Dense(1))
model_gru.compile(optimizer='adam', loss='mse', metrics=['mae'])

history_gru = model_gru.fit(X_train_gru, y_train, validation_data=(X_val_gru, y_val), epochs=100, batch_size=32)

# 10. Модель 3: Линейная Регрессия (Добавлено)
model_lr = LinearRegression()
model_lr.fit(X_train_processed, y_train)

# 11. Модель 4: Простая RNN (Добавлено)
# Изменение формы данных для подачи в SimpleRNN
X_train_rnn = X_train_processed.reshape((X_train_processed.shape[0], 1, X_train_processed.shape[1]))
X_val_rnn = X_val_processed.reshape((X_val_processed.shape[0], 1, X_val_processed.shape[1]))
X_test_rnn = X_test_processed.reshape((X_test_processed.shape[0], 1, X_test_processed.shape[1]))

model_rnn = Sequential()
model_rnn.add(SimpleRNN(150, activation='relu', input_shape=(1, X_train_processed.shape[1])))
model_rnn.add(Dense(1))
model_rnn.compile(optimizer='adam', loss='mean_squared_error')

history_rnn = model_rnn.fit(X_train_rnn, y_train, validation_data=(X_val_rnn, y_val), epochs=100, batch_size=32)

# 12. Оценка моделей и запись результатов в файл
output_file_path = 'model_evaluation_results.txt'

# Создание или очистка файла перед записью
with open(output_file_path, 'w') as output_file:
    output_file.write(f"Оценка моделей - {datetime.now()}\n\n")

# # Функция для оценки и записи результатов
# def evaluate_and_log(model, X_test, y_test, model_name, is_nn=False):
#     if is_nn:
#         y_pred = model.predict(X_test)
#     else:
#         y_pred = model.predict(X_test)
#     rmse = np.sqrt(mean_squared_error(y_test, y_pred))
#     r2 = r2_score(y_test, y_pred)
#     mae = mean_absolute_error(y_test, y_pred)
#     with open(output_file_path, 'a') as output_file:
#         output_file.write(f"Модель: {model_name}\n")
#         output_file.write(f"RMSE: {rmse}\n")
#         output_file.write(f"R²: {r2}\n")
#         output_file.write(f"MAE: {mae}\n\n")
#     print(f"{model_name} - RMSE: {rmse}, R²: {r2}, MAE: {mae}")

def evaluate_and_log(model, X_test, y_test, model_name, is_nn=False):
    if is_nn:
        y_pred = model.predict(X_test)
    else:
        y_pred = model.predict(X_test)
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    with open("model_evaluation_results.txt", "a", encoding="utf-8") as output_file:
        output_file.write(f"Модель: {model_name}\n")
        output_file.write(f"RMSE: {rmse}\n")
        output_file.write(f"R²: {r2}\n")
        output_file.write(f"MAE: {mae}\n\n")
    
    print(f"{model_name} - RMSE: {rmse}, R²: {r2}, MAE: {mae}")

# Оценка Полносвязной Нейронной Сети
evaluate_and_log(model_fc, X_test_processed, y_test, "Полносвязная Нейронная Сеть")

# Оценка GRU Нейронной Сети
evaluate_and_log(model_gru, X_test_gru, y_test, "GRU Нейронная Сеть", is_nn=True)

# Оценка Линейной Регрессии
evaluate_and_log(model_lr, X_test_processed, y_test, "Линейная Регрессия")

# Оценка Простая RNN
evaluate_and_log(model_rnn, X_test_rnn, y_test, "Простая RNN", is_nn=True)

# 13. Подбор гиперпараметров (Grid Search) для полносвязной модели
def create_model(optimizer='adam'):
    model = Sequential()
    model.add(Dense(128, input_dim=X_train_processed.shape[1], activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer=optimizer, loss='mse')
    return model

model = KerasRegressor(build_fn=create_model, verbose=0)
param_grid = {'batch_size': [16, 32], 'epochs': [50, 100], 'optimizer': ['adam', 'rmsprop']}
grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=3)
grid_result = grid.fit(X_train_processed, y_train)

print(f"Лучший результат: {grid_result.best_score_} с параметрами {grid_result.best_params_}")

with open(output_file_path, 'a') as output_file:
    output_file.write(f"Лучший результат Grid Search: {grid_result.best_score_} с параметрами {grid_result.best_params_}\n\n")

# 14. Сохранение лучшей модели (раскомментировать при необходимости)
# joblib.dump(grid_result.best_estimator_, 'best_model.pkl')

# 15. Дополнительная визуализация обучения моделей (например, графики потерь)
# Полносвязная Нейронная Сеть
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history_fc.history['loss'], label='Train Loss')
plt.plot(history_fc.history['val_loss'], label='Val Loss')
plt.title('Полносвязная НС - Потери')
plt.xlabel('Эпоха')
plt.ylabel('Потеря')
plt.legend()

# GRU Нейронная Сеть
plt.subplot(1, 2, 2)
plt.plot(history_gru.history['loss'], label='Train Loss')
plt.plot(history_gru.history['val_loss'], label='Val Loss')
plt.title('GRU НС - Потери')
plt.xlabel('Эпоха')
plt.ylabel('Потеря')
plt.legend()

plt.tight_layout()
plt.show()

# Простая RNN
plt.figure()
plt.plot(history_rnn.history['loss'], label='Train Loss')
plt.plot(history_rnn.history['val_loss'], label='Val Loss')
plt.title('Простая RNN - Потери')
plt.xlabel('Эпоха')
plt.ylabel('Потеря')
plt.legend()
plt.show()

# 16. Заключение: на основе результатов сравниваем модели и выбираем лучшую.
# Это может быть реализовано вручную, основываясь на метриках, записанных в файл.

