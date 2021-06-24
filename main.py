from program import Students, Publications, Subjects
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-cm', '--command', required=True)
parser.add_argument('-si', '--student_id', type=int, required=False)
parser.add_argument('-sf', '--student_first_name', required=False)
parser.add_argument('-sl', '--student_last_name', required=False)
parser.add_argument('-se', '--student_email', required=False)
parser.add_argument('-sg', '--student_gender', required=False)
parser.add_argument('-sb', '--student_birth_date', required=False)
parser.add_argument('-sc', '--student_current_semester', type=int, required=False)
parser.add_argument('-d1', '--date_1', required=False)
parser.add_argument('-d2', '--date_2', required=False)
parser.add_argument('-l', '--limit', type=int, default=20, required=False)
parser.add_argument('-subg', '--subject_group', required=False)
parser.add_argument('-ep', '--ects_points', type=int, default=11, required=False)
args = parser.parse_args()


if __name__ == '__main__':
    if args.command not in ['avarage_mark', 'create_student', 'delete_student', 'modify_student',
        'studying_history', 'publications_history', 'points_for_publications', 'ranking_list', 'requirements_verification']:
        raise Exception("Invalid command. Try again")

    if args.command == 'avarage_mark':
        result = Subjects.avarage_student_mark(args.student_id)
        print("\n")
        print(result[0] + " " + result[1] + "'s" + " " + " avarage mark is: " + str(result[2]))
        print("\n")


    if args.command == 'create_student':
        if Students.creating_student(args.student_first_name, args.student_last_name, args.student_email,
        args.student_gender, args.student_birth_date, args.student_current_semester) is True:
            print("Student was successfully created")

    if args.command == 'delete_student':
        if Students.deleting_student_through_id(args.student_id) is True:
            print("Student with id {} was successfully deleted".format(args.student_id))

    if args.command == 'modify_student':
        if Students.modifying_student(args.student_id, args.student_first_name, args.student_last_name, args.student_email,
        args.student_gender, args.student_birth_date, args.student_current_semester) is True:
            print("Student with id {} was successfully modified".format(args.student_id))

    if args.command == 'studying_history':
        result = Students.studying_history(args.student_id)
        print("\n")
        print((result[0][0] + " " + result[0][1] + "'s" + " " + "marks:"))
        for row in result:
            print(row[2] + " " + str(row[3]) + ", semester " + str(row[4]))

    if args.command == 'publications_history':
        result = Publications.publications_history(args.student_id)
        print("\n")
        print(result[0] + " " + result[1] + "'s " + "Publications:" + "\n")
        for each in result[2:]:
            for i in each:
                print(i)
        print("\n")

    if args.command == 'points_for_publications':
        result = Publications.points_for_publication_for_period(args.student_id, args.date_1, args.date_2)
        print(result[0] + " " + result[1] + "'s " + "points for publications: " + str(result[2]))

    if args.command == 'ranking_list':
        if args.limit == 0:
            print("No students with grants")
        else:
            students_top_list = Subjects.ranking_list(args.limit)
            print("\t")
            print("The list of students with grants:")
            for tup in students_top_list:
                print(tup[0] + " " + str(tup[1]))

    if args.command == 'requirements_verification':
        result = Subjects.requierements_verification(args.student_id, args.subject_group, args.ects_points)
        if result[0] is True:
            print(result[1][0] + " " + result[1][1] + " " + "passed requirements with {}".format(result[1][-1]) + " " + "points")
        elif result[0] is False:
            print(result[1][0] + " " + result[1][1] + " " + "didn't pass requirements")
