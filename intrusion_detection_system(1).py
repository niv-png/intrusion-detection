# -*- coding: utf-8 -*-
"""intrusion detection system
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1kyt50JZi3xZa8yRFvHBtmNPxHqaBSsHn
"""

#n -import important packages (this might change as we move forward with the project)

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import time

#N - updated: libraries for Evaluate and measure the accuracy of the model
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score, confusion_matrix

#n -libraries for the files in google drive
from pydrive.auth import GoogleAuth
from google.colab import drive
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

from google.colab import drive
drive.mount('/content/drive')

#load dataset
df = pd.read_csv('/content/drive/MyDrive/kddcup99_csv.csv')
df.columns
df.info() #n

#n -check for any missing values
print(df.isnull().sum())
duplicates = df.duplicated()
print('Number of duplicate entries:', duplicates.sum())

#Remove duplicate rows
df = df.drop_duplicates()
print('Number of duplicate entries after removing:', df.duplicated().sum())
df.label.value_counts()

#AlAnoud AlJebreen -Convert categorical data into numerical data
df = pd.get_dummies(df, columns=['protocol_type', 'service', 'flag', 'label'])

#NS - Normalization of dataset
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df_normalized = scaler.fit_transform(df.drop('label_normal', axis=1))
df_normalized = pd.DataFrame(df_normalized, columns=df.drop('label_normal', axis=1).columns)
df_normalized = pd.concat([df_normalized, df['label_normal']], axis=1)

df.to_csv('newkddcup99.csv', index=False)

#NS
corr = df.corr()
  
plt.figure(figsize =(15, 12))
  
sns.heatmap(corr)
  
plt.show()

#UPDATE: kept the unimportant columns to introduce a little noise

#df.drop('lnum_access_files', axis = 1, inplace = True)
df.drop('is_guest_login', axis = 1, inplace = True)
#NS - This variable is highly correlated with rerror_rate and should be ignored for analysis.
df.drop('srv_rerror_rate', axis = 1, inplace = True)
#NS - This variable is highly correlated with srv_serror_rate and should be ignored for analysis.
df.drop('dst_host_srv_serror_rate', axis = 1, inplace = True)
#NS - This variable is highly correlated with rerror_rate and should be ignored for analysis.
df.drop('dst_host_serror_rate', axis = 1, inplace = True)
#NS - This variable is highly correlated with srv_rerror_rate and should be ignored for analysis.
df.drop('dst_host_rerror_rate', axis = 1, inplace = True)
#NS - This variable is highly correlated with rerror_rate and should be ignored for analysis.
df.drop('dst_host_srv_rerror_rate', axis = 1, inplace = True)
#NS - This variable is highly correlated with srv_rerror_rate and should be ignored for analysis.
df.drop('dst_host_same_srv_rate', axis = 1, inplace = True)
#df 


#AlAnoud AlJebreen -Feature Selection PCA
from sklearn.decomposition import PCA
x = df.drop('label_normal', axis=1)
y = df['label_normal']
pca = PCA(n_components=3)
x_pca = pca.fit_transform(x)

#AlAnoud AlJebreen -Feature Selection RFE 
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
x = df.drop('label_normal', axis=1)
y = df['label_normal']
model = LinearRegression()
rfe = RFE(model, n_features_to_select=3)
rfe.fit(x,y) 

#SK - Split the dataset into training and testing sets (30% for test data and 70% for train data >> We can change it)
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.4, random_state=42)
#print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)

#SK - Save the training and testing datasets into separate CSV files
X_train.to_csv('train_data.csv', index=False)
X_test.to_csv('test_data.csv', index=False)
Y_train.to_csv('train_labels.csv', index=False)
Y_test.to_csv('test_labels.csv', index=False)

#NS - Create a decision tree classifier
dtc = DecisionTreeClassifier()

#SK - Train the model using the training data
start = time.time()
dtc.fit(X_train, Y_train)
print("Processing time for Training using Decision Tree Classifier: %s seconds " % (time.time() - start))

#SK - Make predictions on the test data
start = time.time()
Y_pred = dtc.predict(X_test)
print("Processing time for Testing using Decision Tree Classifier: %s seconds " % (time.time() - start)) 

