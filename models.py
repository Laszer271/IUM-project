from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

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
        pass
    
    def fit(self, df):
        combinations = pd.DataFrame({'category': df['category_path'],
                                     'product_id': df['product_id']})
        combinations = combinations.drop_duplicates()
        self.possible_combinations = combinations.reset_index(drop=True)
        return self
    
    def save(self, path):
        self.possible_combinations.to_csv(path, index=False)
        
    def load(self, path):
        self.possible_combinations = pd.read_csv(path)
        
    def predict(self, category, products_in_session, n):
        if not self.possible_combinations['category'].str.contains(category).any():
            raise ValueError('There was no such category in training set')
        df = self.possible_combinations
        df = df.loc[df['category'] == category] # only the products from given category are considered
        df = df.drop(df['product_id'].isin(products_in_session)) # products viewed in session do not repeat
        return df['product_id'].sample(min(n, len(df))) # sample with uniform probability without
    
class ParametrizedModel(BaselineModel):
    def __init__(self):
        pass
    
    def fit(self, df):
        super().fit(df)
        weights = df.groupby('product_id')['product_id'].count().reset_index(drop=True)
        for category in self.possible_combinations['category']:
            mask = self.possible_combinations['category'] == category
            masked_weights = weights.loc[mask]
            weights.loc[mask] = masked_weights / masked_weights.sum()
        self.possible_combinations['weight'] = weights
        return self
        
    def predict(self, category, products_in_session, n):
        if not self.possible_combinations['category'].str.contains(category).any():
            raise ValueError('There was no such category in training set')
        df = self.possible_combinations
        df = df.loc[df['category'] == category] # only the products from given category are considered
        df = df.drop(df['product_id'].isin(products_in_session)) # products viewed in session do not repeat
        return df['products'].sample(min(n, len(df)), df['weight']) # sample with probability according to learnt weights