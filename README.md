# Космическая битва
В далекой звездной системе встретились две флотилии космических кораблей.
Корабли могут передвигаться по всему пространству звездной системы по прямой, поворачиваться против и по часовой стрелке, стрелять фотонными торпедами. 
Попадание фотонной торпеды в корабль выводит его из строя.
От каждой флотилии в сражении принимают участие по три космических корабля.
Победу в битве одерживает та флотилия, которая первой выведет из строя все корабли соперника.


Формат сообщений:
```json
{
  "user_id": 1, // Парситься всегда
  "token": "str", // Парситься всегда, кроме action get_token
  "game_id": "str",  // id игры. Задает клиент, что бы можно было по нему обращаться в дальнейшем
  "action": "str",  //  Действие. Всего 3 варианта [register_game, start_game, execute_command]
  "command_name": "str", // Парсится только в случае указания execute_command
  "user_ids": [1, 2, 3], // Парсится только в случае регистрации игры
  "objects": [     // Парсится только в случание register_game
    {
      "position": [12, 5],
      "velocity": [-7, 3],
      "fuel_level": 100,
      "required_fuel_level": 10,
      "direction": 100,
      "angular_velocity": 30,
      "direction_number": 360
    }
  ],
  "object_id": "str" // Парсится только в случае указания execute_command
}
```

# Диаграмма взаимодействия сервисов:

![services.png](services.png)![](/home/gideon/projects/otus-spacebattle/services.png)

## Техническое описание задания:
При создании данного проекта был сделан упор на соблюдение принципов SOLID, в особенности принцип 
подстановки Барбары Лисков(`LSP`), принцип открытости-закрытости(`OCP`) и принцип инверсии зависимостей(`DIP`).
Для реализации и соблюдения принципов были применены следующие паттерны:
 * Команда (`Command`)
 * Стратегия (`Strategy`)
 * Абстрактная фабрика (`Abstract Factory`)
 * Шаблонный метод (`Template Method`)
 * Декоратор (`Decorator`)
 * Инверсия управления (`IoC`)
 * Репозиторий (`Repository`)
 * Конвейер (`Pipeline`) или Производитель-Потребитель (`Producer-Consumer`), **смотря с какой стороны посмотреть**

## Проблемы и узкие места:
 * При сетевом сбое отсутствует система повторов (`retry`) сообщений
 * Игровые сессии не сохраняются. В случае сбоя питания или перезагрузки сервера данные будут утеряны.

## Компоненты, которым чаще всего будут меняться:
 * Команды. Но поскольку весь проект построен на принципе `DI`, проблем с добавлением и\или изменений команд быть не должно.
 * Броккер сообщений. `RabbitMQ` можно заменить на что угодно. Включая переписать с очередей на REST API. Но используя интерфейс работника (`BaseWorker`) мы легко можем изменить эту часть системы.
 * База данных для хранения информации для пользователя. В проекте все взаимодействия с базой данных идет через интерфейс паттерна репозиторий (`BaseRepository`). Замена на любую другую базу должна быть безболезненной.