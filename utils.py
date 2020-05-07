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
            profit=float(row['budget'])-float(row['revenue'])
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
