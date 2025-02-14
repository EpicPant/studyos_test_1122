from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.router import router as router_auth
from sphere.router import router as sphere_router
from course.router import router as course_router
from module.router import router as module_router
from topic.router import router as topic_router
from card.router import router as card_router
from last_recently.router import router as last_recent_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Добавляем middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

#app.mount('/static', StaticFiles(directory='app/static'), name='static')


@app.get("/")
def home_page():
    return {
        "message": "StudyOS хули"
    }


app.include_router(router_auth)
app.include_router(sphere_router)
app.include_router(module_router)
app.include_router(course_router)
app.include_router(topic_router)
app.include_router(card_router)
app.include_router(last_recent_router)
