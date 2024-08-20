from fastapi import FastAPI
from src.activity.routers import router as activity_router
from src.entry.routers import router as entry_router
from src.user.routers import router as user_router
from src.pages.routers import router as pages_router
from src.chart.routers import router as chart_router
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# Стандартная схема авторизации через Bearer токен
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# Сохраняем оригинальную функцию openapi
original_openapi = app.openapi

# Функция для настройки JWT авторизации в OpenAPI (Swagger)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = original_openapi()  # Используем оригинальную функцию openapi

    # Добавляем схему безопасности с использованием Bearer токена
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Добавляем глобальную безопасность для всех эндпоинтов
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Устанавливаем функцию для генерации кастомной схемы OpenAPI
app.openapi = custom_openapi

# Подключаем роутеры с нужными префиксами и тегами
app.include_router(activity_router, prefix="/api/activities", tags=["Activities"])
app.include_router(entry_router, prefix="/api/entries", tags=["Entries"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])
app.include_router(pages_router, prefix="/api/pages", tags=["Pages"])
app.include_router(chart_router, prefix="/api/charts", tags=["Charts"])

@app.get("/")
async def root():
    return {"message": "API is running"}
