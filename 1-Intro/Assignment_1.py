import re
# Part A: Find a list of all of the names in the following string using regex.
def names():
    simple_string = """Amy is 5 years old, and her sister Mary is 2 years old. 
    Ruth and Peter, their parents, have 3 kids."""

    # All names start with a capital letter. 
    # Find all words that begin with a capital letter
    names = re.findall('[A-Z]{1}[a-z]+', simple_string)
    return names

#print(names())

# Part B: Create a regex to generate a list of just those students who received a B in the course.
def grades():
    with open ("1_Intro/assets/grades.txt", "r") as file:
        grades = file.read()

    # All students got a B has ": B"
    students = re.findall('([A-Z]{1}[a-z]+\s[A-Z]{1}[a-z]+)(?=\:\sB)', grades)
    return students

# print(grades())

# Part C: Convert Log File into a list of dictionaries
def logs():
    with open("1_Intro/assets/logdata.txt", "r") as file:
        logdata = file.read()

    loglines = logdata.split("\n") # Split by line
    logs = [] # Create output list
    for line in loglines[:-1]: # Exclude final blank line of file
        # Use REGEX to pick out host, user_name, time and request
        host = re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line).group() # IP Address format
        user_name = re.search('(?<=\s\-\s)([a-z0-9\-]+)', line).group() # Start with ' - '
        time = re.search('(?<=\[)(.+)(?=\])', line).group() # Between []
        request = re.search('(?<=\")(.+)(?=\")', line).group() # Between ""

        # Create dictionary record
        record = {"host": host, "user_name": user_name, "time": time, "request": request}

        # Append record to list
        logs.append(record)

    return logs

# print(logs()[0])
