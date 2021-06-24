from program import Students, Publications, Subjects,\
    marks_association_table, sciene_work_association_table, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func


def test_avarage_mark():
    Session = sessionmaker(bind=engine)
    session = Session()
    student_id = 100
    student = Students(student_id=student_id, student_first_name="Ed", student_last_name="Donavan", student_email="d.@.com",
        student_gender="Male", student_birth_date="05/05/1995", student_current_semester=5)

    session.add(student)
    marks_1 = marks_association_table.insert().values(student_id=100, subject_id=1, mark=3, semester=4)
    marks_2 = marks_association_table.insert().values(student_id=100, subject_id=2, mark=5, semester=4)
    conn = engine.connect()
    conn.execute(marks_1)
    conn.execute(marks_2)
    session.commit()
    result = Subjects.avarage_student_mark(student_id)
    avarage = result[-1]

    assert avarage == 4.0


def test_create_student():
    Session = sessionmaker(bind=engine)
    session = Session()
    amount_1 = session.query(func.count(Students.student_id)).scalar()
    first_name = "Dan"
    last_name = "McDavid"
    email = "Dan@gmail.com"
    gender = "Male"
    birth_date = "10/10/1995"
    current_sem = 3
    Students.creating_student(first_name, last_name, email, gender, birth_date, current_sem)
    amount_2 = session.query(func.count(Students.student_id)).scalar()
    session.commit()
    result = amount_2 - amount_1

    assert result == 1


def test_delete_student():
    Session = sessionmaker(bind=engine)
    session = Session()
    student_id = 105
    student = Students(student_id=student_id, student_first_name="Bob", student_last_name="Davis", student_email="d.@.com",
        student_gender="Male", student_birth_date="10/08/1997", student_current_semester=3)

    session.add(student)
    session.commit()
    Students.deleting_student_through_id(student_id)
    session.commit()
    result = session.query(Students.student_id).filter(Students.student_id == student_id).scalar()
    session.commit()

    assert result is None


def test_modifying_student():
    Session = sessionmaker(bind=engine)
    session = Session()
    student_id = 102
    student = Students(student_id=student_id, student_first_name="Alice", student_last_name="Carter", student_email="c.@.com",
        student_gender="Female", student_birth_date="10/03/1996", student_current_semester=4)

    session.add(student)
    session.commit()
    first_name = "Lisa"
    last_name = "Carter"
    email = "l@gmail.com"
    gender = "Feale"
    birth_date = "10/03/1996"
    current_sem = 4
    Students.modifying_student(student_id, first_name, last_name, email,
         gender, birth_date, current_sem)
    result = session.query(Students.student_first_name).filter_by(student_id=student_id).first()
    session.commit
    name = result[0]

    assert name == "Lisa"


def test_points_for_publication():
    Session = sessionmaker(bind=engine)
    session = Session()
    student_id = 103
    student_1 = Students(student_id=student_id, student_first_name="Brad", student_last_name="Dilan", student_email="d.@.com",
    student_gender="Male", student_birth_date="10/07/1995", student_current_semester=4)

    student_2 = Students(student_id=104, student_first_name="El", student_last_name="Donavan", student_email="d.@.com",
    student_gender="Male", student_birth_date="05/05/1994", student_current_semester=5)

    pub_1 = Publications(publication_id=110, publication_title="Pub1", publication_number="20-90",
    publication_points=40,publication_date="07/08/2017")

    pub_2 = Publications(publication_id=111, publication_title="Pub2", publication_number="10-60",
    publication_points=70, publication_date="07/09/2016")
    session.add(student_2)
    session.add(student_1)
    session.add(pub_2)
    session.add(pub_1)
    session.commit()
    publication_1 = sciene_work_association_table.insert().values(student_id=103, publication_id=110)
    publication_2 = sciene_work_association_table.insert().values(student_id=103, publication_id=111)
    publication_3 = sciene_work_association_table.insert().values(student_id=104, publication_id=111)
    conn = engine.connect()
    conn.execute(publication_1)
    conn.execute(publication_2)
    conn.execute(publication_3)
    session.commit()
    date_1 = "06/05/2012"
    date_2 = "03/08/2019"
    result = Publications.points_for_publication_for_period(student_id, date_1, date_2)
    points = result[-1]
    assert points == 75.0

