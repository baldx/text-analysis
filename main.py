import json
import glob
import matplotlib.pyplot as plt


def read_file(output):
    count_dict = dict()
    top_10_words = dict()
    word_count_dict = dict()

    words_once = set()
    unique_words = set()

    total_upper_cases = 0
    total_letters = 0
    total_lines = 0
    total_words = 0
    total_sentences = 0
    sentiment = 0

    
    longest_sentence = ""
    shortest_sentence = "sigma"*10 
    current_sentence = ""

    #placeholder rather than having an extra if statement which will use more power when comparing a whole file

    with open(f"{output}", "r", encoding="utf8") as file:
        
        for line in file:
            if line: #only works if line is not an empty array
                total_lines += 1
                total_letters = count_letters(line.lower(), count_dict, total_letters)
                total_upper_cases += case_distribution(line)
                total_words = number_of_words(line.lower(), word_count_dict, total_words, unique_words)
                longest_sentence, shortest_sentence, total_sentences, current_sentence = find_sentences(longest_sentence, shortest_sentence, total_sentences, line, current_sentence)
    
    words_appearing_once(word_count_dict, words_once) #bring these functions outside so it updates once and not every iteration to save time
    ten_words(word_count_dict, top_10_words)
    sentiment = sentiment_counter(sentiment, word_count_dict)

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
        "words_appearing_once": words_once,
        "unique_words": unique_words,
        "average_letters_per_word": round(total_letters / total_words, 2),
        "average_word_per_sentence": round(total_words / total_sentences, 2),
        "average_word_per_line": round(total_words / total_lines, 2),
        "word_counts": word_count_dict,
        "top_10_words": top_10_words,
        "sentiment": sentiment
    }

def sentiment_counter(sentiment, word_count_dict):
    # sets for basic sentiment counter
    happy_words = (
    "glad", "lycklig", "fantastisk", "underbar", "härlig", "trevlig", "positiv", "kärleksfull",
    "snäll", "vacker", "rolig", "kul", "nöjd", "hoppfull", "inspirerande", "motiverad", "framgångsrik",
    "tacksam", "charmig", "briljant", "leende", "mysig", "trygg", "lugn", "harmonisk", "säker",
    "uppskattad", "älskad", "välsignad", "fri", "stark", "modig", "pigg", "energisk", "varm", "vänlig",
    "omtänksam", "hjälpsam", "lyckad", "positivt", "imponerande", "kreativ", "klok", "smart", "givande",
    "välmående", "betydelsefull", "motiverande", "upplyftande", "fantastisk", "imponerad",
    "tillfredsställd", "avslappnad", "bekväm", "underhållande", "hopp", "glädje", "styrka", "framgång",
    "framåt", "uppskattning", "skratt", "njutning", "solsken", "blomstrande", "strålande", "välkomnande",
    "festlig", "tacksamhet", "respektfull", "hederlig", "ärlig", "öppen", "rättvis", "lojal", "trogen",
    "pålitlig", "påhittig", "entusiastisk", "passionerad", "hoppfullhet", "kärlek", "tillgivenhet",
    "vänskap", "gemenskap", "förtroende", "stöd", "trygghet", "balans", "lugn", "fred", "glädjefull",
    "fantasifull", "inspirerad", "charmfull", "mod", "vilja", "kraft", "uppskattande", "nöje",
    "optimistisk", "drömmande", "hoppgivande", "positivism", "lyckorus", "tillfreds", "lycka",
    "stolt", "växande", "blommande", "skön", "ren", "ljus", "klar", "strålande", "livlig", "fest",
    "glädjeämne"
)

    sad_words = (
    "ledsen", "arg", "besviken", "ensam", "trött", "rädd", "orolig", "stressad", "irriterad",
    "deprimerad", "förvirrad", "tom", "sårad", "kall", "mörk", "eländig", "misslyckad", "värdelös",
    "hopplös", "bitter", "hatisk", "förbannad", "avundsjuk", "svag", "missnöjd", "besvärad", "orolig",
    "skamsen", "skyldig", "trasig", "sorgsen", "deppig", "ilsken", "arg", "tung", "sorglig", "dyster",
    "förlorad", "rädsla", "panik", "ångest", "skakad", "krossad", "ledsam", "frusen", "trist", "missmodig",
    "olycklig", "bortglömd", "ensamhet", "uttråkad", "missförstådd", "nedstämd", "pressad", "stress",
    "hat", "ilska", "förakt", "avsky", "tårar", "gråt", "smärta", "lidande", "bekymrad", "orolighet",
    "skam", "ångestfylld", "bruten", "uppgiven", "hopplöshet", "svek", "besvikelse", "förlust", "sorg",
    "oro", "tvivel", "rädsla", "osäker", "osäkerhet", "feg", "svaghet", "skadad", "tragedi", "död",
    "enslighet", "förtvivlad", "frustrerad", "förbannad", "arghet", "förtryckt", "plågad", "skadad",
    "förnedrad", "otrygg", "räddhågsen", "nedbruten", "utsliten", "enslig", "svekfull", "hård", "kallhjärtad",
    "bortstött", "förkastad", "avvisad", "ensamstående", "tyst", "sörjande", "kvävd", "lidande", "bortgång",
    "sjuk", "sårbar", "osedd", "obekväm", "melankolisk", "olycka", "sorglighet", "förtvivlan", "ångestfull"
)

    
    for element in word_count_dict:
        if element in happy_words:
            sentiment += word_count_dict[element]
            
        elif element in sad_words:
            sentiment -= word_count_dict[element]
    
    return sentiment



