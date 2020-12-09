def customizemessage(message):
    text_length = [0, 0, 0, 0]
    customized_message = ""

    lines = message.split("\n")

    for line in lines:
        texts = line.split('|')
        texts.pop()
        for text_index, text in enumerate(texts):
            if len(text) > text_length[text_index]:
                text_length[text_index] = len(text)

    for line in lines:
        texts = line.split('|')
        texts.pop()

        for text_index, text in enumerate(texts):
            if text_index > 0:
                customized_message += "  "

            if len(text) < text_length[text_index]:
                for _ in range(text_length[text_index] - len(text)):
                    text += ' '
            customized_message += text
            customized_message += "  |"
        customized_message += '\n'

    return customized_message


def bytetomb(size):
    return round(size / 1024 ** 2, 3)
