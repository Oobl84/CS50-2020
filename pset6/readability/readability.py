import string


def main():
    text = input("Text: ")

    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    let_per_hundw = (letters / words) * 100
    sen_per_hundw = (sentences / words) * 100

    index = round(0.0588 * let_per_hundw - 0.296 * sen_per_hundw - 15.8, 0)

    if index < 1:
        print("Before Grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


def count_letters(text):
    l_count = 0
    for letter in text:
        if letter not in string.punctuation and letter != " ":
            l_count += 1
    return l_count


def count_words(text):
    w_count = 0
    for word in text.split():
        if word not in string.punctuation:
            w_count += 1
    return w_count


def count_sentences(text):
    s_count = 0
    for char in text:
        if char in ['.', '!', '?']:
            s_count += 1
    return s_count


main()