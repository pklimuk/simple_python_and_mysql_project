from sqlalchemy import create_engine, Column, Integer, String, update
from sqlalchemy import ForeignKey, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime


class InvalidData(Exception):
    """ Base class for invalid data exceptions """
    pass


class NoStudentGiven(InvalidData):
    """ Raised when id/student_id parameter is not given """
    pass


class InvalidStudentID(InvalidData):
    """ Raised when invalid id/student_id parameter is given """
    pass


class InvalidSubject(InvalidData):
    """ Raised when invalid subject parameter is given """
    pass


class InvalidLimit(InvalidData):
    """ Raised when invalid limit parameter is given """


engine = create_engine('sqlite:///project_database_1.db')
Base = declarative_base()
metadata = MetaData()


sciene_work_association_table = Table('science_work', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.student_id')),
    Column('publication_id', Integer, ForeignKey('publications.publication_id'))
)


marks_association_table = Table('marks', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.student_id')),
    Column('subject_id', Integer, ForeignKey('subjects.subject_id')),
    Column('mark', Integer, nullable=False),
    Column('semester', Integer, nullable=False)
)


class Students(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True, nullable=False)
    student_first_name = Column(String, nullable=False)
    student_last_name = Column(String, nullable=False)
    student_email = Column(String, nullable=False)
    student_gender = Column(String, nullable=False)
    student_birth_date = Column(String, nullable=False)
    student_current_semester = Column(Integer, nullable=False)

    children_1 = relationship("Publications", secondary=sciene_work_association_table, back_populates="parents_1", single_parent=True, cascade="all, delete, delete-orphan")
    children_3 = relationship("Subjects", secondary=marks_association_table, back_populates="parents_3", single_parent=True)


    def creating_student(first_name, last_name, email, gender, birth_date, current_semester):
        Session = sessionmaker(bind=engine)
        session = Session()
        new_student = Students(student_first_name=first_name, student_last_name=last_name,
        student_email=email, student_gender=gender, student_birth_date=birth_date,
        student_current_semester=current_semester)
        session.add(new_student)
        session.commit()
        return True


    def deleting_student_through_id(id):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            if id is None:
                raise NoStudentGiven
            elif id != session.query(Students.student_id).filter(Students.student_id == id).scalar():
                raise InvalidStudentID
            student = session.query(Students).filter_by(student_id=id).one()
            session.delete(student)
            session.commit()
            return True
        except NoStudentGiven:
            print("Id is required. Try again")
        except InvalidStudentID:
            print("Try again. There is no student with such id")


    def modifying_student(id, first_name, last_name, email, gender, birth_date, current_semester):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            if id is None:
                raise NoStudentGiven
            elif id != session.query(Students.student_id).filter(Students.student_id == id).scalar():
                raise InvalidStudentID
            session.query(Students).filter(Students.student_id == id).\
            update({Students.student_first_name: first_name, Students.student_last_name: last_name,
                Students.student_email: email, Students.student_gender: gender,
                Students.student_birth_date: birth_date, Students.student_current_semester: current_semester},
                synchronize_session=False)
            session.commit()
            return True
        except NoStudentGiven:
            print("Id is required. Try again")
        except InvalidStudentID:
            print("Try again. There is no student with such id")


    def studying_history(student_id):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            if student_id is None:
                raise NoStudentGiven
            elif student_id != session.query(Students.student_id).filter(Students.student_id == student_id).scalar():
                raise InvalidStudentID
            result = session.query(Students.student_first_name, Students.student_last_name, Subjects.subject_name, marks_association_table.c.mark, marks_association_table.c.semester).\
                filter(marks_association_table.c.subject_id == Subjects.subject_id).filter(marks_association_table.c.student_id == Students.student_id).\
                filter(Students.student_id == student_id)
            session.commit()
            returning_list = []
            for row in result:
                returning_list.append((result[0][0], result[0][1], row[2], str(row[3]), str(row[4])))
            return returning_list
        except NoStudentGiven:
            print("Id is required. Try again")
        except InvalidStudentID:
            print("Try again. There is no student with such id")


