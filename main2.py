import requests
import json
from tqdm import tqdm
import configparser
import os

#Создаем файл для хранения tokena
config = configparser.ConfigParser()
config.read('settings.ini')

# 1 Получать картинки по API с сайта dog.ceo.
# Идем на сайт про собак и делаем запрос
# Получаем список под пород
#breed ="bulldog"
#breed = 'affenpinscher'  # input()
#Вводим название породы
breed = input("Введите название породы:")
# получаем токен из файла
token = config['Tokens']["yd_token"]
# получаем всех подпород
sub_breeds = requests.get(f'https://dog.ceo/api/breed/{breed}/list')
sub_breeds_list = sub_breeds.json()['message']

class YD:
    def __init__(self, token):
        self.token = token
    # функция создает папку на яндекс.диске с названием породы
    def CreateFolder(self, folder_name):
        self.folder_name = folder_name
        # путь к я.диску
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources'
        # Название и путь к папке
        self.params = {'path': f'Dogs/{self.folder_name}'}
        # токен яндекс диска
        self.headers = {'Authorization': self.token}
        # создание папки
        requests.put(self.url, params=self.params, headers=self.headers)

    def upload_image(self, image_url):
        # Имя файла фотографии которую будем загружать берем из ссылки
        self.filename = image_url.split('/')[-2]+ "_" + image_url.split('/')[-1]
        #ссылка на  картинку
        self.params = {'url':image_url}
        # Добавляем в list имя файла чтобы потом добавить в json
        data.append({"filename": self.filename})
        self.headers = {'Authorization': self.token}
        # возвращаем запрос на загрузку картинки
        return requests.post(f'https://cloud-api.yandex.net/v1/disk/resources/upload?path=Dogs/{breed}%2F{self.filename}.jpg',
                      params=self.params,
                      headers=self.headers)
class DogApi:
    def great_list_of_links(self,breed_, sub_breeds_list_):
        list_of_links = []
        if len(sub_breeds_list_) > 1:
            for sub_breed in sub_breeds_list_:
                url = f'https://dog.ceo/api/breed/{breed_}/{sub_breed}/images/random'
                response = requests.get(url)
                image_url = response.json()['message']
                list_of_links.append(image_url)
        else:
            url = f'https://dog.ceo/api/breed/{breed}/images/random'
            response = requests.get(url)
            image_url = response.json()['message']
            list_of_links.append(image_url)
        return list_of_links

#Создаем экземпляр класса YD
dog_api = DogApi()
yd = YD(token)
yd.CreateFolder(breed)
# данные для json файла
data = []

for i in tqdm(dog_api.great_list_of_links(breed, sub_breeds_list)):
    yd.upload_image(i)
with open(os.path.abspath("result.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")
