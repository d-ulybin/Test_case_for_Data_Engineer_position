import re

from unicodedata import normalize

from source.database import SessionLocal
from source.models import Tnved1, Tnved2, Tnved3, Tnved4


def make_readable():
    """
    Необязательная функция.
    Преобразует все имеющиеся файлы в /Data в читабельный формат для удобства анализа данных.
    Возможно, есть более оптимальный и быстрый способ перекодирования файлов, но в рамках тестового его достаточно.
    """

    for i in range(1, 5):
        i = str(i)
        with open(f'Data/TNVED{i}.TXT', "r", encoding="cp866") as file_old:
            temp_text = file_old.read()
        with open(f'Data/TNVED{i}_utf-8.txt', 'w', encoding='utf-8') as file_new:
            file_new.write(temp_text)


def process_single_row(input_row: str) -> list:
    """
    Функция обрабатывает одну строку текстового файла, возвращая список с будущими элементами таблицы.
    """

    # Убираем лишние символы в строке
    norm_row = normalize('NFKD', input_row)
    # Убираем лишние пробелы в строке
    final_row = re.sub(r'\s+', ' ', norm_row)
    # Превращаем строку в список и отрезаем пустой конец
    final_row_list = final_row.split('|')
    final_row_list = final_row_list[:-1]
    if final_row_list[-1] == '':
        final_row_list[-1] = None
    return final_row_list


def get_actual_data(input_list: list) -> list:
    """
    Добавил функцию в последний момент, чтобы убрать исторические данные, что в свою очередь решит проблему
    неуникальности ключей.

    :param input_list: Берем общий список списков с элементами таблицы;
    :return: Возвращаем только список, где последний элемент None, то есть классы - актуальные.
    """

    actual_element_list = input_list.copy()

    for raw_element_list in input_list:
        if raw_element_list[-1] is not None:
            actual_element_list.remove(raw_element_list)

    return actual_element_list


def process_full_text(input_full_text: str) -> list:
    """

    :param input_full_text: Принимаем на вход считанный ранее текст;
    :return: Возвращаем список, где каждый элемент является будущей строкой таблицы (списком элементов таблицы);
    :return:
    """

    input_full_text = input_full_text[1:]

    # Список для хранения списков с обработанными строчками
    collect_data = []

    for raw_row in input_full_text:
        row_list = process_single_row(raw_row)
        collect_data.append(row_list)

    final_data = get_actual_data(collect_data)

    return final_data


def get_element_list(tnved_num: int):
    """

    :param tnved_num: Передаем номер текстового файл ТНВЭД на вход
    :return: Возвращаем готовый список с элементами таблицы
    """
    with open(f'Data/TNVED{tnved_num}_utf-8.txt', "r", encoding='utf-8') as file:
        raw_text = file.readlines()
        element_list = process_full_text(raw_text)

    return element_list


if __name__ == "__main__":
    make_readable()

    session = SessionLocal()
    tnved1_list = get_element_list(1)
    for element in tnved1_list:
        section, name, comment, start_date, finish_date = element
        tnved1 = Tnved1(section=section,
                        name=name,
                        comment=comment,
                        start_date=start_date,
                        finish_date=finish_date
                        )
        session.add(tnved1)
    session.commit()

    session = SessionLocal()
    tnved2_list = get_element_list(2)
    for element in tnved2_list:
        section, group, name, comment, start_date, finish_date = element
        tnved2 = Tnved2(section=section,
                        group=group,
                        name=name,
                        comment=comment,
                        start_date=start_date,
                        finish_date=finish_date
                        )
        session.add(tnved2)
    session.commit()

    session = SessionLocal()
    tnved3_list = get_element_list(3)
    for element in tnved3_list:

        group, position, name, start_date, finish_date = element

        tnved3 = Tnved3(group=group,
                        position=position,
                        name=name,
                        start_date=start_date,
                        finish_date=finish_date
                        )
        session.add(tnved3)
    session.commit()

    session = SessionLocal()
    tnved4_list = get_element_list(4)
    for element in tnved4_list:
        temp_element = element.copy()

        group, position, sub_position, short_name, start_date, finish_date = temp_element

        tnved4 = Tnved4(group=group,
                        position=position,
                        sub_position=sub_position,
                        short_name=short_name,
                        start_date=start_date,
                        finish_date=finish_date
                        )
        session.add(tnved4)
    session.commit()
