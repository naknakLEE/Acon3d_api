import pandas as pd

def insert_db(data_df_2):
    try:
        data_df_2.to_csv('../db/acon3d_db.csv',
            sep=',',
            na_rep='NaN',
            float_format = '%.2f',
            index = False)
        return True
    except:
        return False

def load_db():
    df = pd.read_csv ('../db/user_db.csv')
    return df

def load_product_db():
    df = pd.read_csv ('../db/acon3d_db.csv')
    return df