#NS - Updated - Calculate the accuracy, f1-score,recall, precision and confusion matrix
accuracy = accuracy_score(Y_test, Y_pred)
recall= recall_score(Y_test, Y_pred )
precision= precision_score(Y_test, Y_pred )
f1score = f1_score(Y_test, Y_pred)
conf_matrix = confusion_matrix(Y_test, Y_pred)

#NS - Print the results
print("Decision Tree Classifier:")
print("The accuracy of the model is : {:.4f}%".format(accuracy*100))
print("Recall = {:.4f} " .format(recall*100))
print("Precison = {:.4f} ".format(precision*100))
print("F1-score: ", f1score)
print("Confusion Matrix:\n", conf_matrix)

#NS - Second Model: Random Forest
from sklearn.ensemble import RandomForestClassifier

#NS - Create a random forest classifier with 100 trees
rfc = RandomForestClassifier(n_estimators=100)

#NS - Train the model using the training data
start = time.time()
rfc.fit(X_train, Y_train)
print("Processing time for Training using Random Forest Classifier: %s seconds " % (time.time() - start))

#NS - Make predictions on the test data
start = time.time()
Y_pred = rfc.predict(X_test)
print("Processing time for Testing using Random Forest Classifier: %s seconds " % (time.time() - start))

#NS - Calculate the accuracy, f1-score,recall and precision
accuracy = accuracy_score(Y_test, Y_pred)
recall= recall_score(Y_test, Y_pred )
precision= precision_score(Y_test, Y_pred )
f1score = f1_score(Y_test, Y_pred)
conf_matrix = confusion_matrix(Y_test, Y_pred)

#NS - Print the results
print("Random Forest Classifier:")
print("The accuracy of the model is : {:.4f}%".format(accuracy*100))
print("Recall = {:.4f} " .format(recall*100))
print("Precison = {:.4f} ".format(precision*100))
print("F1-score: ", f1score)
print("Confusion Matrix:\n", conf_matrix)

#NS Third Model - Gaussian Naive Bayes
from sklearn.naive_bayes import GaussianNB

gbc = GaussianNB()

#NS - Train the model using the training data
start = time.time()
gbc.fit(X_train, Y_train)
print("Processing time for Training using Gaussian Naive Bayes Classifier: %s seconds " % (time.time() - start))

#NS - Make predictions on the test data
start = time.time()
Y_pred_gbc = gbc.predict(X_test)
print("Processing time for Testing using Gaussian Naive Bayes Classifier: %s seconds " % (time.time() - start))

#NS - Calculate the accuracy, f1-score,recall and precision
accuracy = accuracy_score(Y_test, Y_pred_gbc)
recall= recall_score(Y_test, Y_pred_gbc )
precision= precision_score(Y_test, Y_pred_gbc )
f1score = f1_score(Y_test, Y_pred_gbc)
conf_matrix = confusion_matrix(Y_test, Y_pred_gbc)

#NS - Print the results
print("Gaussian Naive Bayes Classifier:")
print("The accuracy of the model is : {:.4f}%".format(accuracy*100))
print("Recall = {:.4f} " .format(recall*100))
print("Precison = {:.4f} ".format(precision*100))
print("F1-score: ", f1score)
print("Confusion Matrix:\n", conf_matrix)

#NS Fourth Model - Gaussian Naive Bayes
from xgboost import XGBClassifier

xgb = XGBClassifier()

#NS - Train the model using the training data
start = time.time()
xgb.fit(X_train, Y_train)
print("Processing time for Training using Random Forest Classifier: %s seconds " % (time.time() - start))

#NS - Make predictions on the test data
start = time.time()
Y_pred_xgb = xgb.predict(X_test)
print("Processing time for Testing using Random Forest Classifier: %s seconds " % (time.time() - start))

#NS - Calculate the accuracy, f1-score,recall and precision
accuracy = accuracy_score(Y_test, Y_pred_xgb)
recall= recall_score(Y_test, Y_pred_xgb )
precision= precision_score(Y_test, Y_pred_xgb )
f1score = f1_score(Y_test, Y_pred_xgb)
conf_matrix = confusion_matrix(Y_test, Y_pred_xgb)

#NS - Print the results
print("XG Boost Classifier:")
print("The accuracy of the model is : {:.4f}%".format(accuracy*100))
print("Recall = {:.4f} " .format(recall*100))
print("Precison = {:.4f} ".format(precision*100))
print("F1-score: ", f1score)
print("Confusion Matrix:\n", conf_matrix)
