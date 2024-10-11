# 1. Импорт необходимых библиотек
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PolynomialFeatures
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
from pickle import dump, load

# Подавление предупреждений TensorFlow (опционально)
tf.get_logger().setLevel(logging.ERROR)

# 2. Загрузка данных
column_names = ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model_year', 'origin', 'car_name']
#column_names_filtred = ['mpg','cylinders','weight']
df = pd.read_csv('V10.txt', delim_whitespace=True, names=column_names)

# b. Визуализация
# Одномерная
df.hist(figsize=(12, 8))
plt.show()

# Создание одномерных графиков плотности для данных в df
#df[column_names_filtred].plot(kind='density', subplots=True, layout=(1, 3), sharex=False, legend=True, fontsize=12, figsize=(12, 4))
#plt.show()

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
plt.figure(figsize=(10, 8))
sns.heatmap(df[['mpg', 'cylinders', 'weight', 'displacement']].corr(), annot=True, cmap='coolwarm')
plt.title('Тепловая карта корреляции для выбранных признаков')
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
    
    model.add(GRU(64))
    
    model.add(Dense(1, activation='relu'))
    model.compile(optimizer='adam', loss='mse')
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

# Grid Search для полиномиальной регрессии
print("\n==================== Grid Search для Полиномиальной Регрессии ====================\n")
Deg = [2]
results_rmse = []
results_r2 = []
names = []

deg = 2
polynomial_features = PolynomialFeatures(degree=deg)
housing_X_poly = polynomial_features.fit_transform(X_train_filtered)
model = LinearRegression()
model.fit(housing_X_poly, y_train_filtered)
housing_Y_poly_pred = model.predict(polynomial_features.transform(X_test_filtered))
rmse = np.sqrt(mean_squared_error(y_test_filtered, housing_Y_poly_pred))
r2 = r2_score(y_test_filtered, housing_Y_poly_pred)
print(f"Poly degree = {deg}")
print(f"RMSE for Polynomial Regression: {rmse}")
print(f"R2 Score for Polynomial Regression: {r2}\n")

# 9. Оценка моделей
# Оценка GRU моделей
y_pred_gru_full = gru_model_full.predict(np.expand_dims(X_test_full_prepared, axis=-1))
y_pred_gru_filtered = gru_model_filtered.predict(np.expand_dims(X_test_filtered_prepared, axis=-1))
y_pred_gru_full_standardized = gru_model_full_standardized.predict(np.expand_dims(X_test_full_standardized, axis=-1))
y_pred_gru_filtered_standardized = gru_model_filtered_standardized.predict(np.expand_dims(X_test_filtered_standardized, axis=-1))


evaluation_results = []

evaluation_results.append("\n======================== Оценка моделей GRU ========================\n")
evaluation_results.append(f"GRU Model 1 (Полная):\n  - MSE: {mean_squared_error(y_test_full, y_pred_gru_full):.2f}\n  - R2 Score: {r2_score(y_test_full, y_pred_gru_full):.2f}\n")
evaluation_results.append(f"GRU Model 2 (Фильтрованная):\n  - MSE: {mean_squared_error(y_test_filtered, y_pred_gru_filtered):.2f}\n  - R2 Score: {r2_score(y_test_filtered, y_pred_gru_filtered):.2f}\n")
evaluation_results.append(f"GRU Model 3 (Полная с стандартизацией):\n  - MSE: {mean_squared_error(y_test_full, y_pred_gru_full_standardized):.2f}\n  - R2 Score: {r2_score(y_test_full, y_pred_gru_full_standardized):.2f}\n")
evaluation_results.append(f"GRU Model 4 (Фильтрованная с стандартизацией):\n  - MSE: {mean_squared_error(y_test_filtered, y_pred_gru_filtered_standardized):.2f}\n  - R2 Score: {r2_score(y_test_filtered, y_pred_gru_filtered_standardized):.2f}\n")

# Оценка линейной регрессии
y_pred_lin_full = lin_reg_full.predict(X_test_full_prepared)
y_pred_lin_filtered = lin_reg_filtered.predict(X_test_filtered_prepared)
y_pred_lin_full_standardized = lin_reg_full_standardized.predict(X_test_full_standardized)
y_pred_lin_filtered_standardized = lin_reg_filtered_standardized.predict(X_test_filtered_standardized)

