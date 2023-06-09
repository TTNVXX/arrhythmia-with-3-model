# -*- coding: utf-8 -*-
"""ARRYTHMIA-3MODEL

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hWVbB4lWwOaZhhQNK3320T3xvzJngqAF
"""

# import library
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

# upload data yang dibutuhkan
url =  "data_arrhythmia.csv"
df = pd.read_csv(url, delimiter=';')
df.shape

df

df.describe()

"""# DATA PREPROCESSING

mengolah data dengan mengubah value2 yg dapat merusak data, lalu melakukan imputasi untuk mengisi value data yang kosong dengan mean/rata2 data dari setiap kolom
"""

# mengubah value ? dengan np.NaN value
df = df.replace('?', np.NaN)

#  membuat data copy baru untuk menghindari perubahan pada data original
new_df = df.copy()

"""Dengan menggunakan missing_values=np.nan pada objek SimpleImputer, kita menunjukkan bahwa nilai yang hilang yang akan diimputasi adalah nilai NaN (Not a Number).

Dengan menggunakan strategy='mean' pada objek SimpleImputer, kita menentukan bahwa strategi yang digunakan untuk mengisi nilai yang hilang adalah dengan menggantinya dengan nilai rata-rata (mean) dari setiap kolom.
"""

# Imputation
my_imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
new_df = pd.DataFrame(my_imputer.fit_transform(new_df))
new_df.columns = df.columns

# imputed dataframe
new_df.head()

"""disini setelah data kita bersih dan value yg salah seperti ? dan value yang kosong sudah terisi dengan nilai mean, maka disini kita akan lanjut ketahap dimana kolom diagnosis akan kita gunakan sebagai target lalu dataframe baru akan dimasukkan ke variabel baru yaitu final_df"""

target=new_df["diagnosis"]
final_df = new_df.drop(columns ="diagnosis")

final_df

"""**MODEL**

disini kita akan menggunakan 80% dari data sebagai training, dan 20% dari data akan digunakan untuk test
"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(final_df, target, test_size=0.2, random_state=1)

# disini kita akan menggunakan standardscaler untuk melakukan skalarisasi dan menggunakan metode fit untuk menghitung variansi dan mean dari data train
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()

ss.fit(X_train)
X_train = ss.transform(X_train)
X_test = ss.transform(X_test)

import warnings
warnings.filterwarnings('ignore')



"""**CLASSIFICATION**"""

# import evaluation metrices.
from sklearn.metrics import r2_score,mean_squared_error,accuracy_score,recall_score,precision_score,confusion_matrix

# variabel result akan menyimpan semua hasil dari tiap model
result = pd.DataFrame(columns=['Model','Train Accuracy','Test Accuracy'])

"""**KNN CLASSIFIER**"""

from sklearn.neighbors import KNeighborsClassifier
knnclassifier = KNeighborsClassifier()
knnclassifier.fit(X_train, y_train)
y_pred = knnclassifier.predict(X_test)

knn_train_accuracy = accuracy_score(y_train, knnclassifier.predict(X_train))
knn_test_accuracy = accuracy_score(y_test, knnclassifier.predict(X_test))

result = result.append(pd.Series({'Model':'KNN Classifier','Train Accuracy':knn_train_accuracy,'Test Accuracy':knn_test_accuracy}),ignore_index=True)
result

"""**DECISSION TREE CLASSIFIER**"""

from sklearn.tree import DecisionTreeClassifier 
dtclassifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0,max_depth=5)
dtclassifier.fit(X_train, y_train) 
y_pred_test = dtclassifier.predict(X_test)
y_pred_train = dtclassifier.predict(X_train)

dt_train_accuracy = accuracy_score(y_train,y_pred_train )
dt_test_accuracy = accuracy_score(y_test, y_pred_test)
result = result.append(pd.Series({'Model':'Decision Tree Classifier','Train Accuracy':dt_train_accuracy,'Test Accuracy':dt_test_accuracy}),ignore_index=True )
result

"""**NAIVE BAYES CLASSIFIER**"""

from sklearn.naive_bayes import GaussianNB
nbclassifier = GaussianNB() 
nbclassifier.fit(X_train, y_train)
y_pred = dtclassifier.predict(X_test)

nb_train_accuracy = accuracy_score(y_train, nbclassifier.predict(X_train))
nb_test_accuracy = accuracy_score(y_test, nbclassifier.predict(X_test))

result = result.append(pd.Series({'Model':'Naive Bayes Classifier','Train Accuracy':nb_train_accuracy,'Test Accuracy':nb_test_accuracy}),ignore_index=True)
result

"""Dengan hasil dari data akurasi diatas, kami menyimpulkan bahwa untuk data ini decision tree classifier merupakan pilihan terbaik

"""