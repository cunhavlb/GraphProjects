from bibgrafo.grafo_errors import *
from bibgrafo.grafo_lista_adj_nao_dir import GrafoListaAdjacenciaNaoDirecionado


class MeuGrafo(GrafoListaAdjacenciaNaoDirecionado):
    def vertices_nao_adjacentes(self):
        """
        Provê um conjunto de vértices não adjacentes no grafo.
        O conjunto terá o seguinte formato: {X-Z, X-W, ...}
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Um objeto do tipo set que contém os pares de vértices não adjacentes
        """
        vertices_adj = set()
        for a in self.arestas.values():
            vertices_adj.add(f"{a.v1.rotulo}-{a.v2.rotulo}")
            vertices_adj.add(f"{a.v2.rotulo}-{a.v1.rotulo}")

        combinacoes = set()
        for v1 in range(len(self.vertices)):
            for v2 in range(v1 + 1, len(self.vertices)):
                combinacoes.add(
                    f"{self.vertices[v1].rotulo}-{self.vertices[v2].rotulo}"
                )

        vna = set()
        for i in combinacoes:
            if i not in vertices_adj:
                vna.add(i)
        return vna

    def ha_laco(self):
        """
        Verifica se existe algum laço no grafo.
        return Um valor booleano que indica se existe algum laço.
        """
        for a in self.arestas.values():
            if a.v1.rotulo == a.v2.rotulo:
                return True
        return False

    def grau(self, V=""):
        """
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        """
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError
        grau = 0
        for a in self.arestas.values():
            if a.v1.rotulo == V:
                grau += 1
            if a.v2.rotulo == V:
                grau += 1
        return grau

    def ha_paralelas(self):
        """
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        """
        pares_vistos = set()
        for a1 in self.arestas.values():
            par = (a1.v1.rotulo, a1.v2.rotulo)
            if not par in pares_vistos:
                pares_vistos.add(par)
            else:
                return True
        return False

    def arestas_sobre_vertice(self, V):
        """
        Provê uma lista que contém os rótulos das arestas que incidem sobre o vértice passado como parâmetro
        :param V: Um string com o rótulo do vértice a ser analisado
        :return: Uma lista os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        """
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError
        arestas = set()
        for a in self.arestas.values():
            if a.v1.rotulo == V or a.v2.rotulo == V:
                arestas.add(a.rotulo)
        return arestas

    def eh_completo(self):
        """
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        """
        if (
            not self.ha_paralelas()
            and not self.ha_laco()
            and not self.vertices_nao_adjacentes()
        ):
            return True
        return False

    def eh_conexo(self):
        """
        Verifica se o grafo é conexo.
        :return: Um valor booleano que indica se o grafo é conexo
        """
        from collections import deque

        vertice_inicial = self.vertices[0].rotulo
        fila = deque([vertice_inicial])
        visitados = {vertice_inicial}

        # bfs implementation
        while fila:
            vertice_atual = fila.popleft()

            for aresta in self.arestas.values():
                vizinho = None
                if aresta.v1.rotulo == vertice_atual:
                    vizinho = aresta.v2.rotulo
                elif aresta.v2.rotulo == vertice_atual:
                    vizinho = aresta.v1.rotulo

                if vizinho and vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)

        if len(visitados) == len(self.vertices):
            return True
        else:
            return False

    def ha_ciclo(self):
        """
        Verifica se o grafo contém um ciclo.
        :return: Um valor booleano que indica se o grafo contém um ciclo
        """
        visitados = set()

        def dfs_haciclo(vertice, vertice_pai):
            visitados.add(vertice)
            for a in self.arestas.values():
                vizinho = None
                if a.v1.rotulo == vertice:
                    vizinho = a.v2.rotulo
                elif a.v2.rotulo == vertice:
                    vizinho = a.v1.rotulo
                if vizinho and vizinho not in visitados:
                    if dfs_haciclo(vizinho, vertice):
                        return True
                elif vizinho and vizinho != vertice_pai:
                    return True
            return False

        for v in self.vertices:
            v = v.rotulo
            if v not in visitados:
                if dfs_haciclo(v, None):  # <--- Dispara para cada componente isolada
                    return True
        return False

    def eh_arvore(self):
        """
        Verifica se o grafo é uma árvore.
        :return: Um valor booleano que indica se o grafo é uma árvore
        se for, retorna a quantidade de nos folhas
        """
        if not self.eh_conexo() or self.ha_ciclo():
            return False

        folhas = 0
        for v in self.vertices:
            if self.grau(v.rotulo) == 1:
                folhas += 1
        return folhas

    def eh_bipartido(self):
        """
        Verifica se o grafo é bipartido.
        """
        cores = {}

        def dfs_bipartido(vertice, cor):
            cores[vertice] = cor
            for a in self.arestas.values():
                vizinho = None
                if a.v1.rotulo == vertice:
                    vizinho = a.v2.rotulo
                elif a.v2.rotulo == vertice:
                    vizinho = a.v1.rotulo
                if vizinho and vizinho not in cores:
                    if not dfs_bipartido(vizinho, not cor):
                        return False
                elif vizinho and vizinho in cores and cor == cores[vizinho]:
                    return False
            return True

        for v in self.vertices:
            v = v.rotulo
            if v not in cores:
                if not dfs_bipartido(v, True):
                    return False
        return True
