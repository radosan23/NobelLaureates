import pandas as pd
import os
import requests
import sys
import numpy as np
import re


def check_data():
    if not os.path.exists('../Data'):
        os.mkdir('../Data')
    if 'Nobel_laureates.json' not in os.listdir('../Data'):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = "https://www.dropbox.com/s/m6ld4vaq2sz3ovd/nobel_laureates.json?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/Nobel_laureates.json', 'wb').write(r.content)
        sys.stderr.write("[INFO] Loaded.\n")


def main():
    # prepare dataset
    check_data()
    df = pd.read_json('../Data/Nobel_laureates.json')
    df.dropna(subset=['gender'], inplace=True, ignore_index=True)
    # correct birthplace
    df['place_of_birth'] = df['place_of_birth'].apply(lambda x: x.split(',')[-1].strip() if x and ',' in x else np.nan)
    df['born_in'].replace('', np.nan, inplace=True)
    df['born_in'].fillna(df['place_of_birth'], inplace=True)
    df.dropna(subset='born_in', inplace=True, ignore_index=True)
    df.replace(['US', 'United States', 'U.S.'], 'USA', inplace=True)
    df.replace('United Kingdom', 'UK', inplace=True)
    # calculate age of winning
    df['year_born'] = df['date_of_birth'].apply(lambda x: re.search(r'\d{4}', x).group()).astype('int64')
    df['age_of_winning'] = df['year'] - df['year_born']
    print(df['year_born'].to_list(), df['age_of_winning'].to_list(), sep='\n')


if __name__ == '__main__':
    main()
