# -*- coding: utf-8 -*-
from pandas import read_csv, isna, concat
from math import log

def debug(value=''):
    DEBUG = False
    if DEBUG:
        print(value)

class HandlePreProccess:
    def __init__(self, csv_path):
        self.ds = read_csv(csv_path)

    def handle_NaN(self):
        debug('  * Preenchendo campos vazios')
        self.ds.fillna(self.ds.mean(), inplace=True)
        
    def normalize(self, cols_list):
        debug('  * Normalizando valores')
        for c in cols_list:
            x = self.ds[c]
            x = (x - x.min()) / (x.max() - x.min())
            self.ds[c] = x

    def col_by_entropy(self, target_col=None):
        if target_col is None:
            target_col = list(self.ds)[-1]
        debug('  * Calculando entropia para escolher pior coluna')
        # calculate frequency
        len_dataset = len(self.ds)  # number of instances
        entropy_dict = {}
        frequency_dict = {}
        numer_group = 10
        max_entropy = 0
        min_entropy = 0xEFFFFFFF
        worse_col = None
        best_col = None
        for feature in list(self.ds)[:-1]:
            frequency_dict[feature] = []
            groups_dict = {}
            delta = (self.ds[feature].max() - self.ds[feature].min()) / numer_group
            limit = 0
            for i in range(numer_group):
                groups_dict[i] = self.ds[limit < self.ds[feature]]
                groups_dict[i] = self.ds[self.ds[feature] < (limit+delta)]
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
            if max_entropy < -ent:
                max_entropy = -ent
                worse_col = feature
            if min_entropy > -ent:
                min_entropy = -ent
                best_col = feature

            #print(feature.ljust(25), str(-ent).ljust(30))
            entropy_dict[feature] = -ent
        debug('    * Maior entropia em: {}, valor: {}'.format(worse_col, max_entropy))
        return worse_col, best_col

    def remove_outlies(self, by_feature_list, low_quantile=.07, up_quantile=.93):
        debug('  * Removendo "outlies"')
        
        # Segment by last column
        outcome = list(self.ds)[-1]
        ds0 = self.ds[self.ds[outcome] == 0]
        ds1 = self.ds[self.ds[outcome] == 1]

        get_ds = []
        for current_ds in [ds0, ds1]:
            ds = current_ds
            for feature in by_feature_list:
                lower_limit = current_ds[feature].quantile(low_quantile)
                upper_limit = current_ds[feature].quantile(up_quantile)
                ds = ds[ds[feature] < upper_limit]
                ds = ds[lower_limit < ds[feature]]
            get_ds += [ds]
        self.ds = concat(get_ds)
        #debug('Número de linhas restante:', len(self.ds['Outcome']))

    def remove_col(self, cols):
        debug('  * Removendo colunas: {}'.format(cols))
        current_cols = list(self.ds)
        for col in cols:
            current_cols.remove(col)
        self.ds = self.ds[current_cols]

    def search_bad_cols(self):
        debug('  * Procurando colunas com mais de 30% de NaN')
        counter = 0
        len_dataset = len(self.ds)
        col_to_remove = []
        for i in list(self.ds)[:-1]:
            if len(self.ds[isna(self.ds[i])]) / len_dataset > 0.3:
                col_to_remove += [i]
        debug('    * Colunas esparsas: {}'.format(col_to_remove))
        return col_to_remove

    def out_csv(self, name):
        debug('  * Gravando em {}'.format(name))
        self.ds.to_csv(name, index=False)
    
    def features(self):
        list_ds = list(self.ds)
        return list_ds[:-1], list_ds[-1]

    def replace(self, feature, to_replace, value):
        debug('  * Substituindo {} por {}'.format(to_replace, value))
        self.ds[feature] = self.ds[feature].replace(to_replace, value)
    
def run():
    debug('   Em abalone_dataset.csv')
    dataset = HandlePreProccess('raw_abalone_dataset.csv')
    dataset.replace('sex', 'M', 1)
    dataset.replace('sex', 'F', 2)
    dataset.replace('sex', 'I', 3)
    # worse_col, best_col = dataset.col_by_entropy()
    # bad_cols = dataset.search_bad_cols()
    
    # Aplicando funções
    numeric_cols = dataset.features()[0][1:]
    dataset.normalize(numeric_cols)
    #dataset.remove_col(bad_cols)
    #dataset.handle_NaN()
    #dataset.remove_outlies([best_col])
    
    dataset.out_csv("abalone_dataset.csv")

    debug('   Em abalone_app.csv')
    dataapp = HandlePreProccess('raw_abalone_app.csv')
    dataapp.replace('sex', 'M', 1)
    dataapp.replace('sex', 'F', 2)
    dataapp.replace('sex', 'I', 3)
    #dataapp.remove_col(bad_cols)
    dataapp.out_csv("abalone_app.csv")
    
    return dataset.features()

if __name__ == "__main__":
    run()
