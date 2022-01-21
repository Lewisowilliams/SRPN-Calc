# boolean values for keeping track of if the input is currently a comment both when chekcing the validity of the input
# and when carrying out the calculations

comment = False
valid_comment = False

# list of randomly generated numbers to be used when r is inputted to the calculator
rand = [20575256, 83543830, 83699772, 60665288, 47198772, 92043228, 50442365, 78371521, 38299641, 12967513, 37380783,
        41188267, 81273155, 81756249, 7644557, 92913585, 58719685, 69938744, 16523244, 17410170, 9752420, 51361532,
        28603739, 13425922, 91307539, 8073035, 42682082, 87027631, 28546682, 20032166, 13557614, 22017545, 87727508,
        77673762, 86392028, 81623451, 32847571, 40285417, 65425817, 28670057, 914918, 26788717, 20498630, 43184917,
        92730190, 79177291, 15929300, 72032755, 4548140, 97820333, 88509678, 73196822, 47345532, 14051510, 57512321,
        25972881, 42554085, 20984661, 85568667, 37352363, 32310928, 4643608, 83351276, 59405999, 58930675, 34848543,
        41754372, 95353975, 71231546, 74726339, 53186982, 10028314, 14107037, 75497456, 26665339, 39043157, 39879340,
        88704679, 72514184, 8090302, 59594070, 70187431, 63799848, 57210259, 93431427, 30499544, 92815649, 61534891,
        86950302, 39176940, 72858094, 80128002, 85871565, 83446416, 26003720, 92741022, 73302887, 74963055, 38606950]

# index for moving through the random number list to add a different random number each time
r_index = 0

# initialise operand_stack, a list to which all inputted numbers will be add as well as any results from calculations
operand_stack = []

# state all possible operators and ints so that the format_input function can correctly space out the input
operators = ["+", "-", "/", "*", "%", "d", "^", "r", "#", "^", "="]
ints = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]


# format_input function for formatting any input so that it is correctly spaced out and operations can be
# easily carried out
def format_input(s):
    # initialise a new string that will be correctly spaced
    new_string = ""

    # for each character in the orginal input, add it to the new string and ensure it is spaced correctly
    for ltr in s:
        # if the string is empty add i
        if new_string == "":
            new_string += ltr
        # if i == = and the last char of new_string is an operator
        elif ltr == "=" and new_string[-1] in operators:
            new_string += ltr
        # if the last char of the string is an operator (but not "-", to allow negative numbers) or unknown character
        # and i is not a space then add a space then i
        elif new_string[-1] not in ints and new_string[-1] != " " and ltr != " " and new_string[-1] != "-":
            new_string += " " + ltr
        # if i is an operator and there is no space before it, add one
        elif ltr in operators and new_string[-1] != " ":
            new_string += " " + ltr
        # ensure there is no double spacing
        elif ltr == " " and new_string[-1] == " ":
            pass
        # deal with unrecognised characters
        elif ltr not in operators and ltr not in ints and ltr != " ":
            if new_string[-1] == " ":
                new_string += ltr
            elif new_string[-1] != " ":
                new_string += " " + ltr
        # if i is a space and there is no space before it, add it
        else:
            new_string += ltr

    # strip any initial or trailing edges
    new_string.strip()
    # return a list to be used as input where the formatted string is separated by spaces
    return new_string.split(" ")


def make_valid(chars):
    # list verified characters
    accepted_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "+", "-", "/", "*", "%", "d", "^", "r", "#",
                      "=", ""]
    # global variable to determine if the input is valid
    global valid_comment

    for c in chars:
        # is a # is entered then any input until the next # is a comment and should be ignored
        if c == "#":
            valid_comment = not valid_comment
        # if it is not currently a comment then check that each input is a valid input
        if not valid_comment:
            for j in c:
                if j in accepted_chars:
                    pass
                # if it is not a valid input then
                else:
                    chars.remove(c)
                    print("Unrecognised operator or operand " + "\"" + j + "\"" + ".")


# check that the result is between the min and max integer values and then return the result to the operand stack
def check_saturation(result):
    # if the result of the operation is between the min and max int values then add the result to the operand stack
    if 2147483647 >= result >= -2147483648:
        operand_stack.append(int(result))
    # if the result is greater than the max integer value, append the max integer value to the operand_stack
    elif result >= 2147483647:
        operand_stack.append(2147483647)
    # if the result is less than the min integer value, append the min integer value to the operand_stack
    elif result <= -2147483648:
        operand_stack.append(-2147483648)


