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
