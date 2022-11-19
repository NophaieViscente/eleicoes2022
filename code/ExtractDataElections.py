import pandas as pd
import requests
import json
import time



class ExtractDataElections :

    '''
        This class extract data of results of elections in the Brazil
    '''

    CODE_ROLES = {
    'c0001' :'Presidente Majoritário',
    'c0003': 'Governador',
    'c0005': 'Senador',
    'c0011': 'Prefeito',
    'c0006': 'Deputado Federal',
    'c0007': 'Deputado Estadual',
    'c0008': 'Deputado Distrital',
    'c0013': 'Vereador'}

    def __init__(self, API_RESULTS:str, API_RESULTS_CANDIDATE:str, CODE_ROLES:dict=CODE_ROLES) :
        '''
            Args: 
                API_RESULTS : A URL to get ufs
                API_RESULTS_CANDIDATE: A part of a URL to get results by role and state
                CODE_ROLES : A dict with code and role name
        '''
        self.api = API_RESULTS
        self.candidate = API_RESULTS_CANDIDATE
        self.code_roles = CODE_ROLES
    
    def get_json_of_data(self) :
        dict_ = json.loads(
            requests.get(
                self.api).content)
        return dict_

    def get_ufs(self) :
        dict_ = self.get_json_of_data()

        list_ufs = [
            uf.split('/')[-1].split('.')[0].lower() 
            for uf in dict_['assetGroups'][1]['urls'] 
            if 'bandeiras-estados' in uf ]

        return list_ufs
    
    def get_results_candidate(self) :
        UFS = self.get_ufs()

        dataframe = pd.DataFrame()
        for uf in UFS :
            for code in self.code_roles :
                print(f'CAPTURANDO DADOS DE {self.code_roles.get(code)} PARA O ESTADO DE {uf.upper()}')
                try :
                    response = requests.get(f"{self.candidate}{uf}/{uf}-{code}-e000546-r.json")
                    data_tmp = pd.DataFrame(json.loads(response.content)['cand'])
                    data_tmp['COD_CARGO'] = code
                    data_tmp['UF'] = uf.upper()
                    data_tmp['CARGO'] = self.code_roles.get(code)
                except :
                    print(f"O ESTADO DE {uf.upper()} NÃO TEM DADOS PARA {self.code_roles.get(code)}")
            print('----------------')
            dataframe = pd.concat([dataframe, data_tmp])
            print()
            time.sleep(1)
        
        dataframe['n_partido'] = dataframe['n'].apply(lambda x: x[:2])
        return dataframe