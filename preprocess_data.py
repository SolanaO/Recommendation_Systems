# Import libraries and packages

import pandas as pd
import numpy as np
import pickle

# Import the datasets
df = pd.read_csv('data/user-item-interactions.csv', index_col=[0])
df_content = pd.read_csv('data/articles_community.csv', index_col=[0])


def email_mapper():

    '''
    Function that maps the user email to a generated user_id.
    The initial email column is removed.
    '''
    coded_dict = dict()
    cter = 1
    email_encoded = []

    for val in df['email']:
        if val not in coded_dict:
            coded_dict[val] = cter
            cter+=1

        email_encoded.append(coded_dict[val])
    return email_encoded

# Create a function that picks the title
def get_title(row):

    '''
    The function selects one value from two given column entries.
    '''

    if row['_merge'] == 'left_only':
        return row['doc_full_name']
    else:
        return row['title']


# Preprocess the user-item interactions dataset
def clean_df():

    '''
    Function to preprocess the user-item interaction dataset.
    '''

    # Create new user_id column
    df['user_id'] = email_mapper()

    # Drop columns
    df.drop(columns=['email'], inplace=True)

    # Change dtypes
    df['article_id'] = df['article_id'].astype(int)

    return df


### User based data

# Dataframe to keep track of the articles accessed by a user

def user_based_data():

    '''
    Create a dataframe that contains information on user activity.
    '''

    articles_per_user = pd.pivot_table(df,
                    values=['article_id'],
                    index='user_id',
                    aggfunc={'article_id': list})

    articles_per_user.reset_index(inplace=True)

    # Create a new column that records how many articles a user accessed
    articles_per_user['articles_count'] = [len(x) for x in articles_per_user.article_id]

    # Create a column that records how many unique articles the user accessed
    articles_per_user['unique_articles_count'] = [len(set(x)) for x in articles_per_user.article_id]

    return articles_per_user


### Item based data

def clean_df_content():

    '''
    Function to preprocess the content dataset.
    '''

    # Remove any rows that have the same article_id - only keep the first
    df_content.drop_duplicates(subset=['article_id'], keep='first', inplace=True)

    return df_content


def article_based_data():

    '''
    Create a dataframe that contains all titles on IBM platform and the information on
    how they were accessed.
    '''

    # Dataframe to keep track of the users that accessed a given article
    users_per_article = pd.pivot_table(df,
                    values=['user_id'],
                    index='article_id',
                    aggfunc={'user_id': list})
    users_per_article.reset_index(inplace=True)

    # Rename column
    users_per_article.rename(columns={'user_id': 'users_accessed'}, inplace=True)

    # Count how many times each article is viewed
    article_views = pd.DataFrame(df.groupby(['article_id']).count()['user_id'])

    # Rename column
    article_views.rename(columns={'user_id': 'views'}, inplace=True)

    # Extract article_id and title from df
    df_titles = df[['article_id', 'title']].copy()

    # Drop duplicates to obtain a clean list of articles
    df_titles.drop_duplicates(inplace=True)

    # Combine the titles with the view counts and the user lists
    df_title_info = pd.merge(
    article_views, df_titles, on='article_id').merge(
    users_per_article, on='article_id').set_index('article_id')

    # Perform an outer join of df_content and df_title_info dataframe
    df_content_full = pd.merge(df_content, df_title_info, on='article_id', how='outer', indicator=True)

    # Create a new column that combines the available titles
    df_content_full['doc_name'] = df_content_full.apply(lambda x: get_title(x), axis=1)

    # Create a new column where NaN values in user_id are replaced by empty lists
    df_content_full['users_accessed'] = [ [] if x is np.NaN else x for x in df_content_full['users_accessed'] ]

    # Drop columns
    df_content_full.drop(columns=['doc_full_name', 'doc_status', 'title', '_merge'], inplace=True)

    # Replace the missing views counts by 0
    df_content_full['views'] = df_content_full['views'].fillna(0)

    # Change dtypes
    df_content_full['views'] = df_content_full['views'].astype(int)

    return df_content_full


def main():

    df = clean_df()
    df.to_csv('data/df.csv', index=True)

    articles_per_user = user_based_data()
    articles_per_user.to_csv('data/articles_per_user.csv', index=True)

    df_content = clean_df_content()
    df_content.to_csv('data/df_content.csv', index=True)

    df_content_full = article_based_data()
    df_content_full.to_csv('data/users_per_article.csv', index=True)

if __name__ == '__main__':
    main()
