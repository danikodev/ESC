from ast import increment_lineno
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title('Таблица )')
df = pd.read_csv('titanic.csv')
 
plt.figure(figsize=(6, 4))
sns.countplot(x='Sex', data=df)
plt.title('Распределение пассажиров по полу')
plt.xlabel('Пол')
plt.ylabel('Количество пассажиров')
plt.show()
st.pyplot(plt)