import pandas as pd
import models
import re
import ast

def read_data(path):
    with open(path, 'r') as f:
        lines = f.readlines() 
        
    json_formatted = '['
    for line in lines:
        json_formatted += line + ','
    json_formatted = json_formatted[:-1] + ']' 
    json_formatted = re.sub('null', 'None', json_formatted)
    return ast.literal_eval(json_formatted)

if __name__ == '__main__':
    drive = 'data/'
    df_products = pd.DataFrame(read_data(drive + 'products.jsonl'))
    df_sessions = pd.DataFrame(read_data(drive + 'sessions.jsonl'))
    df_sessions = df_sessions[df_sessions["product_id"].notna()]
    
    df = df_products.set_index('product_id')
    df = df_sessions.join(df, on='product_id')
    df['product_id'] = df['product_id'].astype(int)
    df_viewed = df[df['event_type'] == 'VIEW_PRODUCT'].copy()
    df_bought = df[df['event_type'] == 'BUY_PRODUCT'].copy()
    
    baseline = models.BaselineModel()
    baseline.fit(df_viewed)
    better_model = models.ParametrizedModel()
    better_model.fit(df_viewed)

    session_id = df['session_id'].sample().squeeze()
    df_test = df_viewed[df_viewed['session_id'] == session_id]
    products = df_test['product_id']
    category = df_test['category_path'].iloc[0]
    baseline_preds = baseline.predict(products[:-1], category, 5)
    better_model_preds = better_model.predict(products[:-1], category, 5)