class Publications(Base):
    __tablename__ = 'publications'

    publication_id = Column(Integer, primary_key=True, nullable=False)
    publication_title = Column(String, nullable=False)
    publication_number = Column(Integer, nullable=False)
    publication_points = Column(Integer, nullable=False)
    publication_date = Column(String, nullable=False)

    parents_1 = relationship('Students', secondary=sciene_work_association_table, back_populates="children_1")


    def number_of_publication_authors(publication_id):
        authors = Publications.authors_of_the_publication(publication_id)
        number_of_authors = len(authors)
        return number_of_authors


    def points_for_publication(publication_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        default_points = session.query(Publications.publication_points).\
            filter(Publications.publication_id == publication_id).scalar()
        number_of_authors = Publications.number_of_publication_authors(publication_id)
        session.commit()
        points = round(default_points / number_of_authors, 2)
        return points


    def points_for_publication_for_period(student_id, date_1, date_2):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            if student_id is None:
                raise NoStudentGiven
            elif student_id != session.query(Students.student_id).filter(Students.student_id == student_id).scalar():
                raise InvalidStudentID
            publications = session.query(Publications.publication_date, Publications.publication_id).\
            filter(sciene_work_association_table.c.publication_id == Publications.publication_id).filter(Students.student_id == sciene_work_association_table.c.student_id).\
            filter(Students.student_id == student_id).all()
            person = session.query(Students.student_first_name, Students.student_last_name).\
                filter(Students.student_id ==student_id).first()
            session.commit()
            date_1_datetime = datetime.strptime(date_1, "%m/%d/%Y")
            date_2_datetime = datetime.strptime(date_2, "%m/%d/%Y")
            valid_date_publication_id = []
            for publication in publications:
                publication_datetime = datetime.strptime(publication[0], "%m/%d/%Y")
                if date_1_datetime <= publication_datetime and publication_datetime <= date_2_datetime:
                    valid_date_publication_id.append(publication[-1])
            points = 0
            for publication_id in valid_date_publication_id:
                publication_points = Publications.points_for_publication(publication_id)
                points += publication_points
            result = [person[0], person[1], points]
            return result
        except NoStudentGiven:
            print("Id is required. Try again")
        except InvalidStudentID:
            print("Try again. There is no student with such id")


    def authors_of_the_publication(publication_id):
        Session = sessionmaker(bind=engine)
        session = Session()
        authors = session.query(Students.student_first_name, Students.student_last_name).\
        filter(sciene_work_association_table.c.publication_id == Publications.publication_id).filter(Students.student_id == sciene_work_association_table.c.student_id).\
        filter(Publications.publication_id == publication_id)
        session.commit()
        authors_list = []
        for author in authors:
            authors_list.append(author[0] + " " + author[1])
        return authors_list


    def publications_history(student_id):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            if student_id is None:
                raise NoStudentGiven
            elif student_id != session.query(Students.student_id).filter(Students.student_id == student_id).scalar():
                raise InvalidStudentID
            publications = session.query(Students.student_first_name, Students.student_last_name, Publications.publication_title, Publications.publication_date, Publications.publication_id).\
            filter(sciene_work_association_table.c.publication_id == Publications.publication_id).filter(Students.student_id == sciene_work_association_table.c.student_id).\
            filter(Students.student_id == student_id)
            session.commit()
            end_result = [publications[0][0], publications[0][1]]
            for publication in publications:
                history = []
                authors_history = []
                authors = Publications.authors_of_the_publication(publication[-1])
                history.append(publication[2] + ", " + publication[3])
                authors_history.append(authors)
                result = zip(history, authors_history)
                end_result.append(result)
            return end_result
        except NoStudentGiven:
            print("Id is required. Try again")
        except InvalidStudentID:
            print("Try again. There is no student with such id")


class Subject_groups(Base):
    __tablename__ = 'subject_groups'

    group_id = Column(Integer, primary_key=True, nullable=False)
    group_name = Column(String, nullable=False)

    parents_2 = relationship('Subjects', back_populates="child_2")


class Subjects(Base):
    __tablename__ = 'subjects'

    subject_id = Column(Integer, primary_key=True, nullable=False)
    subject_name = Column(String, nullable=False)
    subject_shortname = Column(Integer, nullable=False)
    group_id = Column(Integer, ForeignKey('subject_groups.group_id'))
    ects_points = Column(Integer, nullable=False)

    child_2 = relationship('Subject_groups', back_populates="parents_2")
    parents_3 = relationship('Students', secondary=marks_association_table, back_populates="children_3")


    def avarage_student_mark(student_id):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            if student_id is None:
                raise NoStudentGiven
            elif student_id != session.query(Students.student_id).filter(Students.student_id == student_id).scalar():
                raise InvalidStudentID
            marks = session.query(Students.student_first_name, Students.student_last_name, marks_association_table.c.mark).\
                filter(marks_association_table.c.student_id == student_id).filter(Students.student_id == student_id).all()
            session.commit()
            sum_of_marks = 0
            number_of_marks = len(marks)
            if number_of_marks == 0:
                return [0]
            reslut = [marks[0][0], marks[0][1]]
            for mark in marks:
                sum_of_marks += mark[-1]
            else:
                avarage = round(sum_of_marks / number_of_marks, 2)
                reslut.append(avarage)
                return reslut
        except NoStudentGiven:
            print("Id is required. Try again")
        except InvalidStudentID:
            print("Try again. There is no student with such id")


    def ranking_list(limit):
        try:
            result = []
            if limit < 0 or limit > 100:
                raise InvalidLimit
            Session = sessionmaker(bind=engine)
            session = Session()
            students = session.query(Students.student_first_name, Students.student_last_name, Students.student_id).all()
            session.commit()
            number_of_students = len(students)
            number_of_students_with_limit = round(number_of_students * limit / 100)
            students_avarage_marks_list = []
            for student in students:
                result = Subjects.avarage_student_mark(student[-1])
                avarage_mark = result[-1]
                students_avarage_marks_list.append((student[0] + " " + student[1], avarage_mark))
            students_avarage_marks_list = sorted(students_avarage_marks_list, key=lambda a: a[1], reverse=True)
            students_top_list = students_avarage_marks_list[:number_of_students_with_limit]
            return students_top_list
        except InvalidLimit:
            print("Limit bust be integer in range (0-100)")


    def requierements_verification(student_id, subject_group, ects_points):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            if student_id is None:
                raise NoStudentGiven
            elif student_id != session.query(Students.student_id).filter(Students.student_id == student_id).scalar():
                raise InvalidStudentID
            if session.query(Subject_groups.group_name).filter(Subject_groups.group_name.in_([subject_group])).first() is None:
                raise InvalidSubject
            result = session.query(Students.student_first_name, Students.student_last_name,
                marks_association_table.c.mark, Subjects.ects_points, Subject_groups.group_name).\
                filter(marks_association_table.c.student_id == student_id).filter(marks_association_table.c.subject_id == Subjects.subject_id).\
                filter(Subjects.group_id == Subject_groups.group_id).filter(Students.student_id == student_id).all()
            session.commit()
            collected_points = 0
            group_marks = []
            returning_list = [result[0][0], result[0][1]]
            for tup in result:
                if tup[-1] == subject_group:
                    group_marks.append((tup[2], tup[3]))
            for element in group_marks:
                if element[0] >= 3:
                    collected_points += element[1]
            if collected_points >= ects_points:
                returning_list.append(collected_points)
                return True, returning_list
            else:
                returning_list.append(collected_points)
                return False, returning_list
        except NoStudentGiven:
            print("Id is required. Try again")
        except InvalidStudentID:
            print("Try again. There is no student with such id")
        except InvalidSubject:
            print("Try again. There is no such subject")


Base.metadata.create_all(engine)
