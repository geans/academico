# -*- coding: utf-8 -*-
from pandas import read_csv, isna, concat
from math import log


class HandlePreProccess:
    def __init__(self, csv_path):
        self.__ds = read_csv(csv_path)

    def handle_NaN(self):
        print('  * Preenchendo campos vazios')
        self.__ds.fillna(self.__ds.mean(), inplace=True)

        #print('  * Removendo campos vazios')
        #for feature in list(self.__ds)[:-1]:
        #    self.__ds = self.__ds[isna(self.__ds[feature]) != True]
        
    def normalize(self):
        print('  * Normalizando valores')
        self.__ds = (self.__ds - self.__ds.min()) / (self.__ds.max() - self.__ds.min())

    def worse_col_by_entropy(self, target_col=None):
        if target_col is None:
            target_col = list(self.__ds)[-1]
        print('  * Calculando entropia para escolher pior coluna')
        # calculate frequency
        len_dataset = len(self.__ds)  # number of instances
        entropy_dict = {}
        frequency_dict = {}
        numer_group = 10
        max_entropy = 0
        worse_col = None
        for feature in list(self.__ds)[:-1]:
            frequency_dict[feature] = []
            groups_dict = {}
            delta = (self.__ds[feature].max() - self.__ds[feature].min()) / numer_group
            limit = 0
            for i in range(numer_group):
                groups_dict[i] = self.__ds[limit < self.__ds[feature]]
                groups_dict[i] = self.__ds[self.__ds[feature] < (limit+delta)]
                limit += delta
                for symbol in [1]:
                    occurence = 0.0
                    for instance in groups_dict[i][target_col]:
                        if instance == symbol:
                            occurence += 1
                    if len(groups_dict[i]) != 0:
                        frequency_dict[feature] += [occurence / len(groups_dict[i])]
            ent = 0.0
            for f in frequency_dict[feature]:
                if f != 0:
                    ent += f * log(f, 2)
            if -ent > max_entropy:
                max_entropy = -ent
                worse_col = feature

            #print(feature.ljust(25), str(-ent).ljust(30))
            entropy_dict[feature] = -ent
        print('    * Maior entropia em:', worse_col, ', valor:', max_entropy)
        return [worse_col]

    def remove_outlies(self, low_quantile=.07, up_quantile=.93):
        print('  * Removendo "outlies"')
        
        # Segment by last column
        outcome = list(self.__ds)[-1]
        ds0 = self.__ds[self.__ds[outcome] == 0]
        ds1 = self.__ds[self.__ds[outcome] == 1]

        get_ds = []
        for current_ds in [ds0, ds1]:
            ds = current_ds
            for feature in ['Glucose']:
                lower_limit = current_ds[feature].quantile(low_quantile)
                upper_limit = current_ds[feature].quantile(up_quantile)
                ds = ds[ds[feature] < upper_limit]
                ds = ds[lower_limit < ds[feature]]
            get_ds += [ds]
        self.__ds = concat(get_ds)
        #print('Número de linhas restante:', len(self.__ds['Outcome']))

    def remove_col(self, cols):
        print('  * Removendo colunas:', cols)
        current_cols = list(self.__ds)
        for col in cols:
            current_cols.remove(col)
        self.__ds = self.__ds[current_cols]

    def search_bad_cols(self):
        print('  * Procurando colunas com mais de 30% de NaN')
        counter = 0
        len_dataset = len(self.__ds)
        col_to_remove = []
        for i in list(self.__ds)[:-1]:
            if len(self.__ds[isna(self.__ds[i])]) / len_dataset > 0.3:
                col_to_remove += [i]
        print('    * Colunas esparsas:', col_to_remove)
        return col_to_remove

    def out_csv(self, name):
        self.__ds.to_csv(name, index=False)
    
    def features(self):
        return list(self.__ds)[:-1]
    
def run():
    print('   Em diabetes_dataset.csv')
    dataset = HandlePreProccess('raw_diabetes_dataset.csv')
    bad_cols = dataset.search_bad_cols() #+ dataset.worse_col_by_entropy()
    
    # Aplicando funções
    dataset.remove_col(bad_cols)
    dataset.handle_NaN()
    dataset.remove_outlies()
    
    dataset.out_csv("diabetes_dataset.csv")

    print('   Em diabetes_app.csv')
    dataapp = HandlePreProccess('raw_diabetes_app.csv')
    dataapp.remove_col(bad_cols)
    dataapp.out_csv("diabetes_app.csv")
    
    return dataset.features()

if __name__ == "__main__":
    run()
