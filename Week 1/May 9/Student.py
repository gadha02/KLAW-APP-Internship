class Student:
    def __init__(self,name,student_id,age,marks):
        self.name = name
        self.student_id = student_id
        self.age = age
        self.marks = marks

    def display(self):
        print(f"Name: {self.name}")
        print(f"ID: {self.student_id}")
        print(f"Age: {self.age}")
        print(f"Marks: {self.marks}")


class StudentManagementSystem:
    def __init__(self):
        self.student_list = []

    def add_student(self):
    
        student_id = input("Enter student id: ")
        for student in self.student_list:
            if student.student_id == student_id:
                print("Student already exists\n")
                return

        name = input("Enter name: ")
        age = input("Enter age: ")
        marks = input("Enter marks: ")
        student = Student(name,student_id,age,marks)
        self.student_list.append(student)
        print("Student added successfully\n")

    def delete_student(self):
        
        student_id = input("Enter student id: ")
        for student in self.student_list:
            if student_id == student.student_id:
                self.student_list.remove(student)
                print(f"Student {student.name} removed successfully \n")
                return

        print("Student not found \n")

    def search(self):
        print("1. Search by id \n2. Search by name")
        op = int(input("Enter your choice: "))
        print("\n")
        match op:
            case 1:
                student_id = input("Enter student id: ")
                for student in self.student_list:
                    if student_id == student.student_id:
                        student.display()
                        return
                
                print("Student not found\n")

            case 2:
                name = input("Enter name: ")
                for student in self.student_list:
                    if name == student.name:
                        student.display()
                        return
                
                print("Student not found\n")

    def display_all_students(self):
        if not self.student_list:
            print("No students in the list")
        else:
            for student in self.student_list:
                student.display()
        
s=StudentManagementSystem()

while(True):
    print("\n1. Add student \n2. Delete student \n3. Search student \n4. Display student list \n5. Exit")
    op = int(input("Enter your choice: "))
    print("\n")

    match op:
        case 1:
            s.add_student()
        case 2:
            s.delete_student()
        case 3:
            s.search()
        case 4:
            print(s.display_all_students())
        case 5:
            break
