from random import choice
from datacenter.models import Mark, Chastisement, Commendation, Lesson, \
    Schoolkid


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
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    if bad_marks:
        print(f'Найденных плохих оценок: {len(bad_marks)}')
    else:
        print('Не нашёл плохих оценок у этого ученика, всё чисто ;)')
        return
    for mark in (2, 3):
        good_mark = mark + 2
        corrections = Mark.objects.filter(schoolkid=schoolkid,
                                          points=mark).update(points=good_mark)
        print(f'Исправил {corrections} оценок "{mark}" на "{good_mark}"')


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


def find_schoolkid(fullname):
    """Ищет ученика по фамилии, имени, отчеству, или по некоторым из них"""
    fullname = fullname.strip()
    while '  ' in fullname:
        fullname = fullname.replace('  ', ' ')
    names = fullname.split(' ')
    names = tuple(name.capitalize() for name in names)
    if any(Schoolkid.objects.filter(full_name__contains=name)
           for name in names):
        found_schoolkids = Schoolkid.objects.all()
        for name in names:
            if found_schoolkids.filter(full_name__contains=name):
                found_schoolkids = \
                    found_schoolkids.filter(full_name__contains=name)
    else:
        found_schoolkids = ()
    if not found_schoolkids:
        print(f'Не нашёл ни одного ученика с полным именем {fullname}.')
        partial_matches = tuple(
            Schoolkid.objects.filter(full_name__contains=name) for
            name in names if Schoolkid.objects.filter(full_name__contains=name)
        )
        if any(partial_matches):
            print('Возможно, ошибка в данных. Нашёл частичные совпадения:')
            for match in partial_matches:
                print(*match, sep='\n')
        else:
            print('Не нашёл совпадений по таким данным')
        print('Запусти скрипт заново с правильными именами')
        return
    if len(found_schoolkids) > 1:
        print('Нашёл несколько учеников с такими данными:')
        print(*found_schoolkids, sep='\n')
        print('Запусти скрипт заново с правильными именами')
        return
    else:
        print(f'Нашёл ученика: {found_schoolkids[0]}')
        return found_schoolkids[0]
