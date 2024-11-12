import console_gfx
import math

def menu():
    print("RLE Menu")
    print("--------")
    print("0. Exit")
    print("1. Load File")
    print("2. Load Test Image")
    print("3. Read RLE String")
    print("4. Read RLE Hex String")
    print("5. Read Data Hex String")
    print("6. Display Image")
    print("7. Display RLE String")
    print("8. Display Hex RLE Data")
    print("9. Display Hex Flat Data")
    print()

#returns a hex string for an inputted list of numbers
def to_hex_string(data):
    result = ""
    hex_digits = "abcdef"

    #converts each number part of the list into its hexadecimal value
    for num in data:
        if num < 10:
            result += str(num)
        else:
            result += hex_digits[num - 10]

    return result

# return the number of runs(sets of 15) in a list
def count_runs(flat_data):
    count = 0
    current_run_length = 1

    #checks the list for runs by iterating through whole list
    for i in range(1, len(flat_data)):

        #checks if the run is still going
        if flat_data[i] == flat_data[i - 1]:
            current_run_length += 1
        else:
            if current_run_length > 0:
                count += 1
            current_run_length = 1

        #accounts for the fact that a single run maxes out at 15 characters
        if current_run_length >= 15:
            count += math.ceil(current_run_length / 15)
            current_run_length = 0

    #checks for the very last run
    if current_run_length > 0:
        count += 1

    #returns the length of encoded rle list
    return count

#converts a regular list of numbers into a rle encoded list of numbers
def encode_rle(flat_data):
    encoded_rle = []
    count = 1
    #checks for repeating numbers together and combines them in rle form
    for i in range(1, len(flat_data)):
        if flat_data[i] == flat_data[i - 1]:
            count += 1

            if count == 16:
                encoded_rle.append(15)
                encoded_rle.append(flat_data[i - 1])
                count = 1
        else:
            encoded_rle.append(count)
            encoded_rle.append(flat_data[i - 1])
            count = 1

    #append the last element
    encoded_rle.append(count)
    encoded_rle.append(flat_data[-1])
    return encoded_rle

#returns the decompressed size of an inputted rle list
def get_decoded_length(rle_data):
    length = rle_data[0]

    #adds up every other number in the rle encoded list
    for i in range(2, len(rle_data), 2):
        length += rle_data[i]

    return length

#takes the input of a rle list and returns the regular list of all the numbers
def decode_rle(rle_data):
    decoded_rle = []

    #adds each number to the list the number of times specified in the rle encoded list
    for i in range(0, len(rle_data), 2):
        decoded_rle.extend([rle_data[i + 1]] * rle_data[i])

    return decoded_rle

#takes in a hex string and returns the list of numbers either in rle form or raw form
def string_to_data(data_string):
    result = []
    hex_digits = "abcdef"

    #converts each hexadecimal number into a decimal number and adds it to the list
    for num in data_string:
        if num.isdigit():
            result.append(int(num))
        elif num in hex_digits:
            temp = 10 + hex_digits.index(num)
            result.append(temp)

    return result

def to_rle_string(rle_data):
    result = ""
    hex_digits = "abcdef"

    #adds each number to string of result converting every other number to a hexadecimal value starting with the second number of the list
    for i in range(0, len(rle_data) - 2, 2):
        result += str(rle_data[i])
        if rle_data[i + 1] < 10:
            result += str(rle_data[i + 1])
        else:
            result += hex_digits[rle_data[i + 1] - 10]
        result += ":"

    #accounts for the last set of numbers in list to add to string without adding a colon after
    result += str(rle_data[-2])
    if rle_data[-1] < 10:
        result += str(rle_data[-1])
    else:
        result += hex_digits[rle_data[-1] - 10]

    return result

def string_to_rle(rle_string):
    result = []
    hex_digits = "abcdef"

    #seperates the string into a list, removing all the colons
    segments = rle_string.split(":")

    #iterates through each new index of the list created
    for segment in segments:
        #checks if the value of the run is in hexadecimal and converts it to decimal if it is
        if segment[-1].lower() in hex_digits:
            run_character = int(10 + hex_digits.index(segment[-1].lower()))
        else:
            run_character = int(segment[-1])

        #removes the run character from the run length (segment)
        segment = segment[:-1]

        #converts any other hexadecimals to decimals
        if segment.lower() in hex_digits:
            segment = int(10 + hex_digits.index(segment.lower()))
        else:
            segment = int(segment)

        #adds run length and run character to list accordingly
        result.append(segment)
        result.append(run_character)

    return result

def main():
    print("Welcome to the RLE image encoder!")
    print()
    print("Displaying Spectrum Image:")
    console_gfx.display_image(console_gfx.test_rainbow)
    image_data = ""
    rle_string = ""
    rle_hex = ""
    flat_hex = ""
    print()

    while True:
        menu()
        User_choice = int(input("Select a Menu Option: "))
        if User_choice == 0: #exit
            quit()
        elif User_choice == 1: #load file
            filename = input("Enter name of file to load: ")
            image_data = console_gfx.load_file(filename)
            rle_image_data = encode_rle(image_data)
            rle_string = to_rle_string(rle_image_data)
            rle_hex = to_hex_string(rle_image_data)
            flat_hex = to_hex_string(image_data)
            print()
        elif User_choice == 2: #load test image
            image_data = console_gfx.test_image
            rle_image_data = encode_rle(image_data)
            rle_string = to_rle_string(rle_image_data)
            rle_hex = to_hex_string(rle_image_data)
            flat_hex = to_hex_string(image_data)
            print("Test image data loaded.")
            print()
        elif User_choice == 3: #read rle string
            rle_string = input("Enter an RLE string to be decoded: ")
            rle_list = string_to_rle(rle_string)
            flat_list = decode_rle(rle_list)
            rle_hex = to_hex_string(rle_list)
            flat_hex = to_hex_string(flat_list)
            print()
        elif User_choice == 4: #read rle hex string
            rle_hex = input("Enter the hex string holding RLE data: ")
            rle_list = string_to_data(rle_hex)
            rle_string = ':'.join(str(rle_list[i]) + (str(rle_list[i + 1]) if i + 1 < len(rle_list) else '') for i in range(0, len(rle_list), 2))
            print()
        elif User_choice == 5: #read data hex string
            flat_hex = input("Enter the hex string holding flat data: ")
            print()
        elif User_choice == 6: #display image
            print("Displaying image...")
            if image_data == "":
                print("(no data)")
            else:
                console_gfx.display_image(image_data)
            print()
        elif User_choice == 7: #display rle string
            if rle_string == "":
                print("RLE representation: (no data)")
            else:
                print(f"RLE representation: {rle_string}")
            print()
        elif User_choice == 8: #display hex rle data
            if rle_hex == "":
                print("RLE hex values: (no data)")
            else:
                print(f"RLE hex values: {rle_hex}")
            print()
        elif User_choice == 9: #display hex flat data
            if flat_hex == "":
                print("Flat hex values: (no data)")
            else:
                print(f"Flat hex values: {flat_hex}")
            print()
        else:
            print("Error! Invalid Input.")
            print()

if __name__ == "__main__":
    main()