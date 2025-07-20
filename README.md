# AI Agent with Langflow Backend

Наша вебка состоит из трёх страниц. первая основная, на ней в начале есть приветственный прямоугольник и кнопка перейти к чату с аи агентом, который сам по себе располагается на второй страничке, после на середине первой располагается описание того, что умеет Tatlin  Neauro, вокруг этого фотографии схд татлин ядро, дальше идёт какая-нибудь мотивирующая цитата татлина, после расписаны шаги если не получилось решить вопрос. кому и что писать по пунктом, в подвале вкладка контактов и ссылка на третью страницу с документацией, на которой основывается аи агент. вторая страница это чат с аи агентом, где слева располагается часто задаваемые вопросы. основная идея заключается в том, чтобы снизить нагрузку на техническую поддержку, так как в неё сейчас обращаются и те, кому действительно нужна помощь и те, кому лень изучать документацию самостоятельно, тем самым среднее время решение проблемы снижается

**Структура:**
project/
├── agent/ (Streamlit)
│ ├── Dockerfile, main.py, Page_3.py, requirements.txt
├── langflow/ (сервер)
│ ├── Dockerfile, flows/Agent.json, data/
├── docker-compose.yml
└── .env


**Запуск:**
A:
`uv pip install langflow -U`
`pip install streamlit`
`pip install seaborn`

`python -m langflow run`
`python -m streamlit run main.py`

B(в разработке):
`docker-compose up --build`


**Доступ:**
- Langflow: http://localhost:7860
- Streamlit: http://localhost:8000

**API:**
- `GET /api/v1/flows` - список потоков
- `POST /api/v1/run/{id}` - выполнить поток
- `GET /api/v1/health` - проверка сервиса

**Разработка:**
- Добавьте JSON-потоки в `langflow/flows/`
- Перезапустите: `docker-compose restart langflow`
- Логи: `docker-compose logs -f langflow|agent`

**Проблемы?**
1. Проверьте файлы: `docker-compose exec langflow ls /app/flows/`
2. Проверьте ID: `docker-compose exec langflow cat /app/flows/Agent.json`
3. Проверьте подключение: `docker-compose exec agent curl http://langflow:7860/api/v1/health`