evaluation_results.append("\n==================== Оценка моделей Линейной Регрессии ====================\n")
evaluation_results.append(f"Linear Regression Model 1 (Полная):\n  - MSE: {mean_squared_error(y_test_full, y_pred_lin_full):.2f}\n  - R2 Score: {r2_score(y_test_full, y_pred_lin_full):.2f}\n")
evaluation_results.append(f"Linear Regression Model 2 (Фильтрованная):\n  - MSE: {mean_squared_error(y_test_filtered, y_pred_lin_filtered):.2f}\n  - R2 Score: {r2_score(y_test_filtered, y_pred_lin_filtered):.2f}\n")
evaluation_results.append(f"Linear Regression Model 3 (Полная с стандартизацией):\n  - MSE: {mean_squared_error(y_test_full, y_pred_lin_full_standardized):.2f}\n  - R2 Score: {r2_score(y_test_full, y_pred_lin_full_standardized):.2f}\n")
evaluation_results.append(f"Linear Regression Model 4 (Фильтрованная с стандартизацией):\n  - MSE: {mean_squared_error(y_test_filtered, y_pred_lin_filtered_standardized):.2f}\n  - R2 Score: {r2_score(y_test_filtered, y_pred_lin_filtered_standardized):.2f}\n")


# 9.5. Сохранение оценок в текстовый файл
# Создание директории для сохранений, если она не существует
# Вывод оценок в консоль
print(''.join(evaluation_results))

results_dir = "model_results"
os.makedirs(results_dir, exist_ok=True)

# Формирование имени файла с текущей датой и временем
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_file = os.path.join(results_dir, f"evaluation_{timestamp}.txt")

# Запись оценок в файл
with open(results_file, 'w', encoding='utf-8') as f:
    f.write(''.join(evaluation_results))

print(f"Оценки моделей сохранены в файл: {results_file}")




# 10. Сохранение и загрузка модели с использованием pickle
# Сохранение модели линейной регрессии в файл
filename = 'finalized_model.sav'
dump(model, open(filename, 'wb'))

# Загрузка модели из файла
#loaded_model = load(open(filename, 'rb'))

# Пример использования загруженной модели для предсказания
#y_pred_loaded = loaded_model.predict(polynomial_features.transform(X_test_filtered))
#print(f"\n==================== Оценка загруженной модели Полиномиальной Регрессии ====================\n")
#print(f"Loaded Model (Полиномиальная Регрессия, Степень {deg}):\n  - MSE: {mean_squared_error(y_test_filtered, y_pred_loaded):.2f}\n  - R2 Score: #{r2_score(y_test_filtered, y_pred_loaded):.2f}\n")


#11. Сохранение моделей
# Создание директории для моделей, если она не существует
models_dir = "saved_models"
os.makedirs(models_dir, exist_ok=True)

# Сохранение моделей GRU
gru_full_path = os.path.join(models_dir, f"gru_model_full_{timestamp}.h5")
gru_model_full.save(gru_full_path)
print(f"GRU Model Full сохранена в: {gru_full_path}")

gru_filtered_path = os.path.join(models_dir, f"gru_model_filtered_{timestamp}.h5")
gru_model_filtered.save(gru_filtered_path)
print(f"GRU Model Filtered сохранена в: {gru_filtered_path}")

gru_full_std_path = os.path.join(models_dir, f"gru_model_full_standardized_{timestamp}.h5")
gru_model_full_standardized.save(gru_full_std_path)
print(f"GRU Model Full Standardized сохранена в: {gru_full_std_path}")

gru_filtered_std_path = os.path.join(models_dir, f"gru_model_filtered_standardized_{timestamp}.h5")
gru_model_filtered_standardized.save(gru_filtered_std_path)
print(f"GRU Model Filtered Standardized сохранена в: {gru_filtered_std_path}")

# Сохранение моделей линейной регрессии с помощью joblib
lin_reg_full_path = os.path.join(models_dir, f"lin_reg_full_{timestamp}.joblib")
joblib.dump(lin_reg_full, lin_reg_full_path)
print(f"Linear Regression Model Full сохранена в: {lin_reg_full_path}")

lin_reg_filtered_path = os.path.join(models_dir, f"lin_reg_filtered_{timestamp}.joblib")
joblib.dump(lin_reg_filtered, lin_reg_filtered_path)
print(f"Linear Regression Model Filtered сохранена в: {lin_reg_filtered_path}")

lin_reg_full_std_path = os.path.join(models_dir, f"lin_reg_full_standardized_{timestamp}.joblib")
joblib.dump(lin_reg_full_standardized, lin_reg_full_std_path)
print(f"Linear Regression Model Full Standardized сохранена в: {lin_reg_full_std_path}")

lin_reg_filtered_std_path = os.path.join(models_dir, f"lin_reg_filtered_standardized_{timestamp}.joblib")
joblib.dump(lin_reg_filtered_standardized, lin_reg_filtered_std_path)
print(f"Linear Regression Model Filtered Standardized сохранена в: {lin_reg_filtered_std_path}")

