from abc import ABC, abstractmethod
import pandas as pd
import random
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

class Model(ABC):
    @abstractmethod
    def fit(self, df):
        pass
    @abstractmethod
    def load(self, path):
        pass
    @abstractmethod
    def save(self, path):
        pass
    @abstractmethod
    def predict(self, category, products_in_session, n):
        pass
    
class BaselineModel(Model):
    def __init__(self):
        self.name = "simple"
        pass
    
    def fit(self, df):
        products = pd.DataFrame({'category': df['category_path'],
                                     'product_id': df['product_id']})
        products = products.drop_duplicates()
        self.products = products
        self.categories = products['category'].unique()
        return self
    
    def save(self, path):
        self.products.to_csv(path, index=False)
        
    def load(self, path):
        self.products = pd.read_csv(path)
        self.categories = self.products['category'].unique()
        
    def predict(self, category, products_in_session, n):
        if category not in self.categories:
            raise ValueError('There was no such category in training set')
        df = self.products
        df = df.loc[df['category'] == category] # only the products from given category are considered
        df = df.loc[~df['product_id'].isin(products_in_session)] # products viewed in session do not repeat
        return df['product_id'].sample(min(n, len(df))) # sample with uniform probability without
    
class ParametrizedModel(BaselineModel):
    def __init__(self):
        self.name = "complex"
        pass
    
    def fit(self, df):
        super().fit(df)
        weights_list = []
        for category in self.categories:
            df_temp = df.loc[df['category_path'] == category]
            weights = df_temp.groupby('product_id')['product_id'].count()
            weights = weights / weights.sum()
            weights_list.append(weights)
        weights = pd.concat(weights_list)
        weights = pd.DataFrame({'weight': weights}, index=weights.index)
        self.products = self.products.join(weights, on='product_id')
        return self
        
    def predict(self, category, products_in_session, n):
        if category not in self.categories:
            raise ValueError('There was no such category in training set')
        df = self.products
        weights = df['weight']
        category_mask = df['category'] == category # only the products from given category are considered
        df = df.loc[category_mask] 
        weights = weights[category_mask]
        not_viewed_mask = ~df['product_id'].isin(products_in_session)
        df = df.loc[not_viewed_mask] # products viewed in session do not repeat
        weights = weights[not_viewed_mask]
        return df['product_id'].sample(min(n, len(df)), weights=weights) # sample with probability according to learnt weights
    
class ModelContainer():
    def __init__(self, n=5):
        self.simple_model = BaselineModel()
        self.complex_model = None
        self.complex_path = None
        self.selected_model = self.simple_model

        self.AB = False
        self.current_session = []
        self.history = []
        df = pd.DataFrame(read_data('data/products.jsonl'))

        self.simple_model.fit(df)

        df = df[['product_id', 'category_path']].drop_duplicates()
        mapping = {}
        for i, row in df.iterrows():
            mapping[row['product_id']] = row['category_path']
        self.mapping = mapping
        self.n_to_predict = n
        
    def set_AB(self, mode):
        self.AB = mode
        return True
        
    def clear_session(self):
        self.current_session = []
        self.history = []
    
    # def load_model(self, path, model_type):
    #     if model_type == "simple":
    #         self.simple_model.load(path)
    #     if model_type == "complex":
    #         self.complex_model.load(path)

    def load_model(self, path):
        if self.complex_model == None:
            self.complex_model = ParametrizedModel()
        self.complex_model.load(path)
        self.complex_path = path
        return True

    def select_model(self, model_type):
        if model_type == "simple":
            self.selected_model = self.simple_model
        if model_type == "complex":
            if self.complex_model == None:
                return False
            self.selected_model = self.complex_model
        return True

    def predict(self, product_id):
        if self.AB:
            r = random.randint(0, 1)
            if r:
                model = self.simple_model
            else:
                model = self.complex_model
        else:
            model = self.selected_model

        category = self.mapping[product_id]
        self.current_session.append(product_id)
        preds = model.predict(category, self.current_session, self.n_to_predict)
        self.history.append({'CurrentSession': self.current_session.copy(),
                             'Model': model.name,
                             'Predictions': list(preds)})
        
        return preds
        
        
    
    