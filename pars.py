import requests
from bs4 import BeautifulSoup

def get_songs_and_lyrics(artist_name):
    # Заменяем пробелы на знак "+" для поиска в URL
    artist_name = artist_name.replace(" ", "+")
    url = f"https://genius.com/artists/{artist_name}"
    
    # Отправляем запрос
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Ошибка при запросе: {response.status_code}")
        return
    
    # Парсим HTML страницы
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ищем все ссылки на песни
    song_links = soup.find_all("a", {"class": "song_link"})
    
    with open(f"{artist_name}_songs.txt", "w", encoding="utf-8") as file:
        for song_link in song_links:
            song_url = song_link.get('href')
            if song_url:
                song_name = song_link.get_text().strip()
                print(f"Обрабатываю песню: {song_name}")
                
                # Получаем текст песни по ссылке
                song_page_response = requests.get(song_url)
                song_page_soup = BeautifulSoup(song_page_response.text, 'html.parser')
                lyrics_div = song_page_soup.find("div", {"class": "lyrics"})
                
                if lyrics_div:
                    lyrics = lyrics_div.get_text().strip()
                    file.write(f"Песня: {song_name}\n")
                    file.write(f"Текст:\n{lyrics}\n\n")
                else:
                    print(f"Текст песни не найден: {song_name}")
    
    print(f"Тексты песен и их названия сохранены в файл: {artist_name}_songs.txt")

# Пример использования
artist = "Splean"  # Укажите имя исполнителя
get_songs_and_lyrics(artist)
