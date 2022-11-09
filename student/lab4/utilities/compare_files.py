# compare_files.py
# Utility by THC to compare two text files to see whether they contain the same lines, in any order.

official_file_name = raw_input("Enter name of official file: ")
student_file_name = raw_input("Enter name of student file: ")
official_file = open(official_file_name, "r")
official_strings = []
for line in official_file:
    official_strings.append(line)
official_file.close()
student_file = open(student_file_name, "r")
student_strings = []
for line in student_file:
    student_strings.append(line)
student_file.close()

# Sort the two lists.
official_strings.sort()
student_strings.sort()

if len(official_strings) != len(student_strings):
    print "Lengths don't match: official = ", len(official_strings), ", student =", len(student_strings)
else:
    i = 0
    while i < len(official_strings):
        if official_strings[i] != student_strings[i]:
            print "Strings don't match at index", i, ": official = ", official_strings[i], "student = ", student_strings[i]
            break
        else:
            i += 1
            
    if i >= len(official_strings):
        print "Files match"