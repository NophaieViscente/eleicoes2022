# Libs
from decouple import config
from ExtractDataElections import ExtractDataElections as TSE

# Load Enviroment Vars
RAW_DATA_PATH = config('RAW_DATA_PATH')
PROCESSED_DATA_PATH = config('PROCESSED_DATA_PATH')
RAW_DATA_PATH = config('RAW_DATA_PATH')
API_RESULTS = config('API_RESULTS')
API_RESULTS_CANDIDATE = config('API_RESULTS_CANDIDATE')

# Create Main Method
def main () :
    # Extract data
    extract_data = TSE(API_RESULTS, API_RESULTS_CANDIDATE)
    data = extract_data.get_results_candidate()
    data.to_csv(RAW_DATA_PATH+'dataframe_eleicoes2022.csv',index=False)


if __name__ == '__main__' :
    main()