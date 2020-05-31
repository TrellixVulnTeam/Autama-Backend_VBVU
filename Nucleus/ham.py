"""
HAM = Human Autama Messaging

This file contains a class to handle conversing with an Autama.
"""

import torch

from itertools import chain
from Nucleus.interact import sample_sequence
from Nucleus.tools import read_pickle
from random import choice, seed


class Ham:
    def __init__(self, first_name: str, last_name: str, personality: list):
        # For creating a conversation environment
        self.__nucleus = read_pickle("nucleus.pickle")
        self.__args = self.__nucleus.get_args()
        self.__model = self.__nucleus.get_model()
        self.__tokenizer = self.__nucleus.get_tokenizer()
        # Autama's identifiers
        self.__first_name = first_name
        self.__last_name = last_name
        self.__full_name = first_name + " " + last_name
        self.__personality = personality # A list of interests
        # An identity is a list containing a name and a personality
        #self.__identity = self.__create_identity() # With four of the traits consisting of name
        self.__identity = self.__create_short_identity()
        self.__history = []
        # Messages for when user types in too much
        self.__error_messages = ["i'm here to have a conversation. not to read a book.",
                                 "i'm confused. can you give me a summary of what you just wrote? thanks!",
                                 "you lost me. can you give me a short version? thanks!",
                                 "i thought we were having a conversation. when did it become a lecture?",
                                 "gross. that is so much writing. just gross."]

    # A method that returns Autama's output by taking in user's input
    # https://github.com/huggingface/transfer-learning-conv-ai/blob/master/interact.py
    def converse(self, user_input: str):
        self.__history.append(self.__tokenizer.encode(user_input))
        user_input_length = len(self.__history[0])
        if user_input_length > 400:
            seed()
            output = choice(self.__error_messages)
            return output
        else:
            with torch.no_grad():
                out_ids = sample_sequence(self.__identity, self.__history, self.__tokenizer, self.__model, self.__args)
            self.__history.append(out_ids)
            self.__history = self.__history[-(2 * self.__args.max_history + 1):]
            nucleus_output = self.__tokenizer.decode(out_ids, skip_special_tokens=True)
            return nucleus_output

    # A method that checks if the user asks for the Autama's name and helps answer that question if needed
    def check_converse(self, user_input: str):
        name = self.__first_name
        response = self.converse(user_input)
        if "what is your name" in user_input or "your name?" in user_input:
            if name in response:
                return response
            else:
                return "my name is " + name
        elif "who are you" in user_input or "who dis" in user_input:
            if name in response:
                return response
            else:
                return "i'm " + name
        else:
            return response

    # A method to display the Autama's identity
    def display_identity(self):
        print("Identity: " + self.__tokenizer.decode(chain(*self.__identity)))

    # A method to tokenize and encode an identity
    # https://github.com/huggingface/transfer-learning-conv-ai/blob/master/utils.py
    def __tokenize_and_encode(self, identity: list):
        def tokenize(obj):
            if isinstance(obj, str):
                return self.__tokenizer.convert_tokens_to_ids(self.__tokenizer.tokenize(obj))
            if isinstance(obj, dict):
                return dict((n, tokenize(o)) for n, o in obj.items())
            return list(tokenize(o) for o in obj)

        return tokenize(identity)

    # A method to make sure all traits in personality are lower case
    def __format_personality(self):
        personality = self.__personality[:]
        personality = [trait.lower() for trait in personality]
        return personality

    # A method to create a list of introduction phrases
    def __create_intro(self, name: str):
        lower_name = name.lower()
        introduction1 = "my name is " + lower_name + "."
        introduction2 = 'i am ' + lower_name + "."
        introduction_list = [introduction1, introduction2]
        return introduction_list

    # A method to create an identity
    def __create_identity(self):
        full_introduction = self.__create_intro(self.__full_name)
        introduction = self.__create_intro(self.__first_name)
        personality = self.__format_personality()
        identity = full_introduction + introduction + personality
        return self.__tokenize_and_encode(identity)
    
    # A method to create an identity with just one trait for name
    def __create_short_identity(self):
        name = self.__first_name.lower()
        intro = ["my name is " + name + "."]
        personality = self.__format_personality()
        identity = intro + personality
        print(identity)
        return self.__tokenize_and_encode(identity)
