# -*- coding: utf-8 -*-
"""Hw5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1s2URrLxpWo6A7eB7L9Heb1ISttddPFHN
"""

import zipfile
import requests
import os
import pandas as pd
import numpy as np
from io import BytesIO
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

url = 'https://drive.google.com/file/d/1nzrtQpfaHL0OgJ_eXzA7VuEj7XotrSWO/view'
file_id = url.split('/')[-2]
dwn_url = 'https://drive.google.com/uc?id=' + file_id

response = requests.get(dwn_url)
zip_file = zipfile.ZipFile(BytesIO(response.content))
zip_file.extractall('/content/extracted_data')

# Функція для розрахунку часових ознак
def calculate_time_domain_features(data):
    features = {}
    features['mean'] = np.mean(data)
    features['std'] = np.std(data)
    features['max'] = np.max(data)
    features['min'] = np.min(data)
    features['amplitude'] = np.max(data) - np.min(data)
    features['energy'] = np.sum(data ** 2)
    return features

# Зчитуємо дані з CSV-файлів та об'єднуємо їх у один DataFrame
data_dict = {}
for folder in ['idle', 'running', 'stairs', 'walking']:
    folder_path = os.path.join('/content/extracted_data/data', folder)
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            try:
                data = pd.read_csv(file_path, encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    data = pd.read_csv(file_path, encoding='windows-1251')
                except UnicodeDecodeError:
                    data = pd.read_csv(file_path, encoding='iso-8859-1')
            data_dict[(folder, file_name)] = data

df_list = []
for (folder, file_name), data in data_dict.items():
    features = calculate_time_domain_features(data.iloc[:, 0])
    features['activity'] = folder
    df_list.append(pd.DataFrame(features, index=[0]))

df = pd.concat(df_list, ignore_index=True)

# Розділяємо дані на тренувальний та тестовий набори
X = df.drop('activity', axis=1)
y = df['activity']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Нормалізуємо дані
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Тренуємо модель SVM
svm_model = SVC(kernel='linear', C=1.0, random_state=42)
svm_model.fit(X_train, y_train)
y_pred_svm = svm_model.predict(X_test)

# Тренуємо модель Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

# Виводимо classification report для обох моделей
print("Classification Report SVM:\n", classification_report(y_test, y_pred_svm))
print("Classification Report Random Forest:\n", classification_report(y_test, y_pred_rf))