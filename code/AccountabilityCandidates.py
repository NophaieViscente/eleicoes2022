import pandas as pd
import requests
import json

class AccountabilityCandidates :

    '''
        This class get data of accountability of candidates
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

    def __init__(
        self,API_ACCOUNTABILITY:str)->None :

        self.url_base = API_ACCOUNTABILITY
    
    def mount_url_accountability(
        self, dataframe:pd.DataFrame)->list :
        
        url_base = self.url_base
        urls_candidates = list()

        for idx, row in dataframe.iterrows() :
            
            url_getter_candidate = f"{url_base}{row['UF']}/"
            url_getter_candidate+=f"{row['COD_CARGO'][-1:]}/"
            url_getter_candidate+=f"{row['n_partido']}/{row['n']}/{row['sqcand']}"

            urls_candidates.append(url_getter_candidate)
        
        return urls_candidates

    def get_account_candidates(
        self, dataframe:pd.DataFrame)->pd.DataFrame :

        urls = self.mount_url_accountability(dataframe=dataframe)

        df_expenses = pd.DataFrame()
        df_donors = pd.DataFrame()
        df_providers = pd.DataFrame()

        for url in urls :
            url_splitted = url.split('/')
            print(f"Capturando dados de {url_splitted[10]}, candidato: {url_splitted[-1]}")
            try :
                response = requests.get(url)
                dict_response = json.loads(response.text)
                df_tmp_expenses = pd.DataFrame(dict_response['concentracaoDespesas'])
                df_tmp_donors = pd.DataFrame(dict_response['rankingDoadores'])
                df_tmp_providers = pd.DataFrame(dict_response['rankingFornecedores'])

                df_tmp_expenses['id_candidato'] = url_splitted[-1]
                df_tmp_donors['id_candidato'] = url_splitted[-1]
                df_tmp_providers['id_candidato'] = url_splitted[-1]

                df_expenses = pd.concat([df_expenses, df_tmp_expenses], axis=0)
                df_donors = pd.concat([df_donors, df_tmp_donors], axis=0)
                df_providers = pd.concat([df_providers, df_tmp_providers], axis=0)
            except:
                print(f'ERRO URL: {url}')
                continue
                
        return df_expenses, df_donors, df_providers