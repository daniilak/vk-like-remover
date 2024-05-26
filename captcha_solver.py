import os
from requests import Session
from time import sleep
from dotenv import load_dotenv

load_dotenv()

CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY")


class CaptchaSolver:
    """
    Класс для решения капчи с использованием RUCaptcha.

    Атрибуты:
        img_str (str): Изображение капчи в виде строки base64.
        min_length (int): Минимальная длина ответа капчи.
        max_length (int): Максимальная длина ответа капчи.
        session (Session): HTTP сессия для отправки запросов.
        task_id (str): Идентификатор задачи на решение капчи.
    """

    def __init__(self, img_str: str) -> None:
        """
        Инициализация объекта CaptchaSolver.

        :param img_str: Изображение капчи в виде строки base64.
        """
        self.img_str = img_str
        self.min_length = 4
        self.max_length = 7
        self.session = Session()
        self.task_id = self.create_tasks()

    def create_tasks(self) -> str:
        """
        Создание задачи на решение капчи.

        :return: Идентификатор задачи.
        """
        el_json = {
            "key": CAPTCHA_API_KEY,
            "method": "base64",
            "body": self.img_str,
            "min_len": self.min_length,
            "max_len": self.max_length,
            "language": 1,
            "lang": "ru",
            "json": 1,
        }
        task = self.session.post("https://rucaptcha.com/in.php", json=el_json)
        task = task.json()
        if task["status"] != 1:
            print(task)
            exit()
        return task["request"]

    def get_task_result(self) -> dict:
        """
        Получение результата задачи на решение капчи.

        :return: Ответ от сервера в виде JSON.
        """
        url = f"http://rucaptcha.com/res.php?key={CAPTCHA_API_KEY}&action=get&id={self.task_id}&json=1"
        task = self.session.get(url)
        return task.json()

    def wait_for_captcha(self) -> str:
        """
        Ожидание готовности результата капчи.

        :return: Ответ капчи или "CAPTCHA_NOT_READY" если капча не готова.
        """
        for _ in range(3):
            sleep(5)
            result = self.get_task_result()

            if result["request"] != "CAPTCHA_NOT_READY":
                return result["request"]

        return "CAPTCHA_NOT_READY"
