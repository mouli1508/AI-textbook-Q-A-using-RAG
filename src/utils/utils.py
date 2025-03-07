import tiktoken
from pydantic import create_model
import inspect
from inspect import Parameter


class Utils:
    def __init__(self):
        pass

    def count_number_of_tokens(self, text):
        encoding = tiktoken.encoding_for_model("gpt-4o-mini")
        tokens = encoding.encode(text)
        return len(tokens)

    def count_number_of_characters(self, text):
        return len(text)

    def jsonschema(self, f):
        """
        Generate a JSON schema for the input parameters of the given function.

        Parameters:
            f (FunctionType): The function for which to generate the JSON schema.

        Returns:
            Dict: A dictionary containing the function name, description, and parameters schema.
        """
        kw = {n: (o.annotation, ... if o.default == Parameter.empty else o.default)
              for n, o in inspect.signature(f).parameters.items()}
        s = create_model(f'Input for `{f.__name__}`', **kw).schema()
        return dict(name=f.__name__, description=f.__doc__, parameters=s)
