from bibgrafo.grafo_errors import *
from bibgrafo.grafo_lista_adj_dir import GrafoListaAdjacenciaDirecionado


class MeuGrafo(GrafoListaAdjacenciaDirecionado):
    def vertices_nao_adjacentes(self):
        """
        Provê um conjunto de vértices não adjacentes no grafo.
        O conjunto terá o seguinte formato: {X-Z, X-W, ...}
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Um objeto do tipo set que contém os pares de vértices não adjacentes
        """
        """
        vertices_adj = set()
        for a in self.arestas.values():
            vertices_adj.add(f"{a.v1.rotulo}-{a.v2.rotulo}")

        combinacoes = set()
        for v1 in range(len(self.vertices)):
            for v2 in range(len(self.vertices)):
                if v1 != v2:
                    combinacoes.add(
                        f"{self.vertices[v1].rotulo}-{self.vertices[v2].rotulo}"
                    )

        vna = set()
        for i in combinacoes:
            if i not in vertices_adj:
                vna.add(i)
        return vna
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
        :return: Um valor booleano que indica se existe algum laço.
        """
        for a in self.arestas.values():
            if a.v1.rotulo == a.v2.rotulo:
                return True
        return False

    def grau_entrada(self, V=""):
        """
        Provê o grau de entrada do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoError se o vértice não existe no grafo
        """
        if not self.existe_rotulo_vertice(V):
            raise VerticeInvalidoError
        grau = 0
        for a in self.arestas.values():
            if a.v2.rotulo == V:
                grau += 1
        return grau

    def grau_saida(self, V=""):
        """
        Provê o grau de saída do vértice passado como parâmetro
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

    def dijkstra(self, origem, destino):
        """
        Executa o algoritmo de Dijkstra para encontrar o caminho mais curto entre dois vértices.
        :param origem: Um string com o rótulo do vértice de origem
        :param destino: Um string com o rótulo do vértice de destino
        :return: Um dicionário que mapeia cada vértice ao seu predecessor no caminho mais curto
        :raises: VerticeInvalidoException se o vértice de origem ou destino não existe no grafo
        """
        import heapq
        # Se os vertices de origem e destino n existirem retorna erro
        if not self.existe_rotulo_vertice(origem) or not self.existe_rotulo_vertice(
            destino
        ):
            raise VerticeInvalidoError
        # seta as distancias iniciais como infinito usando uma gambiarra do python
        distancias = {v.rotulo: float("inf") for v in self.vertices}
        # seta a distancia da origem pra 0 pq estamos começando dela
        distancias[origem] = 0
        # inicializa a fila com o vertice de origem
        queue = [(0, origem)]
        predecessores = {}
        while queue:
            distancia_atual, vertice_atual = heapq.heappop(queue)
            if distancia_atual > distancias[vertice_atual]:
                continue

            if vertice_atual == destino:
                break

            for a in self.arestas.values():
                if a.v1.rotulo == vertice_atual:
                    vizinho = a.v2.rotulo
                    peso = a.peso
                    nova_distancia = distancia_atual + peso

                    if nova_distancia < distancias[vizinho]:
                        distancias[vizinho] = nova_distancia
                        heapq.heappush(queue, (nova_distancia, vizinho))
                        predecessores[vizinho] = vertice_atual

        if distancias[destino] == float("inf"):
            return float("inf"), []

        menor_caminho = []
        vertice = destino
        while vertice != origem:
            menor_caminho.append(vertice)
            vertice = predecessores[vertice]
        menor_caminho.append(origem)
        menor_caminho.reverse()
        return distancias[destino], menor_caminho
