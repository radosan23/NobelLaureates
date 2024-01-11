import pandas as pd
import os
import requests
import sys


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
    check_data()
    df = pd.read_json('../Data/Nobel_laureates.json')
    df.dropna(subset=['gender'], inplace=True, ignore_index=True)
    print(df.duplicated().any())
    print(df.head(20)[['country', 'name']].to_dict())


if __name__ == '__main__':
    main()
