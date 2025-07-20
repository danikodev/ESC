import pandas as pd
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('titanic.csv')  # или просто 'titanic.csv', если файл в текущей директории

df['Age'] = df['Age'].round().astype('Int64')  # 'Int64' поддерживает NaN (в отличие от 'int')



# Загрузка данных
df = pd.read_csv('titanic.csv')  # или полный путь к файлу

# Выбор только числовых столбцов для корреляции
numeric_df = df.select_dtypes(include=['int64', 'float64'])

# Расчет корреляционной матрицы
corr_matrix = numeric_df.corr()

# Визуализация heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(
    corr_matrix,
    annot=True,  # показывать значения в ячейках
    fmt=".2f",   # округление до 2 знаков после запятой
    cmap='coolwarm',  # цветовая схема
    center=0,    # центр цветовой шкалы (0 для корреляции)
    linewidths=0.5,
    linecolor='gray'
)

plt.title('Матрица корреляции числовых признаков')
plt.xticks(rotation=45)  # поворот подписей столбцов
plt.tight_layout()
plt.show()

st.pyplot(plt)
