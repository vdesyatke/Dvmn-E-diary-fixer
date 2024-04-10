from random import choice
from datacenter.models import Mark, Chastisement, Commendation, Lesson, \
    Schoolkid
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import F


COMMENDATIONS = ('Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше!',
                 'Великолепно!', 'Прекрасно!',
                 'Сказано здорово – просто и ясно!',
                 'Точно!', 'Очень хороший ответ!', 'Талантливо!',
                 'Уже существенно лучше!', 'Потрясающе!', 'Замечательно!',
                 'Прекрасное начало!', 'Так держать!',
                 'Ты на верном пути!',
                 'Здорово!', 'Это как раз то, что нужно!',
                 'Я тобой горжусь!',
                 'С каждым разом у тебя получается всё лучше!',
                 'Мы с тобой не зря поработали!',
                 'Я вижу, как ты стараешься!', 'Ты растешь над собой!',
                 'Теперь у тебя точно все получится!')


def fix_marks(schoolkid):
    corrections = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).\
        update(points=F('points') + 2)
    print(f'Исправил {corrections} оценок')


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    if chastisements:
        print(f'Найденных жалоб: {len(chastisements)}')
    else:
        print('Не нашёл жалоб на этого ученика, всё чисто ;)')
        return
    deletions = chastisements.delete()[0]
    print(f'Количество удалённых жалоб: {deletions} ')


def add_commendation(schoolkid, subject=None):
    text = choice(COMMENDATIONS)
    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
    )
    if subject:
        if lessons.filter(subject__title=subject):
            lessons = lessons.filter(subject__title=subject)
        else:
            print('Не нашёл ни одного предмета с таким названием. '
                  'Есть предметы:')
            subjects = lessons.values_list('subject__title',
                                           flat=True).distinct()
            print(*subjects, sep=', ')
            print('Запусти скрипт заново с правильным названием предмета')
            return
    lesson = lessons.order_by('?').first()
    Commendation.objects.create(
        text=text,
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher,
    )
    print(f'Создал похвалу для этого ученика на уроке {lesson}, {lesson.date}')


def find_schoolkid(full_name):
    """Ищет ученика по фамилии, имени, отчеству, или по некоторым из них"""
    full_name = full_name.strip()
    while '  ' in full_name:
        full_name = full_name.replace('  ', ' ')
    names = full_name.split(' ')
    names = tuple(name.capitalize() for name in names)
    full_name = ' '.join(names)

    try:
        return Schoolkid.objects.get(full_name=full_name)
    except ObjectDoesNotExist:
        print('Ученик с таким именем не найден')
    except MultipleObjectsReturned:
        print('Найдено несколько учеников с такими данными')