def ten_words(word_count_dict, top_10_words):
    sorted_word_count = []
    
    for word, value in word_count_dict.items(): #loops through all the words and values in the dictionary as a set. 
        sorted_word_count.append([value, word]) #adds the the set in the list and switches the word and 

    sorted_word_count.sort(reverse = True) #sorts the list from high to low
    sorted_word_count = sorted_word_count[ : 10] #slices the first 10
    
    for value, word in sorted_word_count: #loops through the tuples and stores the key and values in word and value
        top_10_words[word] = value


def words_appearing_once(word_count_dict, words_once):
    sorted_word_count = []
    for word, value in word_count_dict.items(): #loops through all the words and values in the dictionary as a set. 
        sorted_word_count.append([value, word]) #adds the the set in the list and switches the word and 

    sorted_word_count.sort() #sorts the list from low to high
    index = 0
    
    for value, word in sorted_word_count: #loops through the values and words in the list
        if value > 1: #checks if the word appears more than once
            break
        index += 1 #verifies where the loop is compared to the index of the list

    sorted_word_count = sorted_word_count[ : index] #slices the list where the value is more than one 
    
    for value, word in sorted_word_count: #loops through the words and values in the list
        words_once.add(word)


def number_of_words(line, word_count_dict, total_words, unique_words):
    line = punctuation_remover(line)
    word_in_line = line.split() #creates a list of every word

    for word in word_in_line: #checks each word in the list
        if word in word_count_dict: #checks if word is in dictionary
            word_count_dict[word] += 1 
            total_words += 1
        else:
            word_count_dict[word] = 1 #adds word key to dictionary
            unique_words.add(word) #adds unique word to a set
            total_words += 1
    return total_words



def punctuation_remover(line):
    for char in line: #checks each character in line
        if char in '''~@#¤%^&*()_-+=<>?/,.;:!{}[]—|'"''': #checks if character is a special character
            line = line.replace(char, ' ') #replaces special characters with a space
    return line

def visualize_data(upper_case, lower_case, top_10_word_count):


    fig, ax = plt.subplots(2, 2, figsize=(20, 8)) #creates a 2D array which is a 2x2 row and colomn grid for displaying charts
    #can adjust the dimensions later for more plots if needed
    
    #CASE DISTRIBUTION CHART

    ax[0, 0].pie( #ax[0,0] says choose the plot which is in the first row and first colomn
        [upper_case, lower_case],               # pass sizes as first arg (not sizes=)
        labels=["Upper case", "Lower case"],
        colors=["red", "blue"],
        autopct='%1.1f%%', #use percentages
        startangle=90 #rotate 90 degrees for nicer touch
    )

    ax[0, 0].set_title("Case Distribution (Pie)") #adds title for chart when ONLY using plt.subplots() otherwise when using plt.subplot(), setting titles with .title()

    #TOP 10 WORDS CHART

    letters = []
    values = []
    for element in top_10_word_count: #get the keys and values in their lists
        letters.append(element)
        values.append(top_10_word_count[element])
    ax[0, 1].bar(letters, values) #adds the letters as x values and the values to the letters as y values
    ax[0, 1].set_title("Most common words")


    plt.tight_layout() #adjust layout so titles dont overlap
    plt.show()
    
    



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

def find_sentences(longest_sentence, shortest_sentence, total_sentences, line, current_sentence):

    for char in line:

        if char in ".!?": #check for if char is one of the puncuation
            sentence = current_sentence.strip()

            if sentence: #checks if sentence is not an empty string
                total_sentences += 1

                if len(sentence) > len(longest_sentence): #if a sentence is larger than largest sentence, upddate
                    longest_sentence = current_sentence

                if len(sentence) < len(shortest_sentence): #if a sentence is smaller than smallest sentence, upddate
                    shortest_sentence = sentence
                current_sentence = ""
        else:
            current_sentence += char


    return longest_sentence, shortest_sentence, total_sentences, current_sentence

        


#?pseudocode exporting data
# convert data to json/dictionary format
# export it to JSON



def export_data(stats_dict):
    with open("stats.json", "w") as file:
        json.dump(stats_dict, file, indent=4, default=lambda o: list(o) if isinstance(o, set) else o) #? json.dump() used to serialize a python dictionary into a JSON formatted string and write directly in a file
    #default lambda line says when dumping to JSON, if you see a set, turn it into a list so JSON can handle it, if anything else just return it
    #it does it by using default which tells the program that if json.dump() encounters a data type which it doesnt know how to searlize
    #use lambda for creating an inline function (an anonymous function) that takes an argument and returns something, in this case a list if its a set and everything else return normally

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


        elif user_input == 3 and file:
            print("Exporting data...")
            if data:
                export_data(data)
            else:
                data = read_file(file)
                export_data(data)

        #Stuff to show:
        #upper case - lower case distribution with pie chart
        #top 10 words with diagram
        #most common letter
        #miscellaneous stuff such as:
            #total words
            #total sentences
            #total lines
            #total letters

        elif user_input == 4 and file:


            if data:
                visualize_data(data["total_upper_cases"], data["total_lower_cases"], data["top_10_words"])
            else:
                data = read_file(file)
                visualize_data(data["total_upper_cases"], data["total_lower_cases"], data["top_10_words"])
                    
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