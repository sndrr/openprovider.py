# coding=utf-8

"""
Contains a Response class for representing responses from the API.
"""

import lxml
import lxml.objectify


class Response(object):
    """
    Represents a response from OpenProvider. Unwraps the code, desc and data
    fields in the response to attributes.
    """

    tree = None
    reply = None
    code = None
    desc = None
    data = None
    array = None

    def __init__(self, tree):
        self.tree = tree

        self.reply = self.tree.reply
        self.code = self.tree.reply.code
        self.desc = self.tree.reply.desc
        self.data = self.tree.reply.data

        try:
            self.array = self.tree.reply.array[0]
        except AttributeError as e:
            self.array = []

    def as_model(self, klass):
        """Turns a model-style response into a single model instance."""
        return klass(self.data)

    def as_models(self, klass):
        """Turns an array-style response into a list of models."""
        out = []
        try:
            for mod in self.tree.reply.data.results.array[0].item:
                out.append(klass(mod))
        except AttributeError as e:
            return []
        else:
            return out

    def __str__(self):
        return lxml.etree.tostring(self.tree, pretty_print=True)

    def dump(self):
        return lxml.etree.dump(self.tree)
