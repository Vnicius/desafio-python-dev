#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Proposicoes:
    def __init__(self):
        self.resumos = []
        self.materias = []

    def __repr__(self):
        return """\t\tResumos: {self.resumos}
                Materias: {self.materias}\n""".format(self=self)

    def toJSON(self):
        return self.__dict__
