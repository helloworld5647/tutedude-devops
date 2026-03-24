filename = "students_info.txt"
with open(filename, "r") as file:
    content = file.read()
print("File Contents:")
print("==============")
print(content)
