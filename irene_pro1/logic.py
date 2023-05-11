import pyperclip as copier
def separate(numbers):
    floating = []
    new_str = ""
    float_pos = 0
    decision = ""
    sign_negative = ""
    str_num = str(numbers)
    listed = [i for i in str_num]
    original = listed

    try:
        if "." in str_num:
            float_pos += original.index(".")
            decision += "point"
            floating = listed[float_pos:]
        if "-" in str_num:
            listed.remove("-")
            sign_negative += "negative"

    except Exception:
        pass

    if decision == "point":
        listed = listed[:float_pos]

    if len(listed) > 3 and len(listed) < 7:
        try:
            position = len(listed) - 3
            listed.insert(position, " ")
        except Exception:
            pass

    elif len(listed) == 7:
        listed.insert(1, " ")
        listed.insert(5, " ")

    elif len(listed) == 8:
        listed.insert(2, " ")
        listed.insert(6, " ")

    elif len(listed) == 9:
        listed.insert(3, " ")
        listed.insert(7, " ")

    if sign_negative == "negative":
        new_str += "-"
    for j in listed:
        new_str += j
    if len(floating) > 0:
        for k in floating:
            new_str += k
    return new_str

def clipboard(data = None, action = None):
    if action == "copy" and data:
        copier.copy(data)
    elif action == "paste":
        return copier.paste()