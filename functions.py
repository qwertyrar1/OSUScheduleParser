from db_connect import get_group_number
from parse import parser, parser_all_day

lessons_time = ['08:00-09:30', '09:40-11:10', '11:20-12:50', '13:20-14:50', '15:00-16:30', '16:40-18:10']


def get_text_select_day(faculty, group_class, group_name, select_day):
    group_num = get_group_number(faculty, group_class, group_name)
    url = f'https://www.osu.ru/pages/schedule/?who=1&what=1&filial=1&group={group_num}&mode=full'
    timetable = parser(url, select_day)
    for i in range(len(timetable)):
        if timetable[i][:7] == 'Общефиз':
            for j in range(3):
                timetable.remove(timetable[i + 1])
            break
    for i in range(len(timetable)):
        if timetable[i][:6] == ' Ин.яз':
            for j in range(2):
                timetable.remove(timetable[i])
            break
    for i in range(len(timetable)):
        if i == 0:
            continue
        timetable[i] = f'{i} пара({lessons_time[i - 1]}):{timetable[i]}'
    return timetable


def get_text_all_day(faculty, group_class, group_name):
    group_num = get_group_number(faculty, group_class, group_name)
    url = f'https://www.osu.ru/pages/schedule/?who=1&what=1&filial=1&group={group_num}&mode=full'
    schedule_all_day = list(map(lambda x: x, parser_all_day(url)))
    for timetable in schedule_all_day:
        for i in range(len(timetable)):
            if timetable[i][:7] == 'Общефиз':
                for j in range(3):
                    timetable.remove(timetable[i + 1])
                break
        for i in range(len(timetable)):
            if timetable[i][:6] == ' Ин.яз':
                for j in range(2):
                    timetable.remove(timetable[i])
                break
        for i in range(len(timetable)):
            if i == 0:
                continue
            timetable[i] = f'{i} пара({lessons_time[i - 1]}):{timetable[i]}'
    one_week_array = []
    all_week_array = []
    for i in range(len(schedule_all_day)):
        if schedule_all_day[i] and schedule_all_day[i][0][11:-1] != 'воскресенье':
            one_week_array.append(schedule_all_day[i])
        elif schedule_all_day[i] and schedule_all_day[i][0][11:-1] == 'воскресенье':
            all_week_array.append(one_week_array)
            one_week_array = []

    return all_week_array
