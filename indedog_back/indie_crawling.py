import requests
from bs4 import BeautifulSoup
import pprint
import json
import re

movie_data = []
i = 5570

# 인디그라운드 독립영화 DB 크롤링

while i < 5581:
  url = f'https://indieground.kr/indie/movieLibraryView.do?seq={i}&type=D'
  response = requests.get(url, verify=False)
  cnt = 0
  
  if response.status_code == 200:
      html = response.text
      soup = BeautifulSoup(html, 'html.parser')
      content = ''
      if soup.select_one('h2.subject'):
        print(i)
        title = soup.select_one('h2.subject').text.split('\n')[0]
        # director = soup.select_one('div.detail')
        # print(director)
        explain = soup.select_one('div.explain > ul.cf').text.split('\n')
        title_en = explain[1]
        making_year = explain[2]
        genre = explain[3]
        length = explain[4] + explain[5].strip('\t')
        detail = soup.select_one('div.detail').text.split()
        if soup.select_one('div.movie_story > dl > dd'):
            content = soup.select_one('div.movie_story > dl > dd').text
        pprint.pprint(content)
        director = ''
        actors = ''
        keywords = ''
        age = ''

        for el in explain:
            if '관람가' in el or '미분류' in el:
                age = el.strip('\t')

        for el in detail:
            if el == '감독':
                cnt = 1
                continue
            elif '#' in el:
                keywords += el
                continue
            elif el == '출연':
                cnt = 2
                continue
            elif el == '키워드':
                cnt = 3
            
            if cnt == 1:
                director += el
            elif cnt == 2:
                actors += el

        movieInfo = {
            "model": "movies.movie",
            "pk": i,
            "fields": {
                'age': age,
                'genre': genre,
                'title': title,
                'title_en': title_en,
                'director': director,
                'keywords': keywords,
                'making_year': making_year,
                'actors': actors,
                'length': length,
                'img_src': 'https://indieground.kr'+soup.select_one('div.movie_info_poster > img')['src'],
                'detail': json.dumps(soup.select_one('div.detail').text.split(), ensure_ascii=False),
                'content': content,
            }
        }
        movie_data.append(movieInfo)
        pprint.pprint(movieInfo)
      else:
        continue
  else : 
      print(response.status_code)
      break
  
  i += 1
  
with open("movie_data.json", "w", encoding='utf-8') as f:
    json.dump(movie_data, f, indent=2, ensure_ascii=False)
