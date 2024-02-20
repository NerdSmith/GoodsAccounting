# Техническое задание. 
В компании Рога и Копыта организовано хранение информации о заполненности склада товарами для офиса в виде таблицы csv. Менеджер, заполнявший ее, пролил кофе на клавиатуру, и таблица осталась только в распечатанном виде.

Было принято решение, внедрить учет продуктов на внутренний портал организации.

Требуется реализовать web приложение для управления запасом кофе и печенья в офисе. Структуру хранения информации следует выбрать с учетом того что:  
* Есть несколько мест для хранения запасов, различающиеся по максимальному весу товара;  
* Несколько сотрудников пополняющих и забирающих с полки товар;  
* Ассортимент может произвольно пополняться. Данные следует хранить в реляционной базе данных. Таблицы синхронизировать через механизм миграций. Данные с распечатанной таблицы следует перед запуском сервиса добавить в виде миграций к вновь созданной БД. Взаимодействие с порталом осуществляется по REST API. Для проверки работоспособности требуется API UI. 
* Для оптимизации работы приложения было принято решение о вынесении расчета суммарного веса товара на полках в отдельный процесс. Требуется реализовать воркер расчета веса товара и взаимодействие с воркером. 
* При выполнении проекта следует использовать FastAPI для реализации API, SQLAlchemy для подключения к базе данных. Готовый проект подготовить к запуску в docker контейнере с обработкой запросов через ASGI веб сервер и подключению к бд. В README.md указать порядок сборки и запуска. Готовый проект ожидаем в виде открытого репозитория на github.  

# Структура проекта    
```
GoodsAccounting  - корень           
├── src  - исходный код
│   ├── utils  - вспомогательные элементы для авторизации, паролей и DI     
│   ├── tasks  - задачи для воркера               
│   ├── services - сервисы, содержащие бизнес логику
│   ├── schemas  - схемы данных для ответов приложения
│   ├── repositories  - репозитории, работающие с бд
│   ├── models  - модели данных (базовые модели и таблицы)
│   ├── db  - модуль для работы с бд          
│   └── api  - модуль роутов    
│       └── v1              
│           └── endpoints  - конечные точки api
├── migrations  - миграции бд          
│   └── versions  - файлы миграций
└── data  - операции для загрузки данных в бд
    └── csv  - таблицы для загрузки в бд
```
# Инструкция для запуска

1. Склонировать проект
    ```
    git clone https://github.com/NerdSmith/GoodsAccounting.git
    ```

2. Перейти в папку "GoodsAccounting"
    ```
    cd SiteNotebook
    ```
3. Установить конфигурационные данные в шаблонных файлах .env, .env.db, .env.mq
4. Переименовать шаблонные .env* файлы, убрав .tmpl  
   
   Windows:
   ```
   ren ".env.prod.tmpl" ".env.prod"
   ren ".env.mq.prod.tmpl" ".env.mq.prod"
   ren ".env.db.prod.tmpl" ".env.db.prod"
   ```
   Linux:
   ```
   mv .env.prod.tmpl .env.prod
   mv .env.mq.prod.tmpl .env.mq.prod
   mv .env.db.prod.tmpl .env.db.prod
   ```
5. Запустить docker-compose.yml
   ```
   docker compose up -d
   ```
6. Готово, сервис должен работать на порту :8000
# API UI
Для просмотра конечных точек перейдите на [Swagger URL](http://localhost:8000/docs)   
P.S.  
Также добавлена JWT авторизация (позволяет получить текущего юзера '/api/v1/users/me')
Для получения Access и Refresh токенов используются '/api/v1/auth/login' и '/api/v1/auth/refresh'
# Операции с моделями
API позволяет работать с моделями в бд
- Создавать, получать текущего пользователя
- CRUD операции с моделью Place, а также получать текущий вес на месте путем подсчета на месте и с помощью воркера
- CRUD операции с моделью Item
- Для добавления товара на полку необходимо обновить поле place_id у item (можно убрать с полки установив в null)
