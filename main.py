from vk_manager  import VKLikesManager
def main() -> None:
    """
    Главная функция для выбора типа объекта и запуска процесса удаления лайков.
    """
    print("Выберите тип объекта для удаления лайков:")
    print("1. post — запись на стене пользователя или группы")
    print("2. story — история")
    print("3. comment — комментарий к записи на стене")
    print("4. photo — фотография")
    print("5. audio — аудиозапись")
    print("6. video — видеозапись")
    print("7. market — товар")

    choice = input("Введите номер выбора: ")
    type_remove = {
        "1": "post",
        "2": "story",
        "3": "comment",
        "4": "photo",
        "5": "audio",
        "6": "video",
        "7": "market",
    }.get(choice, "post")

    vk_manager = VKLikesManager("input.json", type_remove)
    vk_manager.process_likes()


if __name__ == "__main__":
    main()
