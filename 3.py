filename = "students_info.txt"
with open(filename, "w") as file:
    file.write("Student Information\n")
    file.write("===================\n")
    file.write("Name: Alice     Grade: A\n")
    file.write("Name: Bob       Grade: B\n")
    file.write("Name: Charlie   Grade: C\n")

print(f"Content written to '{filename}' successfully!")
