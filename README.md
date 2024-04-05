# Dvmn-E-diary-fixer
Исправление оценок в электронном дневнике

# Описание функционала
* ищет учеников в базе данных
* исправляет оценки 2, 3 на 4, 5
* удаляет все замечания
* добавляет похвалу

# Установка
Для использования положи файл `scripts.py` в ту же директорию, где находится `manage.py`

# Использование функций и примеры работы
## 1. Запусти django shell:
```
python manage.py shell
```

## 2. Импортируй функции скрипта:
```
from scripts import find_schoolkid, create_commendation, fix_marks, remove_chastisements
```

## 3. Найди нужного ученика
**Функция находит ученика с заданными именами (можно любые из: фамилия, имя, отчество через пробел)**
Этот шаг не обязателен, функции скрипта можно запускать сразу с именем ученика. Но если сперва найти ученика, избежать ошибок будет проще. Ты же не хочешь незаслуженно исправить оценки своему однофамильцу? ;)
```
child = find_schoolkid('Иванов')
Нашёл несколько учеников с такими данными:
Бурова Лукия Ивановна 3А
Иванов Гордей Трофимович 3А
Вишнякова Анастасия Ивановна 4А
Иванов Август Аксёнович 5Б
Иванов Демьян Брониславович 5В
Юдина Екатерина Ивановна 6А
Иванова Нинель Сергеевна 6В
Маркова Прасковья Ивановна 7А
Иванова Алина Аскольдовна 9Б
Герасимова Анастасия Ивановна 10А
Горшкова Прасковья Ивановна 10Б
Запусти скрипт заново с правильными именами
```
Скрипт нашёл всех учеников, у которых в полном имени (фамилия имя отчество) есть слово "Иванов". Так не пойдёт, нам нужно уточнять ФИО, пока скрипт не найдёт единственного ученика с таким полным именем.
```
child = find_schoolkid('Иванов Демьян') 
Нашёл ученика: Иванов Демьян Брониславович 5В
```
## 4. Теперь, когда правильный ученик находится в переменной `child`, можно приступить к улучшению его успеваемости.
### Исправить оценки 2, 3 на 4, 5.
**Функция исправляет все оценки 2 и 3 на 4 и 5.**

Возьмём ученицу похуже - с двойками, с замечаниями и без похвал.
```
child = find_schoolkid('Авдеева Элеонора')
Нашёл ученика: Авдеева Элеонора Анатольевна 5В
```

Было:

![image](https://github.com/vdesyatke/Dvmn-E-diary-fixer/assets/72273263/a252ce55-7c8b-442a-9398-8578aeb8b315)

Запускаем магию:
```
fix_marks(child)
Найденных плохих оценок: 266
Исправил оценку 5 Авдеева Элеонора Анатольевна
Исправил оценку 4 Авдеева Элеонора Анатольевна
...
Исправил оценку 5 Авдеева Элеонора Анатольевна
```
Стало: 
![image](https://github.com/vdesyatke/Dvmn-E-diary-fixer/assets/72273263/0ecdd5e0-0fa6-4dd0-8d30-ffba7aef0fd4)
Двойки и тройки исправились на четвёрки и пятёрки. Успех!

### Удалить замечания
**Функция удаляет все замечания ученика**.

А у Элеоноры их целый букет:
![image](https://github.com/vdesyatke/Dvmn-E-diary-fixer/assets/72273263/8e0fd01f-1994-4cc4-9aea-4b18aa7219c9)
Исправляем:
```
remove_chastisements(child)
Найденных жалоб: 10
Удалил жалобу
...
Удалил жалобу
Удалил жалобу
```
Стало:
![image](https://github.com/vdesyatke/Dvmn-E-diary-fixer/assets/72273263/f70b464c-11dc-49d5-89ac-1cf90ec3cf98)

### Добавить похвалы
**Функция добавляет одну похвалу за один запуск. Урок выбирается рандомно. Можно запускать сколько угодно раз повторно. 
Похвала выбирается случайно из списка:**
_Молодец! Отлично! Хорошо! Гораздо лучше! Великолепно! Прекрасно! Сказано здорово – просто и ясно! Точно! Очень хороший ответ! Талантливо! Уже существенно лучше! Потрясающе! Замечательно! Прекрасное начало! Так держать! Ты на верном пути! Здорово! Это как раз то, что нужно! Я тобой горжусь! С каждым разом у тебя получается всё лучше! Мы с тобой не зря поработали! Я вижу, как ты стараешься! Ты растешь над собой! Теперь у тебя точно все получится!_
Было: 
![image](https://github.com/vdesyatke/Dvmn-E-diary-fixer/assets/72273263/f70b464c-11dc-49d5-89ac-1cf90ec3cf98)
Команда:
```
create_commendation(child)
Создал похвалу для этого ученика на уроке Технология 5В, 2018-10-23
```
Можно создать похвалу на конкретном предмете:
```
create_commendation(child, 'Математика') 
Создал похвалу для этого ученика на уроке Математика 6А, 2018-10-29
```

## 5. Что это за проект?
