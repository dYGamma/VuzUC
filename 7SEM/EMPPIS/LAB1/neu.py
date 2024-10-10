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
from tensorflow.keras.layers import Dense, GRU, Dropout
from sklearn.linear_model import LinearRegression
from tensorflow.keras.callbacks import EarlyStopping
import joblib
import os
from datetime import datetime
import tensorflow as tf
import logging

# Подавление предупреждений TensorFlow (опционально)
tf.get_logger().setLevel(logging.ERROR)

# 2. Загрузка данных
column_names = ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model_year', 'origin', 'car_name']
column_names_filtred = ['mpg','cylinders','weight']
df = pd.read_csv('V10.txt', delim_whitespace=True, names=column_names)

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

# 3. Очистка данных
# Преобразование 'horsepower' в числовой тип и заполнение пропущенных значений медианой
df['horsepower'] = pd.to_numeric(df['horsepower'], errors='coerce')
df['horsepower'] = df['horsepower'].fillna(df['horsepower'].median())
df['hppercil'] = df['horsepower'] / df['cylinders']
# Удаление столбца 'car_name', так как он не влияет на предсказание расхода топлива
df.drop(columns=['car_name'], inplace=True)

plt.figure(figsize=(10, 8))
sns.heatmap(df.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm')
plt.show()

# 4. Разделение данных на обучающую и тестовую выборки
X_full = df.drop(columns=['mpg'])
y = df['mpg']

# Разделение на полные и фильтрованные наборы данных
X_filtered = df[['cylinders', 'horsepower', 'weight']]

# 5. Определение категориальных и числовых признаков
categorical_features = []
numerical_features_full = ['cylinders', 'horsepower', 'weight']
numerical_features_filtered = ['cylinders', 'horsepower', 'weight']

# 6. Предобработка данных
preprocessor_full = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features_full)
    ]
)

preprocessor_filtered = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features_filtered)
    ]
)

scaler_full = StandardScaler()
scaler_filtered = StandardScaler()

# 7. Определение моделей GRU и линейной регрессии
# Функция для создания модели GRU
def create_gru_model(input_shape):
    model = Sequential()
    model.add(GRU(128, input_shape=input_shape, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(GRU(64))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='relu'))
    model.compile(optimizer='RMSprop', loss='mse')
    return model

# Добавление ранней остановки
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# 8. Создание и обучение моделей
# Разделение данных на обучающую и тестовую выборки
X_train_full, X_test_full, y_train_full, y_test_full = train_test_split(X_full, y, test_size=0.2, random_state=42)
X_train_filtered, X_test_filtered, y_train_filtered, y_test_filtered = train_test_split(X_filtered, y, test_size=0.2, random_state=42)

# Стандартизация данных и создание наборов данных для GRU
X_train_full_prepared = preprocessor_full.fit_transform(X_train_full)
X_test_full_prepared = preprocessor_full.transform(X_test_full)

X_train_filtered_prepared = preprocessor_filtered.fit_transform(X_train_filtered)
X_test_filtered_prepared = preprocessor_filtered.transform(X_test_filtered)

# Стандартизация полных данных
X_train_full_standardized = scaler_full.fit_transform(X_train_full)
X_test_full_standardized = scaler_full.transform(X_test_full)

# Стандартизация фильтрованных данных
X_train_filtered_standardized = scaler_filtered.fit_transform(X_train_filtered[numerical_features_filtered])
X_test_filtered_standardized = scaler_filtered.transform(X_test_filtered[numerical_features_filtered])

# GRU Model 1: Полная модель
gru_model_full = create_gru_model((X_train_full_prepared.shape[1], 1))
gru_model_full.fit(np.expand_dims(X_train_full_prepared, axis=-1), y_train_full, epochs=240, batch_size=32,  callbacks=[early_stopping])

# GRU Model 2: Фильтрованная модель
gru_model_filtered = create_gru_model((X_train_filtered_prepared.shape[1], 1))
gru_model_filtered.fit(np.expand_dims(X_train_filtered_prepared, axis=-1), y_train_filtered, epochs=240, batch_size=32,  callbacks=[early_stopping])

# GRU Model 3: Полная модель с стандартизированными данными
gru_model_full_standardized = create_gru_model((X_train_full_standardized.shape[1], 1))
gru_model_full_standardized.fit(np.expand_dims(X_train_full_standardized, axis=-1), y_train_full, epochs=240, batch_size=32,  callbacks=[early_stopping])

