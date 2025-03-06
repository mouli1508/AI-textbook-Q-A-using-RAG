import tiktoken


class Utils:
    def __init__(self):
        pass

    def count_number_of_tokens(self, text):
        encoding = tiktoken.encoding_for_model("gpt-4o-mini")
        tokens = encoding.encode(text)
        return len(tokens)

    def count_number_of_characters(self, text):
        return len(text)
