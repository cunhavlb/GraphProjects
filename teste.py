from bibgrafo import grafo
from bibgrafo.grafo_lista_adj_nao_dir import GrafoListaAdjacenciaNaoDirecionado
from atividades_grafos import meu_grafo_lista_adj_nao_dir

g = GrafoListaAdjacenciaNaoDirecionado()

g.adiciona_vertice('J')
g.adiciona_vertice('C')
g.adiciona_vertice('E')
g.adiciona_vertice('P')
g.adiciona_vertice('M')
g.adiciona_vertice('T')
g.adiciona_vertice('Z')

g.adiciona_aresta('a1', 'J', 'C')
g.adiciona_aresta('a2', 'C', 'E')
g.adiciona_aresta('a3', 'C', 'E')
g.adiciona_aresta('a4', 'C', 'P')
g.adiciona_aresta('a5', 'C', 'P')
g.adiciona_aresta('a6', 'C', 'M')
g.adiciona_aresta('a7', 'C', 'T')
g.adiciona_aresta('a8', 'M', 'T')
g.adiciona_aresta('a9', 'T', 'Z')





ha_laco()