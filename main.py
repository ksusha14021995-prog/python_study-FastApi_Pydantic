import uvicorn
import re
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, field_validator
from datetime import date, datetime
import json
from enum import Enum

class Reason(str, Enum):
    network = "нет доступа к сети"
    phone = "не работает телефон"
    mail = "не приходят письма"

class Student(BaseModel):
    surname: str
    name: str
    birthday_date: date
    phone: str
    email: EmailStr
    reason: list[Reason]
    detected_time: datetime

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        pattern = r"^[А-ЯЁ][а-яё]+$"
        if not re.match(pattern, value):
            raise ValueError("Имя должно начинаться с заглавной буквы и содержать только кириллицу")
        return value

    @field_validator("surname")
    def validate_surname(cls, value: str) -> str:
        pattern = r"^[А-ЯЁ][а-яё]+$"
        if not re.match(pattern, value):
            raise ValueError("Фамилия должна начинаться с заглавной буквы и содержать только кириллицу")
        return value

    @field_validator("phone")
    def validate_phone(cls, value: str) -> str:
        pattern = r"^[0-9\-\+]{9,15}$"
        if not re.match(pattern, value):
            raise ValueError("Телефон должен быть введен по маске")
        return value

app = FastAPI()

@app.get("/health")
async def health():
    return {"mes": "ok"}

@app.post("/add_student")
async def add(model:Student):
    data = model.model_dump(mode="json")
    with open("student.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return model.model_dump()

if __name__ == "__main__":
    uvicorn.run(
        "__main__:app",
        host='0.0.0.0',
        port=8000,
        reload=True
    )

