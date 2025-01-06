# Library
import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from datetime import datetime

# Judul
st.title('OPTIMASI PERENCANAAN PRODUKSI DAN DISTRIBUSI GLOBAL')

#Imputasi
def preprocessing(df):
    preprocessor = ColumnTransformer([
        ('imputasi', SimpleImputer(strategy='costant', fill_value=0), ['kolom'])],
        remainder='passthrough',
        verbose_feature_names_out=False
    )
    preprocessor.fit(df)
    df = preprocessor.transform(df)
    df = pd.DataFrame(df, columns=preprocessor.get_feature_names_out())
    return df

#Converter
def convert_df(df):
    required_columns = ['Produk','Sales','Cost Pabrik 1','Cost Pabrik 2','Cost Pabrik 3','Demand Area 1','Demand Area 2','Demand Area 3']
    for col in required_columns:
        if col not in df.columns:
            st.error(f'Missing required columns: {col}')
            return
        
    for i in df.columns:
        if i != 'Produk':
            df[i] = df[i].astype(int)
            
    df = [col.replace(' ','_') for col in df]
            
#Margin
def margin(df):
    df['Margin_1'] = ['Sales'] - ['Cost_Pabrik_1']
    df['Margin_2'] = ['Sales'] - ['Cost_Pabrik_2']
    df['Margin_3'] = ['Sales'] - ['Cost_Pabrik_3']
    

