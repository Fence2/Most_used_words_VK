from prettytable import PrettyTable


def create_table(obj: [list, dict]) -> PrettyTable:
    """
    Создаёт таблицу из 1 словаря.

    :param obj: список с 1 словарем, либо сам словарь
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


def create_tables(objects: list) -> list[PrettyTable]:
    """
    Создаёт список таблиц из списка словарей

    :param objects: список словарей
    :return: список объектов класса PrettyTable, модуля prettytable
    """

    return [create_table(obj) for obj in objects]


def print_conversations(conversations: list[dict], sortByName=False, sortByTotal=True):
    """
    Выводит список бесед в виде красивой таблицы в консоль.

    Список отсортирован по типам: user -> chat -> group.

    :param conversations: Список бесед для вывода в консоль
    :param sort: Сортировка в лексикографическом порядке (не влияет на сортировку по типам)
    """

    table = PrettyTable()
    table.field_names = ["Имя/название", "Тип", "ID", "Всего"]
    users = list(filter(lambda c: c["type"] == "user", conversations))
    chats = list(filter(lambda c: c["type"] == "chat", conversations))
    groups = list(filter(lambda c: c["type"] == "group", conversations))
    if sortByName or sortByTotal:
        users.sort(key=lambda i: (i["total"] if sortByTotal else 0, i["name"] if sortByName else 0), reverse=True if sortByTotal else False)
        chats.sort(key=lambda i: (i["total"] if sortByTotal else 0, i["name"] if sortByName else 0), reverse=True if sortByTotal else False)
        groups.sort(key=lambda i: (i["total"] if sortByTotal else 0, i["name"] if sortByName else 0), reverse=True if sortByTotal else False)
    for conv in users + chats + groups:
        table.add_row([conv["name"], conv["type"], conv["id"], conv["total"]])
    print(table)
