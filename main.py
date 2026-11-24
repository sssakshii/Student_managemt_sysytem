
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, computed_field
import json
import os

app = FastAPI(title="Student Management System")

FILE_NAME = "students.json"


# Read JSON file
def load_data():
    if not os.path.exists(FILE_NAME):
        return {"students": []}

    with open(FILE_NAME, "r") as file:
        return json.load(file)


# Write JSON file
def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


# Pydantic model
class Student(BaseModel):
    name: str
    class_name: str
    age: int = Field(gt=0)
    father_name: str
    mother_name: str
    monthly_fee: float = Field(ge=0)
    height: float = Field(gt=0)
    weight: float = Field(gt=0)

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def bmi_verdict(self) -> str:

        if self.age < 18:
            return "Age-specific BMI assessment required"

        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal weight"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


# HOME
@app.get("/")
def home():
    return {"message": "Student Management System"}


# POST - Add student
@app.post("/students")
def add_student(student: Student):

    data = load_data()

    students = data["students"]

    new_id = max(
        (s["id"] for s in students),
        default=0
    ) + 1

    student_data = student.model_dump()
    student_data["id"] = new_id

    students.append(student_data)

    save_data(data)

    return {
        "message": "Student added successfully",
        "student": student_data
    }


# GET - All students
@app.get("/students")
def get_students():

    data = load_data()

    return data


# GET - Student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):

    data = load_data()

    for student in data["students"]:
        if student["id"] == student_id:
            return student

    raise HTTPException(status_code=404, detail="Student not found")


# PUT - Update student
@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):

    data = load_data()

    for index, student in enumerate(data["students"]):

        if student["id"] == student_id:

            student_data = updated_student.model_dump()
            student_data["id"] = student_id

            data["students"][index] = student_data

            save_data(data)

            return {
                "message": "Student updated successfully",
                "student": student_data
            }

    raise HTTPException(status_code=404, detail="Student not found")


# DELETE - Delete student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    data = load_data()

    for student in data["students"]:

        if student["id"] == student_id:

            data["students"].remove(student)

            save_data(data)

            return {
                "message": "Student deleted successfully",
                "student_id": student_id
            }

    raise HTTPException(status_code=404, detail="Student not found")
