from tqdm import tqdm
from vk_api import VkApi

import settings

vk = VkApi(token=settings.token).get_api()


def crop_dict(dictionary: dict, keys: list) -> dict:
    """
    Функция обрезает словарь, оставляя только определённые ключи из списка keys.

    :param dictionary: Словарь, который нужно изменить
    :param keys: Ключи, которые нужно оставить
    """
    return {k: v for k, v in dictionary.items() if k in keys}


def get_conversations() -> list[dict]:
    """
    Функция получает и возвращает отредактированный список бесед пользователя.

    Изменения:
    -Удалены неиспользуемые программой поля.
    -У всех бесед есть ключ "name", независимо от типа беседы.
    -При view == "Console" в консоли будет показан progress-bar получения данных с серверов VK.
    """

    def crop_conv(conv) -> dict:
        """
        Основная функциональность функции get_conversations.
        """
        conv = crop_dict(conv["conversation"]["peer"], ["type", "local_id"])
        id, type = conv['local_id'], conv['type']
        for k, v in get_chat_info(id, type).items():
            conv[k] = v
        del conv["local_id"]
        return conv

    conversations = list()
    raw_conversations = vk.messages.getConversations()

    # View
    if settings.view == "Console":
        for conv in tqdm(raw_conversations["items"], desc="Загрузка бесед", colour="blue"):
            conversations.append(crop_conv(conv))
    else:
        for conv in raw_conversations:
            conversations.append(crop_conv(conv))

    return conversations


def get_chat_info(id: int, type="user") -> dict:
    """
    Функция возвращает информацию о беседе в виде словаря двух ключей: name, id

    :param id: идентификатор беседы, информацию о которой нужно получить
    :param type: тип беседы (user, chat, group)
    """

    if type == "user":
        chat = crop_dict(vk.users.get(user_ids=id)[0], ["first_name", "last_name", "id"])
        chat["name"] = f'{chat["first_name"]} {chat["last_name"]}'
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
