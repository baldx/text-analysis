import json
import glob


def read_file(output):
    count_dict = dict()
    top_10_words = dict()
    word_count_dict = dict()

    total_upper_cases = 0
    total_letters = 0
    total_lines = 0
    total_words = 0
    total_sentences = 0
    
    longest_sentence = ""
    shortest_sentence = "sigma"*10 
    #placeholder rather than having an extra if statement which will use more power when comparing a whole file

    with open(f"{output}", "r", encoding="utf8") as file:
        for line in file: #read each line 1 by 1

            if line: #only works if line is not an empty array
                total_lines += 1
                total_letters = count_letters(line.lower(), count_dict, total_letters)
                total_upper_cases += case_distribution(line)
                total_words = number_of_words(line.lower(), word_count_dict, total_words)
                ten_words(word_count_dict, top_10_words)
                longest_sentence, shortest_sentence, total_sentences = find_sentences(longest_sentence, shortest_sentence, total_sentences, line)

    #return dictionary
    return {
        "total_upper_cases": total_upper_cases,
        "total_lower_cases": total_letters - total_upper_cases,
        "total_letters": total_letters,
        "total_lines": total_lines,
        "letter_counts": count_dict,
        "total_words": total_words,
        "longest_sentence": longest_sentence,
        "shortest_sentence": shortest_sentence,
        "total_sentences": total_sentences,
        "average_word_per_sentence": round(total_words / total_sentences, 2),
        "average_word_per_line": round(total_words / total_lines, 2),
        "word_counts": word_count_dict,
        "top_10_words": top_10_words,
    }


def ten_words(word_count_dict, top_10_words):
    sorted_word_count = sorted(word_count_dict.items(), key=lambda item: item[1], reverse = True) #creates a tuple sorted by element 1(value) from high to low
    sorted_word_count = sorted_word_count[ : 10] #slicesk the first 10 elements

    for word, value in sorted_word_count: #loops through the tuples and stores the key and values in word and value
        top_10_words[word] = value




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

#?longest sentences
#go through each line in a text file
#count total words in that line
#when largest sentences compares to something longer, update variable and save sentence

def find_sentences(longest_sentence, shortest_sentence, total_sentences, line):
    total_words_in_sentence = ""


    for char in line:
        if char in ".!?": #check for if char is one of the puncuation
            sentence = total_words_in_sentence.strip()

            if sentence: #checks if sentence is not an empty string
                total_sentences += 1

                if len(sentence) > len(longest_sentence): #if a sentence is larger than largest sentence, upddate
                    longest_sentence = total_words_in_sentence

                if len(sentence) < len(shortest_sentence): #if a sentence is smaller than smallest sentence, upddate
                    shortest_sentence = sentence
                total_words_in_sentence = ""
        else:
            total_words_in_sentence += char


    return longest_sentence, shortest_sentence, total_sentences

        


#?pseudocode exporting data
# convert data to json/dictionary format
# export it to JSON

def export_data(stats_dict):
    with open("stats.json", "w") as file:
        json.dump(stats_dict, file, indent=4) #? json.dump() used to serialize a python dictionary into a JSON formatted string and write directly in a file


def enter_int(): #error handling to input only int
    is_true = True


    while is_true:
        try:
            int_input = int(input("Enter input: ")) 
            return int_input
        except:
            print("Enter a valid number!")

#?Pseudocode
#display text files
#make user be able to choose a text file
#return that text file to readfile()
#add option for exporting to json
#add option to read the file and return in console info

def file_menu():
    files = glob.glob("txtfiles/*.txt")
    is_running = True

    print("================= Text Analysis Program =================\n")
    for index, file in enumerate(files, start=1): # enumerate - used for displaying elements in a list with an index at the start
        print(f"{index}. {file}")


    if len(files) == 0: #error handling for no files found
        print("No textfiles found :'(")
        return #break loop

    while is_running:
        try:
            user_input = enter_int()
            if user_input > 0 and user_input <= len(files): #error handling to choose a valid existing file
                return files[user_input - 1]
            else:
                raise #generate an error so it hops to except block
        except:
            print("Not a valid input. Please select one of the text files!")


