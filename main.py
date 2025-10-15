import json

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

    
    #return dictionary
    return {
        "total_upper_cases": total_upper_cases,
        "total_lower_cases": total_letters - total_upper_cases,
        "total_letters": total_letters,
        "total_lines": total_lines,
        "letter_counts": count_dict
    }



def case_distribution(line): #will be used later with matplotlib
    upper_case = 0

    for element in line: #checks each element in line
        for char in element: #check each char in element
            if char != char.lower(): #checks for uppercases
                upper_case += 1

    return upper_case



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
    return total_letters


#?pseudocode exporting data
# convert data to json/dictionary format
# export it to JSON

def export_data(stats_dict):
    with open("stats.json", "w") as file:
        json.dump(stats_dict, file, indent=4) #? json.dump() used to serialize a python dictionary into a JSON formatted string and write directly in a file

export_data(read_file())

    
        
