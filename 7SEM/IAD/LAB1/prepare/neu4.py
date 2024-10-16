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
from tensorflow.keras.layers import Dense, GRU
from sklearn.linear_model import LinearRegression
import joblib
import os  # Добавлено: для работы с файлами
from datetime import datetime  # Добавлено: для записи времени в файл
import tensorflow as tf
import logging

# Подавление предупреждений TensorFlow (опционально)
tf.get_logger().setLevel(logging.ERROR)

# 2. Загрузка данных
column_names = ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model_year', 'origin', 'car_name']
column_names_filtred = ['mpg','cylinders','weight']
df = pd.read_csv('V10.txt', delim_whitespace=True, names=column_names)

# 3. Разведочный анализ данных (EDA)
print(df.describe())
print(df.info())

df.hist(figsize=(12, 8))
plt.show()

# Создание одномерных графиков плотности для данных в df
df[column_names_filtred].plot(kind='density', subplots=True, layout=(1, 3), sharex=False, legend=True, fontsize=12, figsize=(12, 4))
plt.show()

# Многомерная
sns.pairplot(df)
plt.show()

# 4. Очистка данных
df['horsepower'] = pd.to_numeric(df['horsepower'], errors='coerce')
df['horsepower'] = df['horsepower'].fillna(df['horsepower'].median())
df['hppercil'] = df['horsepower'] / df['cylinders']
df.drop(columns=['car_name'], inplace=True)

# 5. Создание признаков
categorical_features = ['cylinders', 'model_year', 'origin']
continuous_features = ['displacement', 'horsepower', 'weight', 'acceleration']

# Преобразование категориальных и числовых признаков с handle_unknown='ignore'
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), continuous_features),
        ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), categorical_features)
    ])

# 6. Разделение данных на обучающую, тестовую и валидационную выборки
X_all = df.drop(columns=['mpg'])
y_all = df['mpg']
X_train_all, X_temp_all, y_train_all, y_temp_all = train_test_split(X_all, y_all, test_size=0.3, random_state=42)
X_val_all, X_test_all, y_val_all, y_test_all = train_test_split(X_temp_all, y_temp_all, test_size=0.5, random_state=42)

pipeline_all = Pipeline(steps=[('preprocessor', preprocessor)])
X_train_processed_all = pipeline_all.fit_transform(X_train_all)
X_val_processed_all = pipeline_all.transform(X_val_all)
X_test_processed_all = pipeline_all.transform(X_test_all)

# Модель 2: Только нужные признаки
X_selected = df[['mpg', 'cylinders', 'weight']]
y_selected = X_selected['mpg']
X_selected = X_selected.drop(columns=['mpg'])

X_train_selected, X_temp_selected, y_train_selected, y_temp_selected = train_test_split(X_selected, y_selected, test_size=0.3, random_state=42)
X_val_selected, X_test_selected, y_val_selected, y_test_selected = train_test_split(X_temp_selected, y_temp_selected, test_size=0.5, random_state=42)

# Создание пайплайна для обработки данных
pipeline_selected = Pipeline(steps=[
    ('preprocessor', ColumnTransformer(transformers=[
        ('num', StandardScaler(), ['weight']),
        ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), ['cylinders'])
    ]))
])

X_train_processed_selected = pipeline_selected.fit_transform(X_train_selected)
X_val_processed_selected = pipeline_selected.transform(X_val_selected)
X_test_processed_selected = pipeline_selected.transform(X_test_selected)

# 7. Модель 1: Нейронная сеть на основе GRU для всех признаков
X_train_gru_all = X_train_processed_all.reshape((X_train_processed_all.shape[0], 1, X_train_processed_all.shape[1]))
X_val_gru_all = X_val_processed_all.reshape((X_val_processed_all.shape[0], 1, X_val_processed_all.shape[1]))
X_test_gru_all = X_test_processed_all.reshape((X_test_processed_all.shape[0], 1, X_test_processed_all.shape[1]))

model_gru_all = Sequential()
model_gru_all.add(GRU(128, input_shape=(1, X_train_processed_all.shape[1]), return_sequences=True))
model_gru_all.add(GRU(64))
model_gru_all.add(Dense(1))
model_gru_all.compile(optimizer='adam', loss='mse', metrics=['mae'])

history_gru_all = model_gru_all.fit(X_train_gru_all, y_train_all, validation_data=(X_val_gru_all, y_val_all), epochs=100, batch_size=32)

# 8. Модель 2: Линейная Регрессия для всех признаков
model_lr_all = LinearRegression()
model_lr_all.fit(X_train_processed_all, y_train_all)

