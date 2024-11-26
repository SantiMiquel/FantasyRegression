import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from lightgbm import LGBMRegressor
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

# Cargar el dataset
df = pd.read_csv('estadisticas_fantasy.csv')

# Preprocesamiento
df.rename(columns={'Unnamed: 0': 'ID_jugador'}, inplace=True)
df['Precio Actual'] = df['Precio Actual'].str.replace('.', '').astype(int)
df['Precio Inicial'] = df['Precio Inicial'].str.replace('.', '').astype(int)

# Eliminamos variables no relevantes
df = df[df['Posición'] != 'DT']
df.drop(columns=['Nombre', 'ID_jugador', 'Precio Inicial'], inplace=True)

# Encoding de variables categóricas
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['Posición'] = le.fit_transform(df['Posición'])
df['Equipo'] = le.fit_transform(df['Equipo'])

# Feature engineering
df['Gols_per_Minuts'] = df['Goles'] / (df['Minutos'] + 1e-9)
df['Assistencies_per_Partit'] = df['Asistencias'] / (df['Partidos'] + 1e-9)
df['Gols_Assistencies'] = df['Goles'] + df['Asistencias']
df['Mitjana_Gols_Equip'] = df.groupby('Equipo')['Goles'].transform('mean')
df['Minuts_quadrat'] = df['Minutos'] ** 2
df['Log_Gols'] = np.log1p(df['Goles'])

# Separación de variables predictoras y target
target_att = 'Precio Actual'
attributes = [col for col in df.columns if col != target_att]
X = df[attributes]
y = df[target_att]

# Escalado de datos
scaler = StandardScaler()
X = scaler.fit_transform(X)
y = scaler.fit_transform(y.values.reshape(-1, 1))

# División en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Modelos a comparar
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(),
    "LightGBM": LGBMRegressor(),
    "XGBoost": XGBRegressor(),
    "AdaBoost": AdaBoostRegressor()
}

# Entrenamiento y evaluación
results = {}
for name, model in models.items():
    model.fit(X_train, y_train.ravel())  # y_train.ravel() para evitar el warning
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    r2_train = r2_score(y_train, y_pred_train)
    r2_test = r2_score(y_test, y_pred_test)
    mae_train = mean_absolute_error(y_train, y_pred_train)
    mae_test = mean_absolute_error(y_test, y_pred_test)
    results[name] = {"MAE Train": mae_train, "MAE Test": mae_test, 'R2 Train': r2_train, 'R2 Test': r2_test}

# Mostrar los resultados
results_df = pd.DataFrame(results).T
print(results_df)

# Selección de características con Random Forest
rf = RandomForestRegressor()
rf.fit(X_train, y_train.ravel())
importances = rf.feature_importances_

# Crear un DataFrame con las importancias
importances_df = pd.DataFrame({
    'Feature': attributes,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

print(importances_df)

# Seleccionar características importantes (por ejemplo, importancia > 0.05)
selected_features = importances_df[importances_df['Importance'] > 0.05]['Feature'].tolist()
X_train_selected = X_train[:, [attributes.index(f) for f in selected_features]]
X_test_selected = X_test[:, [attributes.index(f) for f in selected_features]]

# Reentrenar con características seleccionadas
rf_filtered = RandomForestRegressor()
rf_filtered.fit(X_train_selected, y_train.ravel())
y_pred_train_selected = rf_filtered.predict(X_train_selected)
y_pred_selected = rf_filtered.predict(X_test_selected)

# Calcular MAE
mae_train_selected = mean_absolute_error(y_train, y_pred_train_selected)
mae_selected = mean_absolute_error(y_test, y_pred_selected)
print(f"MAE después de la selección de características test: {mae_selected} train: {mae_train_selected}")

# Visualización de los resultados
fig, ax = plt.subplots(figsize=(10, 6))
model_names = list(results.keys())
mae_train_values = [results[name]["MAE Train"] for name in model_names]
mae_test_values = [results[name]["MAE Test"] for name in model_names]
r2_train_values = [results[name]['R2 Train'] for name in model_names]
r2_test_values = [results[name]['R2 Test'] for name in model_names]

bar_width = 0.35
index = np.arange(len(model_names))

bar1 = ax.bar(index, mae_train_values, bar_width, label='MAE Train', color='skyblue')
bar2 = ax.bar(index + bar_width, mae_test_values, bar_width, label='MAE Test', color='orange')

ax.set_xlabel('Modelos')
ax.set_ylabel('MAE')
ax.set_title('Comparación de MAE entre modelos')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(model_names, rotation=45)
ax.legend()
plt.axhline(y=0, color='red', linestyle='--', linewidth=1)
plt.show()
print(f'R2 Train: {r2_train_values}')
print(f'R2 test {r2_test_values}')