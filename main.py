import requests
import json
from tqdm import tqdm
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

# 1 Получать картинки по API с сайта dog.ceo.
# Идем на сайт про собак и делаем запрос
# Получаем список под пород
#breed ="bulldog"
#breed = 'affenpinscher'  # input()
breed = input("Введите название породы:")
token = config['Tokens']["yd_token"]
sub_breeds = requests.get(f'https://dog.ceo/api/breed/{breed}/list')
sub_breeds_list = sub_breeds.json()['message']
class YD:
    def __init__(self, token):
        self.token = token
    def CreateFolder(self, folder_name):
        self.folder_name = folder_name
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources'
        # Название и путь к папке
        self.params = {'path': f'{self.folder_name}'}
        # токен яндекс диска
        self.headers = {'Authorization': self.token}
        # создание папки
        requests.put(self.url, params=self.params, headers=self.headers)

    def upload_image(self, image_url):
        self.filename = image_url.split('/')[-2]+ "_" + image_url.split('/')[-1]
        self.params = {'url':image_url}
        data.append({"filename": self.filename})
        self.headers = {'Authorization': self.token}
        return requests.post(f'https://cloud-api.yandex.net/v1/disk/resources/upload?path={breed}%2F{self.filename}.jpg',
                      params=self.params,
                      headers=self.headers)
#Создаем экземпляр класса YD
yd = YD(token)
yd.CreateFolder(breed)
# данные для json файла
data = []
spisok_ssilok =[]
if len(sub_breeds_list) > 1:
    for sub_breed in sub_breeds_list:
        url = f'https://dog.ceo/api/breed/{breed}/{sub_breed}/images/random'
        response = requests.get(url)
        image_url = response.json()['message']
        spisok_ssilok.append(image_url)
else:
    url = f'https://dog.ceo/api/breed/{breed}/images/random'
    response = requests.get(url)
    print(response)
    image_url = response.json()['message']
    print(image_url)
    spisok_ssilok.append(image_url)
    print(spisok_ssilok)

for i in tqdm(spisok_ssilok):
    yd.upload_image(i)

with open(r"D:\NETOLOGY\Python_Full Stack\Kursovaya_work\Dogs_Api\result.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")
