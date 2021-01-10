import requests
from urllib.parse import urljoin
from alive_progress import alive_bar
import time
TOKEN = "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008"
TOKEN_YANDEX = "AgAAAAANNcmvAADLW75hgWZVrUfQr8jC3nwewvw"
API_BASE_URL = "https://api.vk.com/method/"
User_ID =  184809253
V = "5.77"
class User:
    BASE_URL = API_BASE_URL
    def __init__(self, token=TOKEN, version=V, count_max=5, user_id=User_ID):
        self.token = token
        self.version = version
        self.count_max = count_max
        self.user_id = user_id
        self.link_list = []
        self.count_like = 0
    def choose_biggest_size(self, sizes):
        SIZES = "smxopqryzw"
        return max(sizes, key=lambda s: SIZES.index(s["type"]))
    def get_photos(self):
        link = urljoin(API_BASE_URL, "photos.get")
        res = requests.get(
            link,
            params={
                "access_token": self.token,
                "v": self.version,
                "album_id": "profile",
                "count": self.count_max,
                "extended": 1,d
                "owner_id": self.user_id,
                "photo_sizes": 1,
            },
        )
        res_json = res.json()["response"]["items"]
        for photo in res_json:
            self.count_like = photo["likes"]["count"]
            biggest_size = self.choose_biggest_size(photo["sizes"])
            new_dict = {
                "ID Фото": photo["id"],
                "наибольший размер": biggest_size,
                "Тип": biggest_size["type"],
            }
            self.link_list.append(new_dict)
        return (
            f"Топ {self.count_max} фотография с самым большим размером : \n {self.link_list} \n"
            f"ВНИМАНИЕ! Если ваши фотографии на профиле меньше чем вы указали в параметрах, то програма выводит только фотографии, которые у вас есть. \n"
        )
    def Yandex_upload(self, file_path, token=TOKEN_YANDEX):
        HEADERS = {"Authorization": f"OAuth {token}"}
        DOWNLOAD_LINK = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        return_list = []
        print("Прогресс в процессе, подождите!")
        with alive_bar(len(self.link_list)) as bar:
            for links in self.link_list:
                bar()
                time.sleep(1)
                photo_links = links["наибольший размер"]["url"]
                photo_types = links["Тип"]
                result = requests.post(
                    DOWNLOAD_LINK,
                    headers=HEADERS,
                    params={
                        "url": photo_links,
                        "disable_redirects": False,
                        "path": f"/{file_path}/{self.count_like}.jpeg",
                    },
                )
                return_dict = {
                    "Имя файла": f"{self.count_like}.jpeg",
                    "Тип фото": photo_types,
                }
                return_list.append(return_dict)
            if result.status_code == 202:
                return f"Всё  прошло успешно! Код: {result.status_code} \n Список фотографий загруженных на Диск: \n {return_list}"
            else:
                return f"ошибка! Код: {result.status_code} \n {result.json()}"
first_user = User(TOKEN, V, 5, User_ID)
print(first_user.get_photos())
print(first_user.Yandex_upload("здесь имя папки которой мы хотим сохранить на диске"))
