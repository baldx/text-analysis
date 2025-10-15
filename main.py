def read_file():
    total_upper_cases = 0
    count_dict = dict()
    total_letters = 0
    total_lines = 0
    with open("txtfiles/DenSistaTågresan.txt", "r", encoding='utf8') as file:
        for line in file: #read each line 1 by 1

            if line: #only works if line is not an empty array
                total_lines += 1
                total_letters = count_letters(line.lower(), count_dict, total_letters)
                total_upper_cases += case_distribution(line)

    #element 3, calculate total lower case letters
    return [total_upper_cases, count_dict, total_letters, total_letters - total_upper_cases, total_lines]



def case_distribution(line):
    upper_case = 0

    for element in line: #checks each element in line
        for char in element: #check each char in element
            if char != char.lower(): #checks for uppercases
                upper_case += 1

    return upper_case


def print_letters(count_dict):

    for i in count_dict:
        print(f'{i} appears {count_dict[i]} time(s)')



def count_letters(sentence, count_dict, total_letters):
    for character in sentence: #checks each element in line
        
        if character.isalpha() and character in count_dict: #checks for letters in dictionary
            count_dict[character] += 1
            total_letters += 1
        elif character.isalpha(): #checks for letters
            count_dict[character] = 1 #adds letter key to dictionary
            total_letters += 1

        if character in '!.?,' and character in count_dict: #checks for punctuation in dictionary
            count_dict[character] += 1
        elif character in '!.?,': #checks for punctuation
            count_dict[character] = 1 #adds punctuation key to dictionary




#pseudocode exporting data

def export_data(stats):
    with open("stats.txt", "w") as file:
        file.writelines(stats)
        