def menu():
    print("================= Text Analysis Program =================\n")

    print("1. Choose file")
    print("2. Display relevant statistics")
    print("3. Export data to JSON file")
    print("4. Show data in a graph")
    print("5. Compare 2 files")
    print("6. Exit program\n")

def stats_menu(data):
    is_running = True
    keys_list = list(data.keys()) #adds all keys in a key

    while is_running:
        print("What would you like to see?")

        for index, element in enumerate(data, start=1): #prints a list with numbers in the console starting from 1
            print(f"{index}. {element}")
            if index == len(data):
                print(f"{index + 1}. Go back")
        
        user_input = enter_int() - 1
        if user_input >= 0 and user_input <= len(data): #check if input is in bound

            if user_input != len(data): 
                print(f"{keys_list[user_input]}: {data[keys_list[user_input]]}") #print the chosen data
            elif user_input == len(data): #exit program
                is_running = False

        else: #error message
            print("Not a valid input, enter an input within bounds")





#function for displaying results of difference of different statistics
def calculate_case_difference(x, y, file_1, file_2):
    if x > y:
        return f"File {file_1} has {x - y} more upper case letters than {file_2}"
    elif y > x:
        return f"File {file_2} has {y - x} more upper case letters than {file_1}"
    else:
        return "Both files have the same amount of upper case letters"

def calculate_letter_difference(x, y, file_1, file_2):
    if x > y:
        return f"File {file_1} has {x - y} more letters than {file_2}"
    elif y > x:
        return f"File {file_2} has {y - x} more letters than {file_1}"
    else:
        return "Both files have the same amount of letters"
    
def calculate_line_difference(x, y, file_1, file_2):
    if x > y:
        return f"File {file_1} has {x - y} more lines than {file_2}"
    elif y > x:
        return f"File {file_2} has {y - x} more lines than {file_1}"
    else:
        return "Both files have the same amount of lines"

def calculate_words_difference(x, y, file_1, file_2):
    if x > y:
        return f"File {file_1} has {x - y} more words than {file_2}"
    elif y > x:
        return f"File {file_2} has {y - x} more words than {file_1}"
    else:
        return "Both files have the same amount of words"

def calculate_sentence_difference(x, y, file_1, file_2):
    if x > y:
        return f"File {file_1} has {x - y} more sentences than {file_2}"
    elif y > x:
        return f"File {file_2} has {y - x} more sentences than {file_1}"
    else:
        return "Both files have the same amount of sentences"

#function for displaying compared files
def compare_files(file_1, file_2):
    file_1_stats = read_file(file_1)
    file_2_stats = read_file(file_2)

    print("Relevant statistics for the files:")
    
    print(calculate_case_difference(file_1_stats["total_upper_cases"], file_2_stats["total_upper_cases"], file_1, file_2)) #print difference
    print(calculate_letter_difference(file_1_stats["total_letters"], file_2_stats["total_letters"], file_1, file_2)) #print difference
    print(calculate_line_difference(file_1_stats["total_lines"], file_2_stats["total_lines"], file_1, file_2)) #print difference
    print(calculate_words_difference(file_1_stats["total_words"], file_2_stats["total_words"], file_1, file_2)) #print difference
    print(calculate_sentence_difference(file_1_stats["total_sentences"], file_2_stats["total_sentences"], file_1, file_2)) #print difference



    
def main():
    is_running = True
    file = None
    data = None
    file_1 = None
    file_2 = None

    while is_running:
            
        menu()

        user_input = enter_int()
        
        if user_input == 1:
            file = file_menu()

        elif user_input == 2 and file:
            data = read_file(file)

            stats_menu(data)


            #for element in data: #displays data with key, value pairs
            #    print(f"{element}: {data[element]}")

        elif user_input == 3 and file:
            print("Exporting data...")
            export_data(data)

        #!display diagrams with matplotlib later
        
        #comparing files
        elif user_input == 5:
            print("Choose your first file!")
            file_1 = file_menu()

            print("Choose your second file!")
            file_2 = file_menu()

            compare_files(file_1, file_2)


        elif user_input == 6:
            print("Exiting program, see ya later!")
            is_running = False

        elif file == None:
            print("Choose a file")

        else:
            print("Not a valid input! Enter what has been listed")


main()