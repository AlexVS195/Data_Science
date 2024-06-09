# -*- coding: utf-8 -*-
"""Hw2_1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vynmL7w1_nbRYRgc70QF8HUv9xG0SuAp
"""

# Підключення до бібліотек
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from google.colab import drive

# URL сторінки Вікіпедії
source = 'https://uk.wikipedia.org/wiki/%D0%9D%D0%B0%D1%81%D0%B5%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F_%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B8#%D0%9D%D0%B0%D1%80%D0%BE%D0%B4%D0%B6%D1%83%D0%B2%D0%B0%D0%BD%D1%96%D1%81%D1%82%D1%8C'

# Завантаження таблиці
df = pd.read_html(source, match='Коефіцієнт народжуваності в регіонах України', thousands=".", decimal=",")[0]

# Виведення перших рядків таблиці
print(df.head())

# Кількість рядків та стовпців у датафреймі
print(df.shape)

# Заміна значень "—" на NaN
df = df.replace('—', pd.NA)

# Типи всіх стовпців
print(df.dtypes)

# Заміна типів нечислових колонок на числові
for col in df.columns:
    if df[col].dtype == object and col != 'Регіон':
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Частка пропусків у кожній колонці
print(df.isnull().sum() / len(df))

# Видалення останнього рядка (дані по всій країні)
df = df.drop(df.index[-1])

# Заміна пропусків середніми значеннями стовпців
numeric_columns = df.columns.difference(['Регіон'])
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

# Регіони з вищою народжуваністю в 2019 році
average_2019 = df[df.columns[-1]].mean()
regions_above_average_2019 = df[df.columns[-1]] > average_2019
print("Регіони з вищою народжуваністю у 2019 році:", df[regions_above_average_2019]['Регіон'])

# Регіон з найвищою народжуваністю в 2014 році
max_birth_rate_2014 = df[df[df.columns[-6]] == df[df.columns[-6]].max()]['Регіон']
print(max_birth_rate_2014)

# Стовпчикова діаграма народжуваності по регіонам у 2019 році
plt.figure(figsize=(10, 5))

# Сортуємо дані за зменшенням коефіцієнта народжуваності у останньому стовпці (2019 рік)
sorted_df = df.sort_values(by=df.columns[-1], ascending=False)

# Вибираємо останній стовпець для побудови графіка
last_column = df.columns[-1]

# Будуємо стовпчикову діаграму
sorted_df[last_column].plot(kind='bar', color='skyblue')

# Встановлюємо назви регіонів як мітки на осі X
plt.xticks(range(len(sorted_df)), sorted_df['Регіон'], rotation=90)

plt.title('Народжуваність по регіонах у 2019 році')
plt.ylabel('Коефіцієнт народжуваності')
plt.xlabel('Регіон')
plt.tight_layout()
plt.show()

# Побудова графіка розподілу рівня народжуваності по регіонах за роками
plt.figure(figsize=(12, 8))

# Проходимося по стовпцях, крім першого (назви регіонів)
for i in range(1, len(df.columns)):
    plt.plot(df['Регіон'], df[df.columns[i]], label=df.columns[i])

plt.title('Рівень народжуваності по регіонах за роками')
plt.xlabel('Регіон')
plt.ylabel('Коефіцієнт народжуваності')
plt.xticks(rotation=90)
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()

# Побудова графіка розподілу середньої народжуваності за роками
numeric_columns = df.columns.difference(['Регіон'])

# Обчислення середніх значень для числових стовпців
mean_values = df[numeric_columns].mean()

# Побудова графіка розподілу середньої народжуваності за роками
plt.figure(figsize=(10, 6))
mean_values.plot(kind='bar', color='skyblue')
plt.title('Середня народжуваність за роками')
plt.xlabel('Рік')
plt.ylabel('Середній коефіцієнт народжуваності')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Побудова кругової діаграми для показника "Народження"
plt.figure(figsize=(8, 8))
birth_rate_fraction = df['1950'].value_counts()
birth_rate_fraction.plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title('Розподіл кількості народжень')
plt.axis('equal')
plt.tight_layout()
plt.show()