def remove_letters_in_string(string):
    string = string.replace(" ", "")
    for letter in string:
        if letter == ",":
            string = string.split(",")
            string = string[0]
            break
        try:
            _ = int(letter)
        except:
            string = string.replace(letter, "", 1)
    return string


def price_adj(string1, string2):
    string1 = remove_letters_in_string(string1)
    string2 = remove_letters_in_string(string2)
    price = float(string1 + "." + string2)
    return price
