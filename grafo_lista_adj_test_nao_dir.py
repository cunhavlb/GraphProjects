import unittest

import gerar_grafos_teste
from bibgrafo.aresta import Aresta
from bibgrafo.grafo_builder import GrafoBuilder
from bibgrafo.grafo_errors import *
from bibgrafo.grafo_json import GrafoJSON
from bibgrafo.vertice import Vertice
from meu_grafo_lista_adj_nao_dir import *


class TestGrafo(unittest.TestCase):
    def setUp(self):
        # Grafo da Paraíba
        self.g_p = GrafoJSON.json_to_grafo("test_json/grafo_pb.json", MeuGrafo())

        # Clone do Grafo da Paraíba para ver se o método equals está funcionando
        self.g_p2 = GrafoJSON.json_to_grafo("test_json/grafo_pb2.json", MeuGrafo())

        # Outro clone do Grafo da Paraíba para ver se o método equals está funcionando
        # Esse tem um pequena diferença na primeira aresta
        self.g_p3 = GrafoJSON.json_to_grafo("test_json/grafo_pb3.json", MeuGrafo())

        # Outro clone do Grafo da Paraíba para ver se o método equals está funcionando
        # Esse tem um pequena diferença na segunda aresta
        self.g_p4 = GrafoJSON.json_to_grafo("test_json/grafo_pb4.json", MeuGrafo())

        # Grafo da Paraíba sem arestas paralelas
        self.g_p_sem_paralelas = MeuGrafo()
        self.g_p_sem_paralelas.adiciona_vertice("J")
        self.g_p_sem_paralelas.adiciona_vertice("C")
        self.g_p_sem_paralelas.adiciona_vertice("E")
        self.g_p_sem_paralelas.adiciona_vertice("P")
        self.g_p_sem_paralelas.adiciona_vertice("M")
        self.g_p_sem_paralelas.adiciona_vertice("T")
        self.g_p_sem_paralelas.adiciona_vertice("Z")
        self.g_p_sem_paralelas.adiciona_aresta("a1", "J", "C")
        self.g_p_sem_paralelas.adiciona_aresta("a2", "C", "E")
        self.g_p_sem_paralelas.adiciona_aresta("a3", "P", "C")
        self.g_p_sem_paralelas.adiciona_aresta("a4", "T", "C")
        self.g_p_sem_paralelas.adiciona_aresta("a5", "M", "C")
        self.g_p_sem_paralelas.adiciona_aresta("a6", "M", "T")
        self.g_p_sem_paralelas.adiciona_aresta("a7", "T", "Z")

        # Grafos completos
        self.g_c = (
            GrafoBuilder()
            .tipo(MeuGrafo())
            .vertices(["J", "C", "E", "P"])
            .arestas(True)
            .build()
        )

        self.g_c2 = GrafoBuilder().tipo(MeuGrafo()).vertices(3).arestas(True).build()

        self.g_c3 = GrafoBuilder().tipo(MeuGrafo()).vertices(1).build()

        # Grafos com laco
        self.g_l1 = GrafoJSON.json_to_grafo("test_json/grafo_l1.json", MeuGrafo())

        self.g_l2 = GrafoJSON.json_to_grafo("test_json/grafo_l2.json", MeuGrafo())

        self.g_l3 = GrafoJSON.json_to_grafo("test_json/grafo_l3.json", MeuGrafo())

        self.g_l4 = (
            GrafoBuilder()
            .tipo(MeuGrafo())
            .vertices([v := Vertice("D")])
            .arestas([Aresta("a1", v, v)])
            .build()
        )

        self.g_l5 = (
            GrafoBuilder().tipo(MeuGrafo()).vertices(3).arestas(3, lacos=1).build()
        )

        # Grafos desconexos
        self.g_d = (
            GrafoBuilder()
            .tipo(MeuGrafo())
            .vertices(
                [a := Vertice("A"), b := Vertice("B"), Vertice("C"), Vertice("D")]
            )
            .arestas([Aresta("asd", a, b)])
            .build()
        )

        self.g_d2 = GrafoBuilder().tipo(MeuGrafo()).vertices(4).build()

        # Grafo p\teste de remoção em casta
        self.g_r = GrafoBuilder().tipo(MeuGrafo()).vertices(2).arestas(1).build()

        self.g_tree = MeuGrafo()
        self.g_tree.adiciona_vertice('A')
        self.g_tree.adiciona_vertice('B')
        self.g_tree.adiciona_vertice('C')
        self.g_tree.adiciona_vertice('D')
        self.g_tree.adiciona_aresta('1', 'A', 'B')
        self.g_tree.adiciona_aresta('2', 'A', 'C')
        self.g_tree.adiciona_aresta('3', 'B', 'D')

        # Grafo mínimo: 1 vértice, sem arestas (K1)
        self.g_single = GrafoBuilder().tipo(MeuGrafo()).vertices(1).build()

        # Grafo com apenas 2 vértices e 1 aresta
        self.g_dois = GrafoBuilder().tipo(MeuGrafo()).vertices(2).arestas(1).build()

        # Grafo com apenas laços — nenhuma aresta entre vértices distintos
        v_a = Vertice("A")
        v_b = Vertice("B")
        self.g_so_lacos = MeuGrafo()
        self.g_so_lacos.adiciona_vertice(v_a)
        self.g_so_lacos.adiciona_vertice(v_b)
        self.g_so_lacos.adiciona_aresta(Aresta("l1", v_a, v_a))
        self.g_so_lacos.adiciona_aresta(Aresta("l2", v_b, v_b))

        # Grafo com par invertido: a1(X-Y) e a2(Y-X) → em não-dir, são paralelas
        v_x = Vertice("X")
        v_y = Vertice("Y")
        self.g_par_invertido = MeuGrafo()
        self.g_par_invertido.adiciona_vertice(v_x)
        self.g_par_invertido.adiciona_vertice(v_y)
        self.g_par_invertido.adiciona_aresta(Aresta("a1", v_x, v_y))
        self.g_par_invertido.adiciona_aresta(Aresta("a2", v_y, v_x))

        # Estrela: vértice "centro" conectado a 4 folhas, folhas não se tocam
        self.g_estrela = MeuGrafo()
        for r in ["centro", "A", "B", "C", "D"]:
            self.g_estrela.adiciona_vertice(r)
        for r in ["A", "B", "C", "D"]:
            self.g_estrela.adiciona_aresta(f"e_{r}", "centro", r)

        # Grafo com múltiplos laços no mesmo vértice Z
        v_z = Vertice("Z")
        self.g_multi_laco = MeuGrafo()
        self.g_multi_laco.adiciona_vertice(v_z)
        self.g_multi_laco.adiciona_aresta(Aresta("l1", v_z, v_z))
        self.g_multi_laco.adiciona_aresta(Aresta("l2", v_z, v_z))

        # Caminho simples: A-B-C-D (sem ramificações, sem ciclos)
        self.g_caminho = MeuGrafo()
        for r in ["A", "B", "C", "D"]:
            self.g_caminho.adiciona_vertice(r)
        self.g_caminho.adiciona_aresta("e1", "A", "B")
        self.g_caminho.adiciona_aresta("e2", "B", "C")
        self.g_caminho.adiciona_aresta("e3", "C", "D")

    def test_adiciona_aresta(self):
        self.assertTrue(self.g_p.adiciona_aresta("a10", "J", "C"))
        a = Aresta("zxc", self.g_p.get_vertice("C"), self.g_p.get_vertice("Z"))
        self.assertTrue(self.g_p.adiciona_aresta(a))
        with self.assertRaises(ArestaInvalidaError):
            self.assertTrue(self.g_p.adiciona_aresta(a))
        with self.assertRaises(VerticeInvalidoError):
            self.assertTrue(self.g_p.adiciona_aresta("b1", "", "C"))
        with self.assertRaises(VerticeInvalidoError):
            self.assertTrue(self.g_p.adiciona_aresta("b1", "A", "C"))
        with self.assertRaises(TypeError):
            self.g_p.adiciona_aresta("")
        with self.assertRaises(TypeError):
            self.g_p.adiciona_aresta("aa-bb")
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.adiciona_aresta("x", "J", "V")
        with self.assertRaises(ArestaInvalidaError):
            self.g_p.adiciona_aresta("a1", "J", "C")

    def test_remove_vertice(self):
        self.assertIsNone(self.g_r.remove_vertice("A"))
        self.assertFalse(self.g_r.existe_rotulo_vertice("A"))
        self.assertFalse(self.g_r.existe_rotulo_aresta("1"))
        with self.assertRaises(VerticeInvalidoError):
            self.g_r.get_vertice("A")
        self.assertFalse(self.g_r.get_aresta("1"))
        self.assertEqual(self.g_r.arestas_sobre_vertice("B"), set())

    def test_eq(self):
        self.assertEqual(self.g_p, self.g_p2)
        self.assertNotEqual(self.g_p, self.g_p3)
        self.assertNotEqual(self.g_p, self.g_p_sem_paralelas)
        self.assertNotEqual(self.g_p, self.g_p4)

    def test_vertices_nao_adjacentes(self):
        self.assertEqual(
            self.g_p.vertices_nao_adjacentes(),
            {
                "J-E",
                "J-P",
                "J-M",
                "J-T",
                "J-Z",
                "C-Z",
                "E-P",
                "E-M",
                "E-T",
                "E-Z",
                "P-M",
                "P-T",
                "P-Z",
                "M-Z",
            },
        )
        self.assertEqual(
            self.g_d.vertices_nao_adjacentes(), {"A-C", "A-D", "B-C", "B-D", "C-D"}
        )
        self.assertEqual(
            self.g_d2.vertices_nao_adjacentes(),
            {"A-B", "A-C", "A-D", "B-C", "B-D", "C-D"},
        )
        self.assertEqual(self.g_c.vertices_nao_adjacentes(), set())
        self.assertEqual(self.g_c3.vertices_nao_adjacentes(), set())

    def test_ha_laco(self):
        self.assertFalse(self.g_p.ha_laco())
        self.assertFalse(self.g_p2.ha_laco())
        self.assertFalse(self.g_p3.ha_laco())
        self.assertFalse(self.g_p4.ha_laco())
        self.assertFalse(self.g_p_sem_paralelas.ha_laco())
        self.assertFalse(self.g_d.ha_laco())
        self.assertFalse(self.g_c.ha_laco())
        self.assertFalse(self.g_c2.ha_laco())
        self.assertFalse(self.g_c3.ha_laco())
        self.assertTrue(self.g_l1.ha_laco())
        self.assertTrue(self.g_l2.ha_laco())
        self.assertTrue(self.g_l3.ha_laco())
        self.assertTrue(self.g_l4.ha_laco())
        self.assertTrue(self.g_l5.ha_laco())

    def test_grau(self):
        # Paraíba
        self.assertEqual(self.g_p.grau("J"), 1)
        self.assertEqual(self.g_p.grau("C"), 7)
        self.assertEqual(self.g_p.grau("E"), 2)
        self.assertEqual(self.g_p.grau("P"), 2)
        self.assertEqual(self.g_p.grau("M"), 2)
        self.assertEqual(self.g_p.grau("T"), 3)
        self.assertEqual(self.g_p.grau("Z"), 1)
        with self.assertRaises(VerticeInvalidoError):
            self.assertEqual(self.g_p.grau("G"), 5)

        self.assertEqual(self.g_d.grau("A"), 1)
        self.assertEqual(self.g_d.grau("C"), 0)
        self.assertNotEqual(self.g_d.grau("D"), 2)
        self.assertEqual(self.g_d2.grau("A"), 0)

        # Completos
        self.assertEqual(self.g_c.grau("J"), 3)
        self.assertEqual(self.g_c.grau("C"), 3)
        self.assertEqual(self.g_c.grau("E"), 3)
        self.assertEqual(self.g_c.grau("P"), 3)

        # Com laço. Lembrando que cada laço conta 2 vezes por vértice para cálculo do grau
        self.assertEqual(self.g_l1.grau("A"), 5)
        self.assertEqual(self.g_l2.grau("B"), 4)
        self.assertEqual(self.g_l4.grau("D"), 2)

    def test_ha_paralelas(self):
        self.assertTrue(self.g_p.ha_paralelas())
        self.assertFalse(self.g_p_sem_paralelas.ha_paralelas())
        self.assertFalse(self.g_c.ha_paralelas())
        self.assertFalse(self.g_c2.ha_paralelas())
        self.assertFalse(self.g_c3.ha_paralelas())
        self.assertTrue(self.g_l1.ha_paralelas())

    def test_arestas_sobre_vertice(self):
        self.assertEqual(self.g_p.arestas_sobre_vertice("J"), {"a1"})
        self.assertEqual(
            self.g_p.arestas_sobre_vertice("C"),
            {"a1", "a2", "a3", "a4", "a5", "a6", "a7"},
        )
        self.assertEqual(self.g_p.arestas_sobre_vertice("M"), {"a7", "a8"})
        self.assertEqual(self.g_l2.arestas_sobre_vertice("B"), {"a1", "a2", "a3"})
        self.assertEqual(self.g_d.arestas_sobre_vertice("C"), set())
        self.assertEqual(self.g_d.arestas_sobre_vertice("A"), {"asd"})
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.arestas_sobre_vertice("A")

    def test_eh_completo(self):
        self.assertFalse(self.g_p.eh_completo())
        self.assertFalse((self.g_p_sem_paralelas.eh_completo()))
        self.assertTrue((self.g_c.eh_completo()))
        self.assertTrue((self.g_c2.eh_completo()))
        self.assertTrue((self.g_c3.eh_completo()))
        self.assertFalse((self.g_l1.eh_completo()))
        self.assertFalse((self.g_l2.eh_completo()))
        self.assertFalse((self.g_l3.eh_completo()))
        self.assertFalse((self.g_l4.eh_completo()))
        self.assertFalse((self.g_l5.eh_completo()))
        self.assertFalse((self.g_d.eh_completo()))
        self.assertFalse((self.g_d2.eh_completo()))

    def test_eh_conexo(self):
        self.assertTrue(self.g_p.eh_conexo())
        self.assertTrue(self.g_p_sem_paralelas.eh_conexo())
        self.assertTrue(self.g_tree.eh_conexo())
        self.assertTrue(self.g_c.eh_conexo())

        # Desconexos
        self.assertFalse(self.g_d.eh_conexo())
        self.assertFalse(self.g_d2.eh_conexo())

        self.assertTrue(self.g_single.eh_conexo())  # K1 é trivialmente conexo
        self.assertTrue(self.g_estrela.eh_conexo())  # estrela: tudo passa pelo centro → conexo
        self.assertTrue(self.g_caminho.eh_conexo())  # caminho linear é conexo
        self.assertFalse(self.g_so_lacos.eh_conexo())  # 2 vértices com só laços (sem aresta entre eles) → desconexo

        self.g_caminho.adiciona_vertice("isolado")
        self.assertFalse(self.g_caminho.eh_conexo())  # vértice sem aresta torna qualquer grafo desconexo

    def test_ha_ciclo(self):
        # Grafos com arestas paralelas ou laços possuem ciclo
        self.assertTrue(self.g_p.ha_ciclo())
        self.assertTrue(self.g_l1.ha_ciclo())

        # O grafo g_p_sem_paralelas possui o ciclo C-M-T
        self.assertTrue(self.g_p_sem_paralelas.ha_ciclo())

        # Grafo completo possui ciclo
        self.assertTrue(self.g_c.ha_ciclo())

        # Árvores e o grafo desconexo A-B simples não possuem ciclo
        self.assertFalse(self.g_tree.ha_ciclo())
        self.assertFalse(self.g_d.ha_ciclo())

        self.assertTrue(self.g_so_lacos.ha_ciclo())  # laço já é um ciclo
        self.assertTrue(self.g_multi_laco.ha_ciclo())  # múltiplos laços → ciclo
        self.assertFalse(self.g_caminho.ha_ciclo())  # caminho linear A-B-C-D não tem ciclo
        self.assertFalse(self.g_estrela.ha_ciclo())  # estrela (árvore) não tem ciclo

        self.g_caminho.adiciona_aresta("e_fecha", "D", "A")
        self.assertTrue(self.g_caminho.ha_ciclo())  # fechar o caminho cria um ciclo

    def test_eh_arvore(self):
        # A árvore g_tree retorna a quantidade de folhas, que neste caso é 2 (os nós C e D)
        self.assertEqual(self.g_tree.eh_arvore(), 2)

        # Falham por não ser conexo ou por ter ciclo
        self.assertFalse(self.g_p.eh_arvore())
        self.assertFalse(self.g_p_sem_paralelas.eh_arvore())
        self.assertFalse(self.g_d.eh_arvore())
        self.assertFalse(self.g_c.eh_arvore())

        self.assertEqual(self.g_caminho.eh_arvore(), 2)  # A-B-C-D: árvore com 2 folhas (A e D)
        self.assertEqual(self.g_estrela.eh_arvore(), 4)  # estrela com 4 folhas → 4
        self.assertFalse(self.g_so_lacos.eh_arvore())  # desconexo → não é árvore

        # Caminho com ciclo fechado não é árvore
        g_ciclo = MeuGrafo()
        for r in ["A", "B", "C"]:
            g_ciclo.adiciona_vertice(r)
        g_ciclo.adiciona_aresta("e1", "A", "B")
        g_ciclo.adiciona_aresta("e2", "B", "C")
        g_ciclo.adiciona_aresta("e3", "C", "A")
        self.assertFalse(g_ciclo.eh_arvore())  # grafo com ciclo não é árvore

        g_desconexo = MeuGrafo()
        for r in ["A", "B", "C"]:
            g_desconexo.adiciona_vertice(r)
        g_desconexo.adiciona_aresta("e1", "A", "B")
        self.assertFalse(g_desconexo.eh_arvore())  # grafo desconexo nunca é árvore

    def test_eh_bipartido(self):
        # Árvores sempre são grafos bipartidos
        self.assertTrue(self.g_tree.eh_bipartido())

        # Grafos desconexos sem ciclo ímpar também são bipartidos (como o A-B)
        self.assertTrue(self.g_d.eh_bipartido())

        # O grafo g_p_sem_paralelas falha por ter o ciclo ímpar C-M-T (triângulo)
        self.assertFalse(self.g_p_sem_paralelas.eh_bipartido())

        # O grafo completo K4 falha por possuir ciclos ímpares (triângulos)
        self.assertFalse(self.g_c.eh_bipartido())

        self.assertTrue(self.g_single.eh_bipartido())  # K1: trivialmente bipartido
        self.assertTrue(self.g_caminho.eh_bipartido())  # caminho par A-B-C-D: {A,C} e {B,D}
        self.assertTrue(self.g_estrela.eh_bipartido())  # estrela: {centro} e {folhas}
        self.assertFalse(self.g_so_lacos.eh_bipartido())  # laço cria ciclo de comprimento 1 (ímpar) → não bipartido

        g_k3 = GrafoBuilder().tipo(MeuGrafo()).vertices(3).arestas(True).build()
        self.assertFalse(g_k3.eh_bipartido())  # K3 tem triângulo (ciclo ímpar) → não bipartido

        g_dois_caminhos = MeuGrafo()
        for r in ["A", "B", "C", "D"]:
            g_dois_caminhos.adiciona_vertice(r)
        g_dois_caminhos.adiciona_aresta("e1", "A", "B")
        g_dois_caminhos.adiciona_aresta("e2", "C", "D")
        self.assertTrue(g_dois_caminhos.eh_bipartido())  # duas arestas isoladas: componentes bipartidas → bipartido
