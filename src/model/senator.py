#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Senator:
    def __init__(self):
        self.nome_parlamentar = ""
        self.nome_completo = ""
        self.perfil = ""
        self.partido = ""
        self.uf = ""
        self.periodo = ""
        self.telefones = ""
        self.fax = ""
        self.email = ""
        self.data_nascimento = ""
        self.naturalidade = ""
        self.gabinete = ""
        self.site = ""
        self.endereco_escritorio = ""
        self.chapa = []
        self.comissoes_atuais = []
        self.missoes = None
        self.historico_academico = []
        self.profissoes = []
        self.mandatos = []
        self.pronunciamentos = []
        self.materias_ralatadas = []

    def __repr__(self):
        return """\t\tNome: {self.nome_parlamentar}
                Nome Completo: {self.nome_completo}
                Perfil: {self.perfil}
                Partido: {self.partido}
                UF: {self.uf}
                Periodo: {self.periodo}
                Telefones: {self.telefones}
                E-mail: {self.email}
                Data de Nascimento: {self.data_nascimento}
                Naturalidade: {self.naturalidade}
                Gabinete: {self.gabinete}
                Site: {self.site}
                Esritorio: {self.endereco_escritorio}
                Fax: {self.fax}
                Chapa: {self.chapa}
                Comissões Atuais: {self.comissoes_atuais}
                Histórico Acadêmico: {self.historico_academico}
                Profissões: {self.profissoes}
                Mandatos: {self.mandatos}\n""".format(self=self)

    def toJSON(self):
        return self.__dict__