def calculation(input_list):

    global comment, r_index

    for i in input_list:

        # ensure the input is not currently a comment, if it is skip until another # is seen and it's no longer a
        # comment

        if i == "#":
            comment = not comment

        if not comment:

            # if the input contains and = then there are several possibilities for what should be outputted
            if "=" in i:
                # if the stack is empty print Stack Empty
                if i == "=" and len(operand_stack) == 0:
                    print("Stack empty.")
                # if an operator and = (i.e. + =) are entered and stack is empty print error message for both
                elif len(i) == 2 and i[0] in operators and len(operand_stack) == 0:
                    print("Stack empty. \nStack Underflow.")
                # if an operator and = are entered with no space in between (i.e. +=)
                # then return the peak of the stack but do not carry out the operation
                elif len(i) == 2 and i[0] in operators and len(operand_stack) == 1:
                    print(str(operand_stack[-1]) + "\nStack Underflow.")
                # if i == "=" and the operand stack is not empty then print the peak of the stack
                else:
                    print(operand_stack[-1])

            # if i is not in operators and it is not currently a comment then it must be an integer and should be
            # added to the stack
            elif i not in operators:
                # check that the operand stack is not full then convert i to an int
                # (so that operations can be carried out on it later) and add it to the stack
                try:
                    if len(operand_stack) <= 23:
                        operand_stack.append(int(i))
                # if the operand stack if full print stack overflow
                    else:
                        print("Stack Overflow.")
                # this except statement stop the programme from breaking if an int is entered and then deleted
                # after its been processed (this is only an issue in some IDEs)
                except:
                    pass

            # deal with special cases (d and r)

            # if d is inputted then simply print all digits in the operand stack
            elif i == 'd':
                for d in operand_stack:
                    print(d)
            # if r is inputted retrieve a number from the random number list and add it to the stack
            elif i == 'r':
                if len(operand_stack) <= 22:
                    operand_stack.append(rand[r_index])
                    r_index += 1
                else:
                    print("Stack Overflow.")
                    r_index += 1
            elif i == "#":
                pass

            # now deal with all operators
            else:
                # for each operator if there are less than 2 operands in the stack print Stack Underflow
                # if the operand stack is length 2 or greater then carry out the operation and
                # check its saturation (using check_saturation) before returning the result to the operand stack
                if len(operand_stack) <= 1:
                    print("Stack Underflow.")
                else:
                    # if the length of the stack is 2 or greater retrieve the top two elements from the stack
                    operand1 = operand_stack.pop()
                    operand2 = operand_stack.pop()

                    # carry out the calculation, then check its saturation before returning it to the stack
                    # (in check_saturation function)
                    if i == '+':
                        check_saturation(operand2 + operand1)

                    elif i == '-':
                        check_saturation(operand2 - operand1)

                    elif i == '/':
                        # check to ensure the program is not attempting to divide by 0
                        if operand1 == 0:
                            print("Divide by 0.")
                        else:
                            check_saturation(operand2 / operand1)

                    elif i == '*':
                        check_saturation(operand2 * operand1)

                    elif i == '%':
                        check_saturation(operand2 % operand1)

                    # if ^ is inputted the programme must first ensure operand1 is not negative,
                    # if it is then the operands should be returned to the stack
                    # if it is positive then the calculation can continue
                    elif i == '^':
                        if operand1 < 0:
                            print("Negative Power.")
                            operand_stack.append(operand2)
                            operand_stack.append(operand1)
                        else:
                            check_saturation(pow(operand2, operand1))


# main loop for taking input, formatting the input, removing invalid chars and then carrying out calculations
while True:

    # take an input
    inputted_chars = input()

    # ensure the input is correctly formatted
    formatted_input = format_input(inputted_chars)

    # ensure any unrecognised characters are flagged (error printed) and removed
    make_valid(formatted_input)

    # the input list has now had invalid characters removed and can be processed
    calculation(formatted_input)

#
# t-single : 9.5/10
# t-multiple : 7/10
# t-saturation : 6/10
# t-obscure : 6/10
#
# Running with expected input : 28.5/40
# Functionality mark to give : 36/50
#
# Well done for replicating so much of the legacy program's functionality. Some of the tests that did not pass include:
# Test the code with 3 3 * 4 4 * += d to see how this differs in the legacy program (Issue: spaces vs. no spaces between operators and operands).
# Saturation after calculation works but not on input. Entering 100000000000 d should read in using appropriate data type, cap at 2147483647, save to stack and print.
# Try the following input and see how it differs in the original calculator: 12515e252626+322e22fgh+d
# Obscure: The legacy calculator handles octal input (part of obscure functions). Numbers starting with 0, and containing solely values between 0-7, should be treated as octal (e.g. 01235 = 669 in decimal)
#
# The
# code is generally
# well
# written
# with good use of local variables and globals.Good commenting of code to help explain the functionality of the code
# written, but at times the commenting is overly verbose (no marks deducted just a note).Consistent code formatting
# throughout, with functions formatted well.Consistent naming throughout.Variables and functions are named well
# and capitalised correctly.However, the bulk of the code is within the calculate function.This code does a lot of
# work and hence there is some code repetition.For example, you check for Stack Overflow in two different places,
# if you had a function to deal with this then it would be easier for the code to change or be maintained.You could
# think about the functions you could create to reduce the size of this function.(30 / 50)