import json
import os

from tqdm import tqdm
from vk_api import VkApi

import modules.settings as settings

vk = VkApi(token=settings.token).get_api()

MY_ID = vk.users.get()[0]["id"]


# DONE
def crop_dict(dictionary: dict, keys: list) -> dict:
    """
    Функция обрезает словарь, оставляя только определённые ключи из списка keys.

    :param dictionary: Словарь, который нужно изменить
    :param keys: Ключи, которые нужно оставить
    """
    return {k: v for k, v in dictionary.items() if k in keys}


# ALMOST DONE
def get_20conversations() -> list[dict]:
    """
    Функция получает и возвращает отредактированный список 20 бесед пользователя.

    Изменения:
    -Удалены неиспользуемые программой поля.
    -У всех бесед есть ключ "name", независимо от типа беседы.
    -При view == "Console" в консоли будет показан progress-bar получения данных с серверов VK.
    """

    conversations = list()
    raw_conversations = vk.messages.getConversations()

    # View
    if settings.view == "Console":
        print(f"Всего бесед: {raw_conversations['count']}")
        raw_conversations = tqdm(raw_conversations["items"], desc="Загрузка бесед", colour="blue")
    else:
        raw_conversations = raw_conversations["items"]

    for conv in raw_conversations:
        conv = crop_dict(conv["conversation"]["peer"], ["type", "local_id"])
        id, type = conv['local_id'], conv['type']
        for k, v in get_chat_info(id, type).items():
            conv[k] = v
        del conv["local_id"]

        conversations.append(conv)

    return conversations


# ALMOST DONE
def get_conversations_from_file(file_path=f"data/{MY_ID}_conversations_ids.txt", rewrite=False):
    """
    Функция создаёт json файл со всеми ID и названиями бесед из файла со списком этих ID.

    Если json файл данного пользователя уже существует - загружает его.

    :param file_path: Путь к файлу, в котором на каждой строке указан ID беседы
    :param rewrite: Нужно ли перезаписать json файл?
    :return: список словарей, где каждый словарь - отдельная беседа с ключами type, id, name
    """

    conversations = list()
    if os.path.exists(f"data/{MY_ID}_conversations_FULL.json") and not rewrite:
        with open(f"data/{MY_ID}_conversations_FULL.json", encoding="utf-8") as file:
            conversations = json.load(file)
            if settings.view == "Console":
                print(f"Всего бесед: {len(conversations)}")
                for _ in tqdm(conversations, desc="Загрузка бесед", colour="blue"):
                    pass
    else:
        with open(file_path) as file:
            ids = [int(line.strip()) for line in file if line.strip().replace("-", "").isdigit()]
            if settings.view == "Console":
                print(f"Всего бесед: {len(ids)}")
                ids = tqdm(ids, desc="Загрузка бесед", colour="blue")
            for id in ids:
                type = "user"
                if id >= 2_000_000_000:
                    id = id % 10000
                    type = "chat"
                elif id < 0:
                    id = -id
                    type = "group"
                chat_info = {"type": type}
                for k, v in get_chat_info(id, type).items():
                    chat_info[k] = v
                conversations.append(chat_info)
        with open(f"data/{MY_ID}_conversations_FULL.json", "w", encoding="utf-8") as file:
            json.dump(conversations, file, ensure_ascii=False)

    return conversations


# DONE
def get_chat_info(id: int, type="user") -> dict:
    """
    Функция возвращает информацию о беседе в виде словаря двух ключей: name, id

    :param id: идентификатор беседы, информацию о которой нужно получить
    :param type: тип беседы (user, chat, group)
    """

    if type == "user":
        chat = crop_dict(vk.users.get(user_ids=id)[0], ["first_name", "last_name", "id"])
        chat["name"] = f'{chat["first_name"]}{" " if chat["last_name"] else ""}{chat["last_name"]}'
        del chat["first_name"]
        del chat["last_name"]
        return chat

    elif type == "chat":
        chat = crop_dict(vk.messages.getChat(chat_id=id), ["title", "id"])
        chat["name"] = chat["title"]
        del chat["title"]
        return chat

    elif type == "group":
        return crop_dict(vk.groups.getById(group_ids=id)[0], ["name", "id"])
