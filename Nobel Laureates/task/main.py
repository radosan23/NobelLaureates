import pandas as pd
import os
import requests
import sys
import numpy as np
import re
import matplotlib.pyplot as plt


def check_data():
    if not os.path.exists('../Data'):
        os.mkdir('../Data')
    if 'Nobel_laureates.json' not in os.listdir('../Data'):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = "https://www.dropbox.com/s/m6ld4vaq2sz3ovd/nobel_laureates.json?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/Nobel_laureates.json', 'wb').write(r.content)
        sys.stderr.write("[INFO] Loaded.\n")


def correct_birthplace(df):
    df['place_of_birth'] = df['place_of_birth'].apply(lambda x: x.split(',')[-1].strip() if x and ',' in x else np.nan)
    df['born_in'].replace('', np.nan, inplace=True)
    df['born_in'].fillna(df['place_of_birth'], inplace=True)
    df.dropna(subset='born_in', inplace=True, ignore_index=True)
    df.replace(['US', 'United States', 'U.S.'], 'USA', inplace=True)
    df.replace('United Kingdom', 'UK', inplace=True)
    df.drop(columns=['place_of_birth'], inplace=True)
    return df


def plot_countries(df):
    df['born_in'] = df['born_in'].apply(lambda x: 'Other countries' if df['born_in'].value_counts()[x] < 25 else x)
    colors = ['blue', 'orange', 'red', 'yellow', 'green', 'pink', 'brown', 'cyan', 'purple']
    explode = [0, 0, 0, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]
    data = df['born_in'].value_counts()
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.pie(data, colors=colors, explode=explode, labels=data.index,
           autopct=lambda pct: f'{pct:.2f}%\n({data.sum()*pct/100:.0f})')
    plt.show()


def plot_male_female(df):
    df['category'].replace('', np.nan, inplace=True)
    df.dropna(subset='category', inplace=True)
    data = df.groupby('category')['gender'].agg('value_counts')
    x_axis = np.arange(len(data[::2]))
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.suptitle('The total count of male and female Nobel Prize winners by categories', fontsize=20)
    ax.set_xlabel('Category', fontsize=14)
    ax.set_ylabel('Nobel Laureates Count', fontsize=14)
    ax.bar(x_axis - 0.2, data[::2], width=0.4, color='blue', label='Males')
    ax.bar(x_axis + 0.2, data[1::2], width=0.4, color='crimson', label='Females')
    ax.set_xticks(x_axis, data[::2].index.get_level_values(0))
    ax.legend()
    plt.show()


def main():
    # prepare dataset
    check_data()
    df = pd.read_json('../Data/Nobel_laureates.json')
    df.dropna(subset=['gender'], inplace=True, ignore_index=True)
    df = correct_birthplace(df)
    # calculate age of winning
    df['year_born'] = df['date_of_birth'].apply(lambda x: re.search(r'\d{4}', x).group()).astype('int64')
    df['age_of_winning'] = df['year'] - df['year_born']
    # plot male/female by category
    plot_male_female(df)


if __name__ == '__main__':
    main()
