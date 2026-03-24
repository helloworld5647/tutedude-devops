students = {}
while True:
    print("\n===== Student Grade Menu =====")
    print("1. Add a new student")
    print("2. Update an existing student's grade")
    print("3. Print all student grades")
    print("4. Exit")
    choice = input("Enter your choice (1-4): ")
    if choice == "1":
        name = input("Enter student name: ")
        if name in students:
            print(f"Student '{name}' already exists. Use option 2 to update.")
        else:
            grade = input(f"Enter grade for {name}: ")
            students[name] = grade
            print(f"Student '{name}' added with grade '{grade}'.")
    elif choice == "2":
        name = input("Enter student name to update: ")
        if name in students:
            grade = input(f"Enter new grade for {name}: ")
            students[name] = grade
            print(f"Grade for '{name}' updated to '{grade}'.")
        else:
            print(f"Student '{name}' not found.")
    elif choice == "3":
        if students:
            print("\n--- Student Grades ---")
            for name, grade in students.items():
                print(f"{name} : {grade}")
        else:
            print("No students found.")
    elif choice == "4":
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please enter 1-4.")
