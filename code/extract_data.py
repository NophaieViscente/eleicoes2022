# Libs
from decouple import config
from ExtractDataElections import ExtractDataElections as TSE
from AccountabilityCandidates import AccountabilityCandidates as ACCOUNT

# Load Enviroment Vars
RAW_DATA_PATH = config('RAW_DATA_PATH')
PROCESSED_DATA_PATH = config('PROCESSED_DATA_PATH')
RAW_DATA_PATH = config('RAW_DATA_PATH')
API_RESULTS = config('API_RESULTS')
API_RESULTS_CANDIDATE = config('API_RESULTS_CANDIDATE')
API_ACCOUNTABILITY = config('')

# Create Main Method
def main () :
    # Extract data
    extract_data = TSE(API_RESULTS, API_RESULTS_CANDIDATE)
    data = extract_data.get_results_candidate()
    data.to_csv(RAW_DATA_PATH+'dataframe_eleicoes2022.csv',index=False)

    # Extract data of expenses, donors and providers of each candidate
    account = ACCOUNT(API_ACCOUNTABILITY=API_ACCOUNTABILITY)
    expenses, donors, providers = account.get_account_candidates(data)
    expenses.to_csv(RAW_DATA_PATH+'dataframe_despesas_candidatos2022.csv')
    donors.to_csv(RAW_DATA_PATH+'dataframe_doacoes_candidatos2022.csv')
    providers.to_csv(RAW_DATA_PATH+'dataframe_fornecedores_candidatos2022.csv')


if __name__ == '__main__' :
    main()