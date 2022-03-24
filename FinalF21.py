import os


class Student:
    def __init__(self, f_name, l_name, id, score, quiz, grade = "", average = 0):
        self.f_name = f_name
        self.l_name = l_name
        self.id = id
        self.score = score
        self.quiz = quiz
        self.grade = grade
        self.average = average

dict = {}
list_lName = []

def read_file(file_name, dict):
    try:
        if os.stat(file_name).st_size == 0:
            raise EOFError
        with open(file_name, 'r') as i_file:
            c_name = i_file.readline().strip()
            dict["course name"] = c_name
            c_id = i_file.readline().strip()
            dict["course id"] = c_id
            c_loc = i_file.readline().strip()
            dict["class location"] = c_loc
            # print("read",c_name,c_id,c_loc)
            count = 0
            s_fname = ""
            s_lname = ""
            s_id = ""
            s_quiz = 0
            s_score = []
            for line in i_file:
                if count % 2 == 0:
                    s_fname = str(line.split()[0])
                    s_lname_temp = line.split()[1:]
                    for i in s_lname_temp:
                        s_lname += (" "+i)
                    # print(line+"-> alpha:",s_fname,",",s_lname.strip())
                    count += 1
                    continue
                elif count % 2 == 1:
                    s_id = str(line.strip().split()[0])
                    s_quiz = int(line.strip().split()[1])
                    s_score_temp = line.strip().split()[2:8]
                    for i in s_score_temp:
                        s_score.append(int(i))
                    # print(line+"-> digit",s_id,",",s_quiz,",",s_score)
                list_lName.append(s_lname.strip())
                dict_temp = Student(s_fname, s_lname.strip(), s_id, s_score, s_quiz)
                dict_temp.average = cal_average(dict_temp)
                dict_temp.grade = grade_student(dict_temp)
                dict[s_lname.strip()] = dict_temp.__dict__
                s_fname = ""
                s_lname = ""
                s_id = ""
                s_quiz = 0
                s_score = []
                count += 1
    except EOFError:
        print("Error: Data file {} is blank.".format(file_name))
        exit(0)
    except:
        print("Error: file {} does not exist.".format(file_name))
        exit(0)


def write_file(file_name, dict):
    try:
        with open(file_name, 'w') as o_file:
            o_file.write("Course Name:\t{}\n".format(dict['course name']))
            o_file.write("Course ID:\t{}\n".format(dict['course id']))
            o_file.write("Course Location:\t{}\n".format(dict['class location']))
            o_file.write("\nName\tID\tAverage\tGrade\n")
            total_avg = 0
            total_count = 0
            for i in list_lName:
                # id_temp = dict[i]['id'][:3] + "-" + dict[i]['id'][3:5] + "-" + dict[i]['id'][5:]
                o_file.write("{}, {}\t{}\t{:.2f}\t{}\n".format(dict[i]['l_name'], dict[i]['f_name'], dict[i]['id'], dict[i]['average'], dict[i]['grade']))
                if dict[i]['average'] > 0:
                    total_avg += dict[i]['average']
                    total_count += 1
            o_file.write("\nClass Average for {} students is:\t{:.2f}\n".format(total_count, (total_avg / total_count)))
    except :
        print("Error: file {} does not exist.".format(file_name))
        exit(0)

def cal_average(Student):
    for i in Student.score:
        if i < 0 or i > 100:
            return -1
    sorted_score = sorted(Student.score, reverse=True)
    total = 0
    for i in range(5):
        total += sorted_score[i]
    result = ((total/5) * 0.9) + (Student.quiz * 0.1)
    return result

def grade_student(Student):
    avg = Student.average
    grade = ''
    if 90 <= avg <= 100:
        grade = 'A'
    elif 80 <= avg <= 89.9:
        grade = 'B'
    elif 70 <= avg <= 79.9:
        grade = 'C'
    elif 60 <= avg <= 69.9:
        grade = 'D'
    elif 0 <= avg <= 59.9:
        grade = 'F'
    else:
        grade = 'I'
    return grade

def print_dict(dict):
    print("Name\tAverage\tGrade")
    for i in list_lName:
        print("{}, {}\t{:.2f}\t{}".format(dict[i]['l_name'], dict[i]['f_name'], dict[i]['average'], dict[i]['grade']))

def find_dict(dict):
    key = input("Enter last name: ")
    flag = True
    for i in list_lName:
        if i == key:
            print("{}, {}".format(dict[i]['l_name'], dict[i]['f_name']))
            print("Student ID:\t{}".format(dict[i]['id']))
            print("Student Test Scores:\t{}".format(dict[i]['score']))
            print("Student Quiz Score:\t{:.2f}".format(dict[i]['quiz']))
            print("Student Average:\t{:.2f}".format(dict[i]['average']))
            print("Student letter Grade:\t{}".format(dict[i]['grade']))
            flag = True
            break
        flag = False
    if not flag:
        print("Error: {} is not on the list.".format(key))
    return flag

def add(dict):
    lName = input("Enter last name: ")
    flag = True
    for i in list_lName:
        if lName == i:
            flag = False
    if flag:
        fName = input("Enter first name: ")
        id = input("Enter ID: ")
        quiz = int(input("Enter quiz score: "))
        score = []
        print("Enter 6 test scores on per line: ")
        for i in range(6):
            score.append(int(input()))
        list_lName.append(lName.strip());
        dict_temp = Student(fName, lName.strip(), id, score, quiz)
        dict_temp.average = cal_average(dict_temp)
        dict_temp.grade = grade_student(dict_temp)
        dict[lName] = dict_temp.__dict__
        print("{} has been added to the list.".format(lName))
    else:
        print("Error: {} is on the list, duplicates are not allowed.".format(lName))

def remove(dict):
    lName = input("Enter last name: ")
    flag = False
    for i in list_lName:
        if lName == i:
            flag = True
    if flag:
        del dict[lName]
        list_lName.remove(lName)
        print("{} has been removed from the list.".format(lName))
    else:
        print("Error: {} is not on the list.".format(lName))

def main():
    '''
    1)  read file and store in your data structure
	2)	Process data (verify scores, calculate average and assign grade)
	3)	Print course content to the monitor
	4)	Search for a student and print details to the monitor
	5)	Add a new student to the list
	6)  Remove a student from the list
	7)	Sort the list of students alphabetically and print to the monitor
	8)  Print course content to a file
	'''

    read_filename = input("enter input file name: ")
    read_file(read_filename, dict)
    # read_file("course.txt",dict)
    print_dict(dict)
    find_dict(dict)
    add(dict)
    remove(dict)
    list_lName.sort()
    print_dict(dict)
    write_filename = input("enter output file name: ")
    write_file(write_filename, dict)
    # write_file("out.txt", dict)
    return

main()