# GRU Model 4: Фильтрованная модель с стандартизированными данными
gru_model_filtered_standardized = create_gru_model((X_train_filtered_standardized.shape[1], 1))
gru_model_filtered_standardized.fit(np.expand_dims(X_train_filtered_standardized, axis=-1), y_train_filtered, epochs=240, batch_size=32,  callbacks=[early_stopping])

# Линейная регрессия
lin_reg_full = LinearRegression()
lin_reg_filtered = LinearRegression()
lin_reg_full_standardized = LinearRegression()
lin_reg_filtered_standardized = LinearRegression()

# Обучение линейной регрессии на полных данных
lin_reg_full.fit(X_train_full_prepared, y_train_full)

# Обучение линейной регрессии на фильтрованных данных
lin_reg_filtered.fit(X_train_filtered_prepared, y_train_filtered)

# Обучение линейной регрессии на стандартизированных полных данных
lin_reg_full_standardized.fit(X_train_full_standardized, y_train_full)

# Обучение линейной регрессии на стандартизированных фильтрованных данных
lin_reg_filtered_standardized.fit(X_train_filtered_standardized, y_train_filtered)

# 9. Оценка моделей
# Оценка GRU моделей
y_pred_gru_full = gru_model_full.predict(np.expand_dims(X_test_full_prepared, axis=-1))
y_pred_gru_filtered = gru_model_filtered.predict(np.expand_dims(X_test_filtered_prepared, axis=-1))
y_pred_gru_full_standardized = gru_model_full_standardized.predict(np.expand_dims(X_test_full_standardized, axis=-1))
y_pred_gru_filtered_standardized = gru_model_filtered_standardized.predict(np.expand_dims(X_test_filtered_standardized, axis=-1))

print("\n======================== Оценка моделей GRU ========================\n")
print(f"GRU Model 1 (Полная):\n  - MSE: {mean_squared_error(y_test_full, y_pred_gru_full):.2f}\n  - R2 Score: {r2_score(y_test_full, y_pred_gru_full):.2f}\n")
print(f"GRU Model 2 (Фильтрованная):\n  - MSE: {mean_squared_error(y_test_filtered, y_pred_gru_filtered):.2f}\n  - R2 Score: {r2_score(y_test_filtered, y_pred_gru_filtered):.2f}\n")
print(f"GRU Model 3 (Полная с стандартизацией):\n  - MSE: {mean_squared_error(y_test_full, y_pred_gru_full_standardized):.2f}\n  - R2 Score: {r2_score(y_test_full, y_pred_gru_full_standardized):.2f}\n")
print(f"GRU Model 4 (Фильтрованная с стандартизацией):\n  - MSE: {mean_squared_error(y_test_filtered, y_pred_gru_filtered_standardized):.2f}\n  - R2 Score: {r2_score(y_test_filtered, y_pred_gru_filtered_standardized):.2f}\n")

# Оценка линейной регрессии
y_pred_lin_full = lin_reg_full.predict(X_test_full_prepared)
y_pred_lin_filtered = lin_reg_filtered.predict(X_test_filtered_prepared)
y_pred_lin_full_standardized = lin_reg_full_standardized.predict(X_test_full_standardized)
y_pred_lin_filtered_standardized = lin_reg_filtered_standardized.predict(X_test_filtered_standardized)

print("\n==================== Оценка моделей Линейной Регрессии ====================\n")
print(f"Linear Regression Model 1 (Полная):\n  - MSE: {mean_squared_error(y_test_full, y_pred_lin_full):.2f}\n  - R2 Score: {r2_score(y_test_full, y_pred_lin_full):.2f}\n")
print(f"Linear Regression Model 2 (Фильтрованная):\n  - MSE: {mean_squared_error(y_test_filtered, y_pred_lin_filtered):.2f}\n  - R2 Score: {r2_score(y_test_filtered, y_pred_lin_filtered):.2f}\n")
print(f"Linear Regression Model 3 (Полная с стандартизацией):\n  - MSE: {mean_squared_error(y_test_full, y_pred_lin_full_standardized):.2f}\n  - R2 Score: {r2_score(y_test_full, y_pred_lin_full_standardized):.2f}\n")
print(f"Linear Regression Model 4 (Фильтрованная с стандартизацией):\n  - MSE: {mean_squared_error(y_test_filtered, y_pred_lin_filtered_standardized):.2f}\n  - R2 Score: {r2_score(y_test_filtered, y_pred_lin_filtered_standardized):.2f}\n")