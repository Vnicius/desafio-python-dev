#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import json
import requests
from bs4 import BeautifulSoup
from model.senator import Senator
from model.chapa import Chapa
from model.comissao import Comissao
from model.missoes import Missoes
from model.missao import Missao
from model.academico import Academico
from model.profissao import Profissao
from model.mandato import Mandato
from model.proposicoes import Proposicoes
from model.resumo import Resumo
from model.materia import Materia
from model.pronunciamento import Pronunciamento
from jsonEncoder import JSONEncoder


class SenatorsScrapper:
    def __init__(self):
        self.base_url = "https://www25.senado.leg.br/web/senadores/em-exercicio"
        self.data = []

    def export_to_JSON(self, file_name):
        """
        Exportar os dados para um arquivo .json

        Parameters
        ___
        file_name: String
            Nome do arquivo
        """

        with open("{}.json".format(file_name), "w", encoding="utf-8") as f:
            f.write(json.dumps([senator.toJSON() for senator in self.data],
                               cls=JSONEncoder, ensure_ascii=False, sort_keys=True))

    def get_data(self):
        """
        Pegar os dados dos senadores em exercício

        Returns
        ___
        Senator[]
            Array com os dados dos senadores
        """
        soup = None
        senators = None

        try:
            # pegar o HTML da primeira página
            response = requests.get(self.base_url)

            # usar o Beautiful Soup no HTML
            soup = BeautifulSoup(response.text, "lxml")
        except:
            raise "Request error!"

        # pegar os dados dos senadores
        senators = self.__get_all_senators(soup)
        self.data = senators

        return senators

    def __get_all_senators(self, soup):
        """
        Pegar todos os dados

        Parameters
        ___
        soup: BeautifulSoup
            objeto BeautifulSoup da página

        Returns
        ___
        Senator[]
            Array de objetos Senator

        """

        # pegar as linhas da tabela com dados
        rows = soup.find(
            "table", {"id": "senadoresemexercicio-tabela-senadores"}).find("tbody").find_all("tr", {"class": ""})

        senators = []

        for row in rows:
            # criat novo objeto Senator
            senator = Senator()

            # pegar as colunas da linha
            columns = row.find_all("td")

            if len(columns):

                # pegar os dados da tabela inicial
                senator.nome_parlamentar = columns[0].text
                senator.perfil = columns[0].find("a").get("href")
                senator.partido = columns[1].text
                senator.uf = columns[2].text
                senator.periodo = columns[3].text
                senator.telefones = columns[4].text
                senator.email = columns[5].text

                # pegar dados pessoais da página do perfil
                profile_page = requests.get(senator.perfil).text
                profile_soup = BeautifulSoup(profile_page, "lxml")
                personal_data = self.__get_senator_personal_data(
                    profile_soup)

                senator.nome_completo = personal_data["nome_civil"] if "nome_civil" in personal_data else ""
                senator.data_nascimento = personal_data[
                    "data_de_nascimento"] if "data_de_nascimento" in personal_data else ""
                senator.fax = personal_data["fax"] if "fax" in personal_data else ""
                senator.naturalidade = personal_data["naturalidade"] if "naturalidade" in personal_data else ""
                senator.gabinete = personal_data["gabinete"] if "gabinete" in personal_data else ""
                senator.site = personal_data["site_pessoal"] if "site_pessoal" in personal_data else ""
                senator.endereco_escritorio = personal_data[
                    "escritório_de_apoio"] if "escritório_de_apoio" in personal_data else ""

                # pegar dados adicionais da página do perfil
                senator.chapa = self.__get_chapa(
                    profile_soup)
                senator.comissoes_atuais = self.__get_comissoes(
                    profile_soup)
                senator.missoes = self.__get_missions(
                    profile_soup)
                senator.historico_academico = self.__get_academy_history(
                    profile_soup)
                senator.profissoes = self.__get_profissions(profile_soup)
                senator.mandatos = self.__get_mandatos(profile_soup)

                # pegar os dados da página de proposições
                senator.proposicoes = self.__get_proposicoes(profile_soup)

                # pegar os dados da página de matérias relatadas
                senator.materias_ralatadas = self.__get_materias_relatadas(
                    profile_soup)

                # pegar os dados da página de pronunciamentos
                senator.pronunciamentos = self.__get_pronunciamentos(
                    profile_soup)

            # adicionar o novo senador à lista
            senators.append(senator)
            if len(senators) == 1:
                break

        return senators

    def __get_senator_personal_data(self, soup):
        """
        Pegar os dados do página do perfil do senador

        Parameters
        ___
        soup: BeautifulSoup
            objeto BeautifulSoup da página

        Returns
        ___
        dict:
            Dicionário com os dados coletados
        """

        # busca o elemento com os dados
        personal_data = soup.find("dl", {"class": "dl-horizontal"})

        # lista com os elementos "dt" que seão o títulos
        dt = personal_data.find_all("dt")

        # lista com os elementos "dd" qie são os dados
        dd = personal_data.find_all("dd")
        data = {}

        # criar uma lista com os títulos como chave e dado como o valor
        for t, d in zip(dt, dd):
            key = t.text.replace(":", "").lower().replace(" ", "_")

            if d.find("a"):
                value = d.find("a").get("href")
            else:
                value = d.text

            data[key] = value

        return data

    def __get_chapa(self, soup):
        """
        Pegar a lista da chapa do senador

        Parameters
        ___
        soup: BeautifulSoup
            objeto BeautifulSoup da página

        Returns
        ___
        Capa[]
            Array com os dados da chapa
        """

        # buscar tabela com os dados
        chapa = soup.find("table", {"title": "Chapa eleitoral do Senador"})

        # buscar linhas da tabela
        rows = chapa.find("tbody").find_all("tr")
        data = []

        # pegar os dados das linhas
        for row in rows:
            pessoa = Chapa()
            td = row.find_all("td")

            if len(td):
                pessoa.nome_parlamentar = td[0].text
                pessoa.nome_completo = td[1].text
                pessoa.chapa = td[2].text

            data.append(pessoa)

        return data

    def __get_comissoes(self, soup):
        """
        Pegar os dados das comições atuais do senador

        Parameters
        ___
        soup: BeautifulSoup
            objeto BeautifulSoup da página

        Returns
        ___
        Comissao[]
            Array com as comissões
        """

        # buscar tabela com as comissões
        comissoes = soup.find(
            "table", {"title": "Participação atual do Senador em Comissões"})

        # pegar linhas da tabela
        rows = comissoes.find("tbody").find_all("tr")
        data = []

        # pegar os dados da linha
        for row in rows:
            comissao = Comissao()
            td = row.find_all("td")

            if len(td):
                comissao.titulo = td[0].text
                comissao.url = td[0].find("a").get("href")
                comissao.data_inicio = td[1].text
                comissao.participacao = td[2].text

            data.append(comissao)

        return data

    def __get_missions(self, soup):
        """
        Pegar as missões do senador

        Parameters
        ___
        soup: BeautifulSoup
            objeto BeautifulSoup da página

        Returns
        ___
        Missoes:
            Objeto com as missões exercídas pelo senador
        """

        # buscar a tabela com as missões
        missoes_tables = soup.find("div", {"id": "missoes"})

        # buscar os títulos "Missão no Exterior" e "Missão no Brasil"
        titulos = missoes_tables.find_all("h3") if missoes_tables else []
        missoes_titulo = [title.text for title in titulos]

        # buscar os dados das tabelas
        tables = missoes_tables.find_all("tbody") if missoes_tables else None
        missoes = Missoes()

        # verificar se possui Missões no Exterior
        if "Missões no Exterior" in missoes_titulo:
            # pegar as linhas da primeira tabela
            rows = tables[0].find_all("tr")

            # pegar os dados das linhas
            for row in rows:
                td = row.find_all("td")
                missao = Missao()

                if len(td):
                    missao.evento = td[0].text
                    missao.periodo = td[1].text
                    missao.documento = td[2].text

                missoes.missoes_exterior.append(missao)

        # verificar se possui Missões no Brasil
        if "Missões no Brasil" in missoes_titulo:
            # buscar indíce da tabela
            index = 0 if "Missões no Brasil" in missoes_titulo[0] else 1

            # pegar as linhas da tabela
            rows = tables[index].find_all("tr")

            # pegar os dados das linhas
            for row in rows:
                td = row.find_all("td")
                missao = Missao()

                if len(td):
                    missao.evento = td[0].text
                    missao.periodo = td[1].text
                    missao.documento = td[2].text

                missoes.missoes_brasil.append(missao)

        return missoes

    def __get_academy_history(self, soup):
        """
        Pegar os dados do hitórico acadêmico

        Parameters
        ___
        soup: BeautifulSoup
            objeto BeautifulSoup da página

        Returns
        ___
        Academico[]:
            Array com os dados do histórico acadêmico
        """

        # buscar tabela com histórico acadêmico
        academy_history_table = soup.find(
            "table", {"title": "Histórico acadêmico do(a) senador(a)"})

        # verifica se a tabela foi encontrada
        if academy_history_table:
            # pegar as linhas da tabela
            academy_history = academy_history_table.find("tbody")
            rows = academy_history.find_all("tr")
            data = []

            # pegar os dados das linhas
            for row in rows:
                td = row.find_all("td")
                academic = Academico()

                if len(td):
                    academic.curso = td[0].text
                    academic.grau = td[1].text
                    academic.estabelecimento = td[2].text
                    academic.local = td[3].text

                data.append(academic)

            return data

        return []

    def __get_profissions(self, soup):
        """
        Pegar as profissões do senador

        Parameters
        ___
        soup: BeautifulSoup
            objeto BeautifulSoup da página

        Returns
        __
        Profissao[]:
            array com as profissões
        """

        # buscar o elemento com os dados biográficos
        bibliography_data = soup.find(
            "div", {"id": "accordion-biografia"})

        # pegar a lista de profissões
        profissions_list = bibliography_data.find_all("li")

        # verifica se possui profissões
        if len(profissions_list):
            data = []

            for profission in profissions_list:
                prof = Profissao()
                prof.nome = profission.text

                data.append(prof)

            return data

        return []

    def __get_mandatos(self, soup):
        """
        Pegar os mandatos do senador

        Parameters
        ___
        soup: BeautifulSoup
            objeto BeautifulSoup da página

        Returns
        ___
        Mandato[]:
            array com os mandatos
        """

        # buscar tabela com os mandator
        mandatos_table = soup.find(
            "table", {"title": "Mandatos do(a) senador(a)"})

        # verificar se achou a tabela com os mandatos
        if mandatos_table:
            # pegar os dados da tabela
            mandatos_data = mandatos_table.find("tbody")
            rows = mandatos_data.find_all("tr")
            data = []

            # pegar os dados das linhas
            for row in rows:
                td = row.find_all("td")
                mandato = Mandato()

                if len(td):
                    mandato.cargo = td[0].text
                    mandato.inicio = td[1].text
                    mandato.fim = td[2].text

                data.append(mandato)

            return data

        return []

    def __get_proposicoes(self, soup):
        """
        Pegar proposições do senador

        Parameters
        ___
        soup: BeautifulSoup
            objeto BeautifulSoup da página

        Returns
        ___
        Proposicoes()
            objeto com os dados da página de promosições
        """

        # pegar a URL da página de proposições
        proposicoes_url = soup.find("a", {"title": "Proposições"}).get("href")
        response = requests.get(proposicoes_url)
        proposicoes_soup = BeautifulSoup(response.text, "lxml")

        # pegar os dados dos resumos
        abstracts = self.__get_abstracts(proposicoes_soup)

        # pegar os dados das materias
        materias = self.__get_materias(proposicoes_soup, proposicoes_url)
        proposicoes = Proposicoes()

        proposicoes.resumos = abstracts
        proposicoes.materias = materias

        return proposicoes

    def __get_abstracts(self, soup):
        """
        Pegar os resumos

        Parameters
        ___
        soup: BeautifulSoup
            objeto BeautifulSoup da página

        Returns
        ___
        Resumo[]
            array com os resumos da página
        """

        # buscar a tabela com os resumos
        abstract_table = soup.find("table")
        abstracts = []

        # verificar se achou a tabela
        if abstract_table:
            # pegar os dados da tabela
            rows = abstract_table.find("tbody").find_all("tr")

            # pegar os dados das linhas
            for row in rows:
                td = row.find_all("td")
                abstract = Resumo()

                if len(td):
                    abstract.titulo = td[0].text
                    abstract.url = td[0].find("a").get("href")
                    abstract.quantidade = td[1].text

                    abstracts.append(abstract)

        return abstracts

    def __get_materias(self, soup, page_url):
        """
        Pegar as materias das páginas

        Parameters
        ___
        soup: BeautifulSoup
            objeto BeautifulSoup da página
        
        page_url: String
            string da primeira página das materias

        Returns
        ___
        Materia[]
            array com todas as matírias do senador 
        """

        # buscar o elemento para a navegação das páginas
        pages = soup.find("div", {"class": "pagination"})

        # última página com as matérias
        last_page = pages.find_all("li")[-1].find("a")

        # URL da última página
        last_page_url = last_page.get("href") if last_page else page_url
        
        # pegar a quantidade de páginas com matérias
        quant_pages = int(
            re.search(r'p/\d+', last_page_url).group(0).replace("p/", ""))
        materias = []

        # pegar as matérias de cada página
        for p in range(quant_pages):
            actual_page = page_url[:-1] + str(p + 1)

            # pegar o html da página
            response = requests.get(actual_page)
            page_soup = BeautifulSoup(response.text, "lxml")
            materias = materias + self.__get_materias_page_data(page_soup)

        return materias

    def __get_materias_page_data(self, soup):
        """
        Pegar as materias de uma página

        Parameters
        ___
        soup: BeautifulSoup
            objeto BeautifulSoup da página

        Returns
        __
        Materia[]
            array com as materias da página
        """

        # buscar todos os elementos das matérias
        materias = soup.find_all(
            "dl", {"class": "dl-horizontal borda-pontilhada-base"})
        all_materias = []

        # pegar os dados das materias
        for materia in materias:
            dt = [item.text.replace(":", "").replace(" ", "").lower()
                  for item in materia.find_all("dt")]
            dd = materia.find_all("dd")
            data = {}

            for key, value in zip(dt, dd):
                data[key] = value

            mat = Materia()

            mat.titulo = data["matéria"].text if "matéria" in data else ""
            mat.url = data["matéria"].find("a").get(
                "href") if "matéria" in data else ""
            mat.ementa = data["ementa"].text if "ementa" in data else ""
            mat.autor = data["autor"].text.split(
                ", ") if "autor" in data else ""
            mat.data = data["data"].text if "data" in data else ""

            all_materias.append(mat)

        return all_materias

    def __get_pronunciamentos(self, soup):
        """
        Pegar os pronunciamentos

        Parameters
        ___
        soup: BeautifulSoup
            objeto BeautifulSoup da página

        Returns
        __
        Pronunciamento[]
            array com os pronunctiamentos do Senador
        """

        # pegar a url da página de pronunciamentos
        pronunciamentos_url = soup.find(
            "a", {"title": "Pronunciamentos"}).get("href")

        # acessar página de pronunciamentos
        response = requests.get(pronunciamentos_url)
        pronunciamentos_soup = BeautifulSoup(response.text, "lxml")
        
        # pegar a quantidade de páginas de pronunciamentos
        pages = pronunciamentos_soup.find(
            "div", {"class": "pagination pagination text-center"})
        last_page = pages.find_all("li")[-1].find("a").get("href")
        quant_pages = int(last_page.split("/")[-1])
        base_url = last_page[:-2]
        pronunciamentos = []

        # acessar todas as páginas de pronunciamento
        for index in range(quant_pages):
            page = base_url + "/" + str(index + 1)
            pronunciamentos = pronunciamentos + \
                self.__get_pronunciamentos_page(page)

        return pronunciamentos

    def __get_pronunciamentos_page(self, page_url):
        """
        Pegar os pronunciamentos de uma página

        Parameters
        ___
        page_url: BeautifulSoup
            url da página

        Returns
        __
        Pronunciamento[]
            array com os pronunciamentos da página
        """

        # pegar os dados da página
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "lxml")
        
        # buscar a tabela de dados
        pronunciamentos_table = soup.find(
            "table", {"class": "table table-striped"})
        pronunciamentos_data = pronunciamentos_table.find(
            "tbody") if pronunciamentos_table else None
        
        # pegar as linhas
        rows = pronunciamentos_data.find_all(
            "tr") if pronunciamentos_data else []
        pronunciamentos = []

        # pegar os dados de cada linha
        for row in rows:
            td = row.find_all("td")
            pronunciamento = Pronunciamento()

            if len(td):
                pronunciamento.data = td[0].text
                pronunciamento.tipo = td[1].text
                pronunciamento.casa = td[2].text
                pronunciamento.partido = td[3].text.split("/")[0]
                pronunciamento.uf = td[3].text.split("/")[1]
                pronunciamento.resumo = td[4].text

            pronunciamentos.append(pronunciamento)

        return pronunciamentos

    def __get_materias_relatadas(self, soup):
        """
        Pegar os dados da página de Matérias Relatadas

        Parameters
        ___
        soup: BeautifulSoup
            objeto BeautifulSoup da página

        Returns
        __
        Proposicoes[]
            array com as materias relatadas do Senador
        """

        # buscar a url da página de Matérias Relatadas
        materias_relatadas_url = soup.find(
            "a", {"title": "Materias Relatadas"}).get("href")
        
        # pegar os dados da página
        response = requests.get(materias_relatadas_url)
        materias_relatadas_soup = BeautifulSoup(response.text, "lxml")
        
        # pegar os resumos
        abstracts = self.__get_abstracts(materias_relatadas_soup)
        
        # pegar as materias
        materias = self.__get_materias(
            materias_relatadas_soup, materias_relatadas_url)
        materias_relatadas = Proposicoes()

        materias_relatadas.resumos = abstracts
        materias_relatadas.materias = materias

        return materias_relatadas


if __name__ == "__main__":
    scrapper = SenatorsScrapper()

    scrapper.get_data()
    scrapper.export_to_JSON("data")
