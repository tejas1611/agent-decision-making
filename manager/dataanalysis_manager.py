import pandas as pd


class DataAnalysisManager:
    def __init__(self, algorithm: str, output: str):
        self.algorithm = algorithm
        self.output = output

    def save(self, data: dict):
        dataframe = pd.DataFrame.from_dict(data) 
        dataframe.to_csv(f'docs/analysis/{self.algorithm}_{self.output}.csv', index=None)