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
    columns_to_impute = [col for col in df.columns if col != 'Produk']
    preprocessor = ColumnTransformer([
        ('imputasi', SimpleImputer(strategy='constant', fill_value=0), columns_to_impute)],
        remainder='passthrough',
        verbose_feature_names_out=False
    )
    preprocessor.fit(df)
    df = preprocessor.transform(df)
    df = pd.DataFrame(df, columns=preprocessor.get_feature_names_out())
    cols = df.columns.tolist()
    cols.insert(0, cols.pop(-1))
    df = df[cols]
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


#Upload File 
uploaded_file = st.file_uploader("Upload Excel Master Data", type=["xlsx"])

#Upload
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        df = preprocessing(df)
        convert_df(df)
        margin(df)
        st.write(df)
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")

