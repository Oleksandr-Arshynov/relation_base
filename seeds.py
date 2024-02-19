from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from models import Student, Group, Teacher, Subject, Grade
import random
from datetime import datetime, timedelta


engine = create_engine('sqlite://///Users/oleksandrarshinov/Desktop/Documents/Repository/hw7/my_db')
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

# Створення груп
for _ in range(3):
    group_name = fake.company()
    group = Group(name=group_name)
    session.add(group)

# Створення викладачів
for _ in range(random.randint(5, 5)):
    teacher_name = fake.name()
    teacher = Teacher(name=teacher_name)
    session.add(teacher)

# Створення предметів
teachers = session.query(Teacher).all()
for _ in range(random.randint(3, 8)):
    subject_name = fake.word()
    teacher = random.choice(teachers)
    subject = Subject(name=subject_name, teacher=teacher)
    session.add(subject)

# Створення студентів
groups = session.query(Group).all()
for _ in range(random.randint(30, 50)):
    student_name = fake.name()
    group = random.choice(groups)
    student = Student(name=student_name, group=group)
    session.add(student)

students = session.query(Student).all()
subjects = session.query(Subject).all()
   
for student in students:
    for subject in subjects:
        # Генерація випадкової кількості оцінок для кожного предмету
        for _ in range(random.randint(0, 2)):
            grade_value = random.randint(1, 100)
            # Генерація випадкової дати
            date = fake.date_time_between(start_date="-2y", end_date="now")
            # Створення нового об'єкту оцінки та збереження його в базу даних
            grade = Grade(student_id=student.id, subject_id=subject.id, grade=grade_value, date=date)
            session.add(grade)
# Збереження змін
session.commit()