import pandas as pd
import numpy as np

# Leer el archivo CSV
df = pd.read_csv('datos_sinteticos.csv')

# Información general del dataset
print("=== INFORMACIÓN DEL DATASET ===")
print(f"Dimensiones: {df.shape}")
print(f"\nTipos de datos:\n{df.dtypes}")

# Estadísticas descriptivas
print("\n=== ESTADÍSTICAS DESCRIPTIVAS ===")
print(df.describe())

# Información de valores faltantes
print("\n=== VALORES FALTANTES ===")
print(df.isnull().sum())

# Primeras filas
print("\n=== PRIMERAS FILAS ===")
print(df.head(10))

# Información de columnas
print("\n=== COLUMNAS ===")
print(df.columns.tolist())

# Correlación entre variables numéricas
print("\n=== CORRELACIÓN ===")
print(df.corr(numeric_only=True))