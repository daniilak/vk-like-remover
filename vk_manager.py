import os
import json
import requests
import urllib
from base64 import b64encode
import os
from time import sleep
from dotenv import load_dotenv
from captcha_solver import CaptchaSolver

load_dotenv()

VK_TOKEN = os.getenv("VK_TOKEN")


class VKLikesManager:
    """
    Класс для управления лайками в VK.
    """

    def __init__(self) -> None:
        """
        Инициализация VKLikesManager.
        """

        try:
            with open("input.json", "r") as f:
                filedata = f.read()
        except Exception as e:
            print(e)
            exit()

        if not filedata:
            exit("Файл пустой")

        if filedata[0] == "'":
            filedata = filedata[1:-1]
        try:
            self.data = list(set(json.loads(filedata)))
        except Exception as e:
            print(e)
            exit()

        self.len_data = len(self.data)
        print(f"Всего {self.len_data} шт")

    def check_captcha(self, response: dict) -> tuple:
        """
        Проверка на наличие капчи в ответе.

        :param response: Ответ от VK API.
        :return: URL изображения капчи и идентификатор капчи.
        """
        if "error" in response:
            if response["error"]["error_code"] == 14:
                captcha_sid = response["error"]["captcha_sid"]
                captcha_img = response["error"]["captcha_img"]
                return captcha_img, captcha_sid
        return None, None

    @staticmethod
    def get_base64_image(captcha_img: str) -> str:
        """
        Получение изображения капчи в формате base64.

        :param captcha_img: URL изображения капчи.
        :return: Изображение капчи в формате base64.
        """
        with urllib.request.urlopen(captcha_img) as response:
            image_data = response.read()

        return b64encode(image_data).decode("ascii")

    def request_vk(
        self,
        owner_id: str,
        post_id: str,
        type_remove: str,
        captcha_sid: str = "",
        captcha_key: str = "",
    ) -> dict:
        """
        Отправка запроса на удаление лайка в VK.

        :param owner_id: ID владельца.
        :param post_id: ID элемента.
        :param captcha_sid: Идентификатор капчи.
        :param captcha_key: Ключ капчи.
        :return: Ответ от VK API.
        """
        data = {
            "access_token": VK_TOKEN,
            "type": type_remove,
            "owner_id": owner_id,
            "item_id": post_id,
            "v": 5.236,
        }
        if captcha_key:
            data["captcha_key"] = captcha_key
        if captcha_sid:
            data["captcha_sid"] = captcha_sid

        response = requests.post("https://api.vk.com/method/likes.delete", data=data)
        return response.json()

    def remove(self, owner_id: str, post_id: str, type_remove: str) -> bool:
        """
        Удаление лайка с элемента.

        :param owner_id: ID владельца.
        :param post_id: ID элемента.
        :return: Успешность операции.
        """
        try:
            response = self.request_vk(owner_id, post_id, type_remove)
        except Exception as e:
            return False

        captcha_img, captcha_sid = self.check_captcha(response)
        if captcha_img and captcha_sid:
            print("Капча")
            c = CaptchaSolver(self.get_base64_image(captcha_img))
            c.create_tasks()
            captcha_key = c.wait_for_captcha()
            response = self.request_vk(
                owner_id, post_id, type_remove, captcha_sid, captcha_key
            )

        return True

    def process_likes(self) -> None:
        """
        Обработка всех лайков из списка данных. Ограничение 3 запроса в секунду. Не рекомендую использовать паралелльные запросы.
        """
        for index, item in enumerate(self.data):
            print(f"Обработка материала №{index+1} из {self.len_data} ")
            if "?reply" in item:
                item = item.replace("https://vk.com/wall", "")
                owner_id, item_id = item.split("_")
                item_id = item_id.split("?reply=")[1]
                type_remove = "comment"
            elif "/video" in item:
                owner_id, item_id = item.replace("/video", "").split("_")
                type_remove = "video"
            elif "/wall" in item:
                owner_id, item_id = item.replace("/wall", "").split("_")
                type_remove = "post"
            elif "/market" in item:
                "/market-223730782?w=product-223730782_9205234"
                owner_id, item_id = item.split("product")[1].split("_")
            else:
                continue
            self.remove(owner_id, item_id, type_remove)
            sleep(0.3)
