#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Missoes:
    def __init__(self):
        self.missoes_exterior = []
        self.missoes_brasil = []

    def __repr__(self):
        return """\t\tMissões Exterior: {self.missoes_exterior}
              Missões Brasil: {self.missoes_brasil}""".format(self=self)

    def toJSON(self):
        return self.__dict__
