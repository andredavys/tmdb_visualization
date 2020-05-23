import pandas as pd

def pre_processing_movies_data(df_movies):
    df_movies.release_date = df_movies.release_date.map(lambda x: str(x))
    df_movies.budget = pd.to_numeric(df_movies.budget, errors='coerce')
    df_movies.revenue = pd.to_numeric(df_movies.revenue, errors='coerce')
    df_movies.release_date = pd.to_datetime(df_movies.release_date, errors='coerce')
    df_movies.popularity = pd.to_numeric(df_movies.popularity, errors='coerce')

    # datarange by year
    df_movies = df_movies[(df_movies.release_date.dt.year > 1965) & (df_movies.release_date.dt.year < 2017)]

    # groupby movies by month
    df_movies.set_index(['release_date'], inplace=True)
    return df_movies

def get_genres_from_row(row):
    aux_row = row[1:-1]
    raw_genres = aux_row.split('}')
    genres = list()
    for g in raw_genres:
        aux = g.split(':')
        if len(aux) >= 3:
            genre = aux[2].replace("'", "")
            genres.append(genre)
    return genres

def build_movie_attr_dict(movies_dict, attr):
    attr_dict = dict()
    for _id, movie_dict in movies_dict.items():
#         movie_id = f"{_id}_{movie_dict['title']}"
        movie_id = f"{movie_dict['title']}"
        attr_dict[movie_id] = movie_dict[attr]
    return attr_dict

def sort_movies_by_attr(movies_dict, attr, desc=True):
    attr_dict = build_movie_attr_dict(movies_dict, attr)
    return {k: v for k, v in sorted(attr_dict.items(), key=lambda item: item[1], reverse=desc)}

def mount_movies_dict(df):
    movies_dict = dict()

    for i, row in df.iterrows():
        id_movie = row['id']
        inner_dict = dict(
            title=row['original_title'],
            budget=float(row['budget']),
            vote_count=float(row['vote_count']),
            vote_avg=float(row['vote_average']),
            revenue=float(row['revenue']),
            genres=get_genres_from_row(row['genres']),
            runtime=float(row['runtime']),
            popularity=float(row['popularity']),
            profit=float(row['revenue'])-float(row['budget'])
        )   
        movies_dict[id_movie] = inner_dict
    
    return movies_dict

def mount_genres_count_dict(movies_dict):
    genres_dict = build_movie_attr_dict(movies_dict, 'genres')
    genres_count_dict = dict()
    for movie, genres in genres_dict.items():
        for genre in genres:
            genre = genre[1:]
            if genre in genres_count_dict:
                genres_count_dict[genre] += 1
            else:
                genres_count_dict[genre] = 1
    genres_count_dict = {k: v for k, v in sorted(genres_count_dict.items(), key=lambda item: item[1], reverse=True)}
    return genres_count_dict

# to do visualization by overtime
def create_day_month_year_column(df):
    days = list()
    months = list()
    years = list()
    for i, row in df.iterrows():
        date = str(i)
        years.append(date.split('-')[0])
        months.append(date.split('-')[1])
        days.append(date.split('-')[2])
    new_df = df.copy()
    print(len(days), len(months), len(years), len(new_df))
    new_df['day'] = days
    new_df['month'] = months
    new_df['year'] = years
    return new_df

def normalize_count_by_year(df):
    norm_df = df.copy()
    norm_count = list()
    for year in df.year.unique():
        y = df[(df.year==str(year))].aux_count
        df.loc[y.index, 'norm_count'] = y.values/sum(y)
    return df