import json
import glob


def read_file(output):
    total_upper_cases = 0
    count_dict = dict()
    total_letters = 0
    total_lines = 0
    word_count_dict = dict()
    total_words = 0

    print(output)
    with open(f"{output}", "r", encoding="utf8") as file:
        for line in file: #read each line 1 by 1

            if line: #only works if line is not an empty array
                total_lines += 1
                total_letters = count_letters(line.lower(), count_dict, total_letters)
                total_upper_cases += case_distribution(line)
                total_words = number_of_words(line.lower(), word_count_dict, total_words)
    
    #return dictionary
    return {
        "total_upper_cases": total_upper_cases,
        "total_lower_cases": total_letters - total_upper_cases,
        "total_letters": total_letters,
        "total_lines": total_lines,
        "letter_counts": count_dict,
        "word_counts": word_count_dict,
        "total_words": total_words
    }



def number_of_words(line, word_count_dict, total_words):
    line = punctuation_remover(line)
    word_in_line = line.split() #creates a list of every word

    for word in word_in_line: #checks each word in the list
        if word in word_count_dict: #checks if word is in dictionary
            word_count_dict[word] += 1 
            total_words += 1
        else:
            word_count_dict[word] = 1 #adds word key to dictionary
            total_words += 1
    return total_words



def punctuation_remover(line):
    for char in line: #checks each character in line
        if char in '''~@#¤%^&*()_-+=<>?/,.;:!{}[]|'"''': #checks if character is a special character
            line = line.replace(char, ' ') #replaces special characters with a space
    return line



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


def enter_int():
    is_true = True


    while is_true:
        try:
            int_input = int(input("Enter input: "))
            if int_input > 0:
                return int_input
        except:
            print("Enter a valid number!")


#display text files
#make user be able to choose a text file
#return that text file to readfile()
#add option for exporting to json
#add option to read the file and return in console info

def file_menu():
    files = glob.glob("txtfiles/*.txt")

    print("================= Text Analysis Program =================\n")
    for index, file in enumerate(files, start=1): # enumerate - used for displaying elements in a list with an index aswell at the start
        print(f"{index}. {file}")

    return files[enter_int()]


#create menu with options
#when exporting data,

def menu():
    print("================= Text Analysis Program =================\n")

    print("1. Choose file")
    print("2. Display relevant statistics")
    print("3. Export data to JSON file")
    print("4. Show data in a graph")
    print("5. Exit program\n")

    
    
def main():
    is_running = True
    file = None
    data = None

    while is_running:
        menu()

        user_input = enter_int()
        
        if user_input == 1:
            file = file_menu()
        elif user_input == 2:
            data = read_file(file)

            for element in data: #displays data with key, value pairs
                print(f"{element}: {data[element]}")

        elif user_input == 3:
            print("Exporting data...")
            export_data(data)

        elif user_input == 5:
            print("Exiting program, see ya later!")
            is_running = False
        else:
            print("Not a valid input! Enter whats been listed")



main()