
# Удаление своих лайков во ВКонтакте

## Где найти материалы, отмеченные моими реакциями?

> Для получения списка материалов в VK API нет метода, поэтому только такой способ

* Перейдите в раздел [Новости](https://vk.com/feed) в левом меню
* Нажмите на пункт [Реакции](https://vk.com/feed?section=likes) в списке справа
  
![news](https://sun7-23.userapi.com/impg/YssQUiwLCFeS9d1Qy0MxjsYO2mumTlIX0QV-Zg/yAeL2KIz-VU.jpg?size=604x389&quality=96&sign=01f9d7159c266d22761a8d3e92318583&type=album)

* Пролистать как можно ниже
* Открыть консоль разработчика F12 и вставить следующий код для получения ссылок:
```
const items = document.querySelectorAll(".PostHeaderSubtitle__link,.post_link");
const data = [];
items.forEach(item => {
    data.push(item.getAttribute("href"));
});
JSON.stringify(data)
```

* Скопировать результат и вставить в input.json
* Запустить код
```
python3 main.py
```
* Повторять до тех пор, пока реакции не исчезнут

## Установка пакетов
```
pip3 install -r requirements.txt
```
