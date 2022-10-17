from source.database import SessionLocal, Base, engine
from source.models import Tnved1, Tnved2, Tnved3, Tnved4
import re
from unicodedata import normalize
from datetime import datetime
import os


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

    return collect_data


def get_element_list(tnved_num: int):
    """

    :param tnved_num: Передаем номер текстового файл ТНВЭД на вход
    :return: Возвращаем готовый список с элементами таблицы
    """
    with open(f'Data/TNVED{tnved_num}_utf-8.txt', "r", encoding='utf-8') as file:
        raw_text = file.readlines()
        element_list = process_full_text(raw_text)

    return element_list


def process_date(input_date: str) -> datetime.date:
    if input_date is None:
        return None

    processed_date = datetime.strptime(input_date, '%d.%m.%Y').date()

    return processed_date


def get_parent_id(base_num: int, *args) -> int:
    temp_session = SessionLocal()

    if base_num == 2:
        if args[-1] is None:
            query_result = (temp_session.query(Tnved1)
                            .filter(Tnved1.section == args[0])
                            .filter(Tnved1.start_date == args[1])
                            .one())
        else:
            print(args)
            query_result = (temp_session.query(Tnved1)
                            .filter(Tnved1.section == args[0])
                            .filter(Tnved1.start_date <= args[1])
                            .filter(Tnved1.finish_date >= args[2])
                            .one())

    elif base_num == 3:
        if args[-1] is None:

            query_result = (temp_session.query(Tnved2)
                            .filter(Tnved2.group == args[0])
                            .filter(Tnved2.start_date == args[1])
                            .one())
        else:
            try:
                query_result = (temp_session.query(Tnved2)
                                .filter(Tnved2.group == args[0])
                                .filter(Tnved2.start_date <= args[1])
                                .filter(Tnved2.finish_date >= args[2])
                                .one())
            except:
                # Обработка случаев, когда даты дочерних кодов "разрывают" даты действия родительских кодов.
                # Изучение этих случаев требует более глубокое погружение в предметную область.
                query_result = None

    elif base_num == 4:
        if args[-1] is None:
            try:
                query_result = (temp_session.query(Tnved3)
                                .filter(Tnved3.group == args[0])
                                .filter(Tnved3.position == args[1])
                                .filter(Tnved3.start_date == args[2])
                                .one())
            except:
                query_result = None

        else:
            try:
                query_result = (temp_session.query(Tnved3)
                                .filter(Tnved3.group == args[0])
                                .filter(Tnved3.position == args[1])
                                .filter(Tnved3.start_date_date <= args[2])
                                .filter(Tnved3.finish_date >= args[3])
                                .one())
            except:
                query_result = None

    if query_result is None:
        return None
    parent_id = query_result.id
    temp_session.commit()
    temp_session.close()
    return parent_id


def execute(base_num):
    session = SessionLocal()
    tnved_list = get_element_list(base_num)

    for element in tnved_list:
        print(element)
        if base_num == 1:
            section, name, comment, start_date, finish_date = element
            tnved = Tnved1(section=section,
                           name=name,
                           comment=comment,
                           start_date=start_date,
                           finish_date=finish_date
                           )
        elif base_num == 2:
            section, group, name, comment, start_date, finish_date = element
            parent_id = get_parent_id(base_num, section, process_date(start_date), process_date(finish_date))

            tnved = Tnved2(parent_id=parent_id,
                           section=section,
                           group=group,
                           name=name,
                           comment=comment,
                           start_date=start_date,
                           finish_date=finish_date
                           )
        elif base_num == 3:
            group, position, name, start_date, finish_date = element
            parent_id = get_parent_id(base_num, group, process_date(start_date), process_date(finish_date))
            tnved = Tnved3(parent_id=parent_id,
                           group=group,
                           position=position,
                           name=name,
                           start_date=start_date,
                           finish_date=finish_date
                           )

        elif base_num == 4:

            group, position, sub_position, short_name, start_date, finish_date = element
            parent_id = get_parent_id(base_num, group, position, process_date(start_date), process_date(finish_date))
            tnved = Tnved4(parent_id=parent_id,
                           group=group,
                           position=position,
                           sub_position=sub_position,
                           short_name=short_name,
                           start_date=start_date,
                           finish_date=finish_date
                           )
        session.add(tnved)
    session.commit()
    session.close()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    make_readable()
    [execute(base_num=i) for i in range(1, 5)]
