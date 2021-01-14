from abc import ABC, abstractmethod
import pandas as pd
import matplotlib.pyplot as plt

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
        pass
    
    def fit(self, df):
        super().fit(df)
        weights_list = []
        for category in self.categories:
            df_temp = df.loc[df['category_path'] == category]
            weights = df_temp.groupby('product_id')['product_id'].count()
            weights.plot(kind='bar')
            plt.show()
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