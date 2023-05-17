import pandas as pd


class DataSanitizer:
    def __init__(self, data: pd.DataFrame, **kwargs):
        self.data = data
        for k in kwargs:
            if hasattr(self, k):
                getattr(self, k)(kwargs[k])
            elif kwargs[k] is None:
                pass
            else:
                self.data = self.data.loc[self.data[k] == kwargs[k]]

    def gt(self, d: dict):
        self.data = self.data.loc[(self.data[list(d)] > pd.Series(d).dropna()).all(axis=1)]

    def gte(self, d: dict):
        self.data = self.data.loc[(self.data[list(d)] >= pd.Series(d).dropna()).all(axis=1)]

    def lt(self, d: dict):
        self.data = self.data.loc[(self.data[list(d)] < pd.Series(d).dropna()).all(axis=1)]

    def lte(self, d: dict):
        self.data = self.data.loc[(self.data[list(d)] <= pd.Series(d).dropna()).all(axis=1)]

    # def _contains(self, d: dict):
    #     self.data = self.data.loc[(self.data[list(d)].str.contains(d).dropna()).all(axis=1)]

    def _orderBy(self, d: dict):
        self.data = self.data.sort_values(by=list(d.keys()), ascending=list(d.values()))

    def getData(self):
        return self.data
