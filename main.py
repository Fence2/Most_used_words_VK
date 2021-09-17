import vk_api
from prettytable import PrettyTable
from tqdm import tqdm

import settings

vk = vk_api.VkApi(token=settings.token).get_api()


def cut_dict(dictionary: dict, keys: list):
    return {k: v for k, v in dictionary.items() if k in keys}


def create_table(obj: [list, dict]):
    """
    Создаёт объект класса PrettyTable, модуля prettytable из 1 словаря.

    :param obj: лист с 1 словарём, либо сам словарь
    :return: объект класса PrettyTable, модуля prettytable
    """

    if type(obj) == list and len(obj) == 1:
        obj = obj[0]
    if type(obj) == dict:
        table = PrettyTable()
        table.field_names = ["Поле", "Значение"]
        for field, value in obj.items():
            table.add_row([field, value])
        return table


def create_tables(objects: list):
    """
    Создаёт список объектов класса PrettyTable, модуля prettytable из списка словарей

    :param objects: список словарей
    """

    return [create_table(obj) for obj in objects]


def get_conversations(print_data=False):
    conversations = list()
    conv_obj = vk.messages.getConversations()
    for conv in tqdm(conv_obj["items"], desc="Загрузка бесед", colour="blue"):
        conv = cut_dict(conv["conversation"]["peer"], ["type", "local_id"])
        id, type = conv['local_id'], conv['type']
        for k, v in get_chat_info(id, type).items():
            conv[k] = v
        del conv["local_id"]
        conversations.append(conv)

    if print_data:
        table = PrettyTable()
        table.field_names = ["Имя/название", "Тип", "ID"]
        users = list(filter(lambda c: c["type"] == "user", conversations))
        chats = list(filter(lambda c: c["type"] == "chat", conversations))
        groups = list(filter(lambda c: c["type"] == "group", conversations))
        for conv in users + chats + groups:
            table.add_row([conv["name"], conv["type"], conv["id"]])
        print(table)

    return conversations


def get_chat_info(id: int, type="user"):
    if type == "user":
        chat = cut_dict(vk.users.get(user_ids=id)[0], ["first_name", "last_name", "id"])
        chat["name"] = f'{chat["first_name"]} {chat["last_name"]}'
        del chat["first_name"]
        del chat["last_name"]
        return chat
    elif type == "chat":
        chat = cut_dict(vk.messages.getChat(chat_id=id), ["title", "id"])
        chat["name"] = chat["title"]
        del chat["title"]
        return chat
    elif type == "group":
        return cut_dict(vk.groups.getById(group_ids=id)[0], ["name", "id"])


get_conversations(print_data=True)
