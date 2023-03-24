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

df

df.columns

df.info() #n

#n -check for any missing values
print(df.isnull().sum())

df.label.value_counts()