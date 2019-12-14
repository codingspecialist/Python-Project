import requests
import json
from Movie import Movie

def getMovie(page):
    url = f"https://yts.am/api/v2/list_movies.json?sort_by=rating&limit=6&page={page}"
    response = requests.get(url = url)

    #json.dumps - json output - dict -> json
    #json.loads - json input - json -> dict
    html = json.loads(response.text)
    #print(type(html))
    data = html['data']
    # print(data['movie_count'])
    # print(data['limit'])
    # print(data['page_number'])
    movies = data['movies']
    #print(type(movies))

    list = []
    for i in movies:
        m = Movie(
            i['rating'], 
            i['title'],
            i['synopsis'][0:230], 
            i['medium_cover_image'] 
        )
        list.append(m)
        # print(movies[0]['id'])
        # print(movies[0]['title'])
        # print(movies[0]['medium_cover_image'])
        # print(movies[0]['synopsis'])

        #print(response.status_code)
        #print(response.text)
    
    return list