# 9. Модель 3: Нейронная сеть на основе GRU для выбранных признаков
X_train_gru_selected = X_train_processed_selected.reshape((X_train_processed_selected.shape[0], 1, X_train_processed_selected.shape[1]))
X_val_gru_selected = X_val_processed_selected.reshape((X_val_processed_selected.shape[0], 1, X_val_processed_selected.shape[1]))
X_test_gru_selected = X_test_processed_selected.reshape((X_test_processed_selected.shape[0], 1, X_test_processed_selected.shape[1]))

model_gru_selected = Sequential()
model_gru_selected.add(GRU(128, input_shape=(1, X_train_processed_selected.shape[1]), return_sequences=True))
model_gru_selected.add(GRU(64))
model_gru_selected.add(Dense(1))
model_gru_selected.compile(optimizer='adam', loss='mse', metrics=['mae'])

history_gru_selected = model_gru_selected.fit(X_train_gru_selected, y_train_selected, validation_data=(X_val_gru_selected, y_val_selected), epochs=100, batch_size=32)

# 10. Модель 4: Линейная Регрессия для выбранных признаков
model_lr_selected = LinearRegression()
model_lr_selected.fit(X_train_processed_selected, y_train_selected)

# 11. Оценка моделей и запись результатов в файл
output_file_path = 'model_evaluation_results.txt'

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(f"Оценка моделей - {datetime.now()}\n\n")

def evaluate_and_log(model, X_test, y_test, model_name, is_nn=False):
    if is_nn:
        y_pred = model.predict(X_test)
        y_pred = y_pred.flatten()
    else:
        y_pred = model.predict(X_test)
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    with open(output_file_path, 'a', encoding='utf-8') as output_file:
        output_file.write(f"Модель: {model_name}\n")
        output_file.write(f"RMSE: {rmse}\n")
        output_file.write(f"R²: {r2}\n")
        output_file.write(f"MAE: {mae}\n\n")
    
    print(f"{model_name} - RMSE: {rmse}, R²: {r2}, MAE: {mae}\n")

evaluate_and_log(model_gru_all, X_test_gru_all, y_test_all, "GRU Нейронная Сеть (всё что есть в датасете)", is_nn=True)
evaluate_and_log(model_lr_all, X_test_processed_all, y_test_all, "Линейная Регрессия (всё что есть в датасете)")

evaluate_and_log(model_gru_selected, X_test_gru_selected, y_test_selected, "GRU Нейронная Сеть (Только нужно: mpg, cylinders, weight)", is_nn=True)
evaluate_and_log(model_lr_selected, X_test_processed_selected, y_test_selected, "Линейная Регрессия (Только нужно: mpg, cylinders, weight)")

# 12. Оценка моделей с использованием стандартизации
# Сначала повторим для всех признаков
pipeline_all_with_std = Pipeline(steps=[('preprocessor', preprocessor)])
X_train_processed_all_std = pipeline_all_with_std.fit_transform(X_train_all)
X_val_processed_all_std = pipeline_all_with_std.transform(X_val_all)
X_test_processed_all_std = pipeline_all_with_std.transform(X_test_all)

evaluate_and_log(model_gru_all, X_test_gru_all, y_test_all, "GRU Нейронная Сеть (Все, что есть и стандартизация)", is_nn=True)
evaluate_and_log(model_lr_all, X_test_processed_all_std, y_test_all, "Линейная Регрессия (Все, что есть и стандартизация)")

# Для выбранных признаков
pipeline_selected_with_std = Pipeline(steps=[
    ('preprocessor', ColumnTransformer(transformers=[
        ('num', StandardScaler(), ['weight']),
        ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), ['cylinders'])
    ]))
])

X_train_processed_selected_std = pipeline_selected_with_std.fit_transform(X_train_selected)
X_val_processed_selected_std = pipeline_selected_with_std.transform(X_val_selected)
X_test_processed_selected_std = pipeline_selected_with_std.transform(X_test_selected)

evaluate_and_log(model_gru_selected, X_test_gru_selected, y_test_selected, "GRU Нейронная Сеть (Только нужное и стандартизация)", is_nn=True)
evaluate_and_log(model_lr_selected, X_test_processed_selected_std, y_test_selected, "Линейная Регрессия (Только нужное и стандартизация)")

# 13. Сохранение моделей
joblib.dump(model_lr_all, 'linear_regression_model_all.pkl')
joblib.dump(model_lr_selected, 'linear_regression_model_selected.pkl')
model_gru_all.save('gru_model_all.h5')
model_gru_selected.save('gru_model_selected.h5')

print("Модели успешно сохранены.")
