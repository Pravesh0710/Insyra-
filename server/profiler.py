import pandas as pd

def load_dataset(file_path):
    dataset=pd.read_csv(file_path)
    return dataset

def get_dataset_overview(dataset):
    print("Shape of data: ",dataset.shape)
    print("memory usage: ",dataset.memory_usage(deep=True).sum())

def get_missing_values(dataset):
    print("Missing values in dataset: \n")
    missing_values=dataset.isnull().sum()
    missing_percentage=dataset.isnull().mean() * 100
    print("missing values: ",missing_values)
    print("missing percentage: ",missing_percentage)


def get_duplicate_count(dataset):
    print("Duplicated values: ",dataset.duplicated().sum())


def get_column_data_types(dataset):
    print("Coloumn Data type:",dataset.dtypes)

def get_columns(dataset):
    print("Coloumns:",dataset.columns)


if __name__ == "__main__":

    file_path = "server/netflix_customer_churn.csv"

    df = load_dataset(file_path)

    get_dataset_overview(df)
    get_missing_values(df)
    get_duplicate_count(df)
    get_column_data_types(df)
    get_columns(df)