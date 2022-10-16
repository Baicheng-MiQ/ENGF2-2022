# >>> ord('a')
# 97
# >>> chr(97)
# 'a'
def any_ord_to_ascii_AZ(order: int) -> str:
    clean_order = order-65 # 0~large
    act_order = clean_order % 26
    ascii_order = act_order + 65
    return ascii_order


def break_cipher(text: str) -> str:
    possibilities = []
    for i in range(26):
        this_deci = ""
        for character in text:
            this_deci += chr(any_ord_to_ascii_AZ(ord(character)+i))
        possibilities.append(this_deci)
    
    for po in possibilities:
        print(po)
    
    note = """===This program prints all 26 offsets.
I don't think there is an easy way to 
design a program that automatically decide which 
of the 26 possible offsets is the correct one.
One possible solution to achieve this is to introduce
some text corpus, and use statistical approach to find
the offset which is most likely to produce valid English."""
    print(note)



if __name__ == "__main__":
    break_cipher("URYYB")

