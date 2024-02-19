from sqlalchemy import create_engine, desc, func
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Subject, Grade, Teacher

# Підключення до бази даних
engine = create_engine('sqlite:////Users/oleksandrarshinov/Desktop/Documents/Repository/SQL_alchemy_alembic/my_db')

# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()

# Запит 1: Знайти 5 студентів із найбільшим середнім балом з усіх предметів
def select_1():
    students_avg_grade = session.query(Student.name, func.avg(Grade.grade).label('average_grade')) \
    .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()    
    return students_avg_grade   

# Запит 2: Знайти студента із найвищим середнім балом з певного предмета
def select_2(subject_name):
    student_max_avg_grade = session.query(Student, func.avg(Grade.grade).label('avg_grade')) \
        .join(Grade, Student.id == Grade.student_id) \
        .join(Subject, Grade.subject_id == Subject.id) \
        .filter(Subject.name == subject_name) \
        .group_by(Student.id) \
        .order_by(func.avg(Grade.grade).desc()) \
        .first()
    return student_max_avg_grade

# Запит 3: Знайти середній бал у групах з певного предмета
def select_3(subject_name):
    groups_avg_grade = session.query(Group.name, func.avg(Grade.grade).label('avg_grade')) \
        .join(Student, Group.id == Student.group_id) \
        .join(Grade, Student.id == Grade.student_id) \
        .join(Subject, Grade.subject_id == Subject.id) \
        .filter(Subject.name == subject_name) \
        .group_by(Group.id) \
        .all()
    return groups_avg_grade

# Запит 4: Знайти середній бал на потоці (по всій таблиці оцінок)
def select_4():
    overall_avg_grade = session.query(func.avg(Grade.grade)).scalar()
    return overall_avg_grade

# Запит 5: Знайти які курси читає певний викладач
def select_5(teacher_name):
    teacher_courses = session.query(Subject.name) \
        .join(Teacher, Subject.teacher_id == Teacher.id) \
        .filter(Teacher.name == teacher_name) \
        .all()
    return teacher_courses

# Запит 6: Знайти список студентів у певній групі
def select_6(group_name):
    group_students = session.query(Student.name) \
        .join(Group, Student.group_id == Group.id) \
        .filter(Group.name == group_name) \
        .all()
    return group_students

# Запит 7: Знайти оцінки студентів у окремій групі з певного предмета
def select_7(group_name, subject_name):
    group_subject_grades = session.query(Student.name, Grade.grade) \
        .join(Group, Student.group_id == Group.id) \
        .join(Grade, Student.id == Grade.student_id) \
        .join(Subject, Grade.subject_id == Subject.id) \
        .filter(Group.name == group_name, Subject.name == subject_name) \
        .all()
    return group_subject_grades

# Запит 8: Знайти середній бал, який ставить певний викладач зі своїх предметів
def select_8(teacher_name):
    teacher_avg_grade = session.query(func.avg(Grade.grade)) \
        .join(Subject, Grade.subject_id == Subject.id) \
        .join(Teacher, Subject.teacher_id == Teacher.id) \
        .filter(Teacher.name == teacher_name) \
        .scalar()
    return teacher_avg_grade

# Запит 9: Знайти список курсів, які відвідує певний студент
def select_9(student_name):
    student_courses = session.query(Subject.name) \
        .join(Grade, Subject.id == Grade.subject_id) \
        .join(Student, Grade.student_id == Student.id) \
        .filter(Student.name == student_name) \
        .all()
    return student_courses

# Запит 10: Список курсів, які певному студенту читає певний викладач
def select_10(student_name, teacher_name):
    student_teacher_courses = session.query(Subject.name) \
        .join(Grade, Subject.id == Grade.subject_id) \
        .join(Student, Grade.student_id == Student.id) \
        .join(Teacher, Subject.teacher_id == Teacher.id) \
        .filter(Student.name == student_name, Teacher.name == teacher_name) \
        .distinct() \
        .all()
    return student_teacher_courses

# Закриваємо сесію
session.close()

print("Запит 1") 
result1 = select_1()
# for r in result1:
print(result1,"\n")
    
print("Запит 2")     
result2 = select_2('current')

for r in result2:
    print(r,"\n")
    
print("Запит 3")     
result3 = select_3('current')
for r in result3:
    print(r,"\n")

print("Запит 4")   
result4 = select_4()
print(f"Cередній бал на потоці (по всій таблиці оцінок) {result4}","\n")

print("Запит 5")     
result5 = select_5('Derek Swanson')
for r in result5:
    print(r,"\n")
       
print("Запит 6")     
result6 = select_6('Stephens and Sons')
print(result6)

print("Запит 7")     
result7 = select_7('Stephens and Sons', 'current')
for r in result7:
    print(r,"\n")
    
print("Запит 8")     
result8 = select_8('Heather White')
print(result8,"\n")

print("Запит 9")     
result9 = select_9('Kimberly Young')
print(result9,"\n")
    
print("Запит 10")     
result10 = select_10('Mark Dominguez', 'Derek Swanson')
print(result10,"\n")