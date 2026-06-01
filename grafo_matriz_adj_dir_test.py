import unittest

from bibgrafo.aresta import ArestaDirecionada
from bibgrafo.grafo_builder import GrafoBuilder
from bibgrafo.grafo_errors import ArestaInvalidaError, VerticeInvalidoError
from bibgrafo.grafo_json import GrafoJSON
from meu_grafo_matriz_adj_dir import *


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
        self.g_p_sem_paralelas = GrafoJSON.json_to_grafo(
            "test_json/grafo_pb_simples.json", MeuGrafo()
        )

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
            .vertices([(v := Vertice("D"))])
            .arestas([ArestaDirecionada("a1", v, v)])
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
            .arestas([ArestaDirecionada("asd", a, b)])
            .build()
        )

        self.g_d2 = GrafoBuilder().tipo(MeuGrafo()).vertices(4).build()

        # Grafo com ciclos e laços
        self.g_e = MeuGrafo()
        self.g_e.adiciona_vertice("A")
        self.g_e.adiciona_vertice("B")
        self.g_e.adiciona_vertice("C")
        self.g_e.adiciona_vertice("D")
        self.g_e.adiciona_vertice("E")
        self.g_e.adiciona_aresta("1", "A", "B")
        self.g_e.adiciona_aresta("2", "A", "C")
        self.g_e.adiciona_aresta("3", "C", "A")
        self.g_e.adiciona_aresta("4", "C", "B")
        self.g_e.adiciona_aresta("10", "C", "B")
        self.g_e.adiciona_aresta("5", "C", "D")
        self.g_e.adiciona_aresta("6", "D", "D")
        self.g_e.adiciona_aresta("7", "D", "B")
        self.g_e.adiciona_aresta("8", "D", "E")
        self.g_e.adiciona_aresta("9", "E", "A")
        self.g_e.adiciona_aresta("11", "E", "B")

        # Grafo de 1 vértice sem arestas (K1)
        self.g_single = GrafoBuilder().tipo(MeuGrafo()).vertices(1).build()

        # Grafo com apenas 2 vértices e 1 aresta: A→B
        self.g_dois = MeuGrafo()
        self.g_dois.adiciona_vertice("A")
        self.g_dois.adiciona_vertice("B")
        self.g_dois.adiciona_aresta("a1", "A", "B")

        # Grafo desconexo: A→B e C, D soltos (mesma estrutura do g_d dos outros testes)
        self.g_desconexo = MeuGrafo()
        for r in ["A", "B", "C", "D"]:
            self.g_desconexo.adiciona_vertice(r)
        self.g_desconexo.adiciona_aresta("asd", "A", "B")

        # Ciclo completo: A→B→C→A (todos alcançam todos, inclusive a si mesmos)
        self.g_ciclo = MeuGrafo()
        for r in ["A", "B", "C"]:
            self.g_ciclo.adiciona_vertice(r)
        self.g_ciclo.adiciona_aresta("e1", "A", "B")
        self.g_ciclo.adiciona_aresta("e2", "B", "C")
        self.g_ciclo.adiciona_aresta("e3", "C", "A")

        # DAG: A→B→C→D (sem ciclos, alcançabilidade só "para frente")
        self.g_dag = MeuGrafo()
        for r in ["A", "B", "C", "D"]:
            self.g_dag.adiciona_vertice(r)
        self.g_dag.adiciona_aresta("e1", "A", "B")
        self.g_dag.adiciona_aresta("e2", "B", "C")
        self.g_dag.adiciona_aresta("e3", "C", "D")

        # Grafo com laço: A→A, mais A→B
        self.g_laco = MeuGrafo()
        self.g_laco.adiciona_vertice("A")
        self.g_laco.adiciona_vertice("B")
        self.g_laco.adiciona_aresta("l1", "A", "A")
        self.g_laco.adiciona_aresta("e1", "A", "B")

        # Grafo bidirecional: A→B e B→A (não é ciclo de 3, mas cria alcançabilidade mútua)
        self.g_bidirecional = MeuGrafo()
        self.g_bidirecional.adiciona_vertice("A")
        self.g_bidirecional.adiciona_vertice("B")
        self.g_bidirecional.adiciona_aresta("a1", "A", "B")
        self.g_bidirecional.adiciona_aresta("a2", "B", "A")

        # Sumidouro: A, B, C apontam para sink — sink não alcança ninguém
        self.g_sumidouro = MeuGrafo()
        for r in ["A", "B", "C", "sink"]:
            self.g_sumidouro.adiciona_vertice(r)
        self.g_sumidouro.adiciona_aresta("e1", "A", "sink")
        self.g_sumidouro.adiciona_aresta("e2", "B", "sink")
        self.g_sumidouro.adiciona_aresta("e3", "C", "sink")

    def test_adiciona_aresta(self):
        self.assertTrue(self.g_p.adiciona_aresta("a10", "J", "C"))
        a = ArestaDirecionada(
            "zxc", self.g_p.get_vertice("C"), self.g_p.get_vertice("Z")
        )
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
        self.assertTrue(self.g_p.remove_vertice("J"))
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.remove_vertice("J")
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.remove_vertice("K")
        self.assertTrue(self.g_p.remove_vertice("C"))
        self.assertTrue(self.g_p.remove_vertice("Z"))

    def test_remove_aresta(self):
        self.assertTrue(self.g_p.remove_aresta("a1"))
        self.assertFalse(self.g_p.remove_aresta("a1"))
        self.assertTrue(self.g_p.remove_aresta("a7"))
        self.assertFalse(self.g_c.remove_aresta("a"))
        self.assertTrue(self.g_c.remove_aresta("a6"))
        self.assertTrue(self.g_c.remove_aresta("a1", "J"))
        self.assertTrue(self.g_c.remove_aresta("a5", "C"))
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.remove_aresta("a2", "X", "C")
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.remove_aresta("a3", "X")
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.remove_aresta("a3", v2="X")

    def test_eq(self):
        self.assertEqual(self.g_p, self.g_p2)
        self.assertNotEqual(self.g_p, self.g_p3)
        self.assertNotEqual(self.g_p, self.g_p_sem_paralelas)
        self.assertNotEqual(self.g_p, self.g_p4)

    def test_vertices_nao_adjacentes(self):
        self.assertEqual(
            set(self.g_p.vertices_nao_adjacentes()),
            {
                "J-E",
                "J-P",
                "J-M",
                "J-T",
                "J-Z",
                "C-J",
                "C-T",
                "C-Z",
                "C-M",
                "C-P",
                "E-C",
                "E-J",
                "E-P",
                "E-M",
                "E-T",
                "E-Z",
                "P-J",
                "P-E",
                "P-M",
                "P-T",
                "P-Z",
                "M-J",
                "M-E",
                "M-P",
                "M-Z",
                "T-J",
                "T-M",
                "T-E",
                "T-P",
                "Z-J",
                "Z-C",
                "Z-E",
                "Z-P",
                "Z-M",
                "Z-T",
            },
        )

        self.assertEqual(
            set(self.g_c.vertices_nao_adjacentes()),
            {"C-J", "E-C", "P-C", "E-J", "P-E", "P-J"},
        )
        self.assertEqual(self.g_c3.vertices_nao_adjacentes(), [])
        self.assertEqual(
            set(self.g_e.vertices_nao_adjacentes()),
            {
                "A-D",
                "A-E",
                "B-A",
                "B-C",
                "B-D",
                "B-E",
                "C-E",
                "D-C",
                "D-A",
                "E-D",
                "E-C",
            },
        )

    def test_ha_laco(self):
        self.assertFalse(self.g_p.ha_laco())
        self.assertFalse(self.g_p_sem_paralelas.ha_laco())
        self.assertFalse(self.g_c2.ha_laco())
        self.assertTrue(self.g_l1.ha_laco())
        self.assertTrue(self.g_l2.ha_laco())
        self.assertTrue(self.g_l3.ha_laco())
        self.assertTrue(self.g_l4.ha_laco())
        self.assertTrue(self.g_l5.ha_laco())
        self.assertTrue(self.g_e.ha_laco())

    def test_grau(self):
        # Paraíba
        self.assertEqual(self.g_p.grau_saida("J"), 1)
        self.assertEqual(self.g_p.grau_entrada("J"), 0)
        self.assertEqual(self.g_p.grau_saida("C"), 2)
        self.assertEqual(self.g_p.grau_entrada("C"), 5)
        self.assertEqual(self.g_p.grau_saida("E"), 0)
        self.assertEqual(self.g_p.grau_entrada("E"), 2)
        self.assertEqual(self.g_p.grau_saida("P"), 2)
        self.assertEqual(self.g_p.grau_entrada("P"), 0)
        self.assertEqual(self.g_p.grau_saida("M"), 2)
        self.assertEqual(self.g_p.grau_entrada("M"), 0)
        self.assertEqual(self.g_p.grau_saida("T"), 2)
        self.assertEqual(self.g_p.grau_entrada("T"), 1)
        self.assertEqual(self.g_p.grau_saida("Z"), 0)
        self.assertEqual(self.g_p.grau_entrada("Z"), 1)
        with self.assertRaises(VerticeInvalidoError):
            self.assertEqual(self.g_p.grau_saida("G"), 5)

        self.assertEqual(self.g_d.grau_entrada("A"), 0)
        self.assertEqual(self.g_d.grau_saida("A"), 1)
        self.assertEqual(self.g_d.grau_entrada("C"), 0)
        self.assertEqual(self.g_d.grau_saida("C"), 0)
        self.assertNotEqual(self.g_d.grau_entrada("D"), 2)
        self.assertNotEqual(self.g_d.grau_entrada("D"), 2)
        self.assertEqual(self.g_d2.grau_entrada("A"), 0)
        self.assertNotEqual(self.g_d.grau_saida("D"), 2)

        # Completos
        self.assertEqual(self.g_c.grau_entrada("J"), 0)
        self.assertEqual(self.g_c.grau_saida("J"), 3)
        self.assertEqual(self.g_c.grau_entrada("C"), 1)
        self.assertEqual(self.g_c.grau_saida("C"), 2)
        self.assertEqual(self.g_c.grau_saida("E"), 1)
        self.assertEqual(self.g_c.grau_entrada("E"), 2)
        self.assertEqual(self.g_c.grau_saida("P"), 0)
        self.assertEqual(self.g_c.grau_entrada("P"), 3)

        # Com laço.
        self.assertEqual(self.g_l1.grau_saida("A"), 2)
        self.assertEqual(self.g_l1.grau_entrada("A"), 3)
        self.assertEqual(self.g_l2.grau_entrada("B"), 2)
        self.assertEqual(self.g_l2.grau_saida("B"), 2)
        self.assertEqual(self.g_l4.grau_entrada("D"), 1)
        self.assertEqual(self.g_l4.grau_saida("D"), 1)

    def test_ha_paralelas(self):
        self.assertTrue(self.g_p.ha_paralelas())
        self.assertFalse(self.g_p_sem_paralelas.ha_paralelas())
        self.assertFalse(self.g_c.ha_paralelas())
        self.assertFalse(self.g_c2.ha_paralelas())
        self.assertFalse(self.g_c3.ha_paralelas())
        self.assertTrue(self.g_l1.ha_paralelas())
        self.assertTrue(self.g_e.ha_paralelas())

    def test_arestas_sobre_vertice(self):
        self.assertEqual(set(self.g_p.arestas_sobre_vertice("J")), {"a1"})
        self.assertEqual(
            set(self.g_p.arestas_sobre_vertice("C")),
            {"a1", "a2", "a3", "a4", "a5", "a6", "a7"},
        )
        self.assertEqual(set(self.g_p.arestas_sobre_vertice("M")), {"a7", "a8"})
        self.assertEqual(set(self.g_l2.arestas_sobre_vertice("B")), {"a1", "a2", "a3"})
        self.assertEqual(set(self.g_d.arestas_sobre_vertice("C")), set())
        self.assertEqual(set(self.g_d.arestas_sobre_vertice("A")), {"asd"})
        with self.assertRaises(VerticeInvalidoError):
            self.g_p.arestas_sobre_vertice("A")
        self.assertEqual(set(self.g_e.arestas_sobre_vertice("D")), {"5", "6", "7", "8"})

    def test_warshall(self):
        # O grafo desconexo g_d possui ordem (A, B, C, D)
        # e apenas uma aresta de A -> B
        matriz_esperada_d = [
            [0, 1, 0, 0],  # A alcança B
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.assertEqual(self.g_d.warshall(), matriz_esperada_d)

        # Criando um grafo pequeno com um ciclo A->B->C->A
        g_ciclo = MeuGrafo()
        g_ciclo.adiciona_vertice("A")
        g_ciclo.adiciona_vertice("B")
        g_ciclo.adiciona_vertice("C")
        g_ciclo.adiciona_aresta("1", "A", "B")
        g_ciclo.adiciona_aresta("2", "B", "C")
        g_ciclo.adiciona_aresta("3", "C", "A")

        # Num ciclo todos se alcançam (inclusive a si mesmos)
        matriz_esperada_ciclo = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        self.assertEqual(g_ciclo.warshall(), matriz_esperada_ciclo)

        # K1: matriz 1x1, vértice não alcança a si mesmo (sem laço)
        self.assertEqual(self.g_single.warshall(), [[0]])

        # A→B: A alcança B, mas B não alcança A, ninguém alcança a si mesmo
        self.assertEqual(self.g_dois.warshall(), [
            [0, 1],  # A alcança B
            [0, 0],  # B não alcança ninguém
        ])

        # Grafo desconexo: A alcança apenas B, C e D são ilhas (ordem: A, B, C, D)
        self.assertEqual(self.g_desconexo.warshall(), [
            [0, 1, 0, 0],  # A alcança B
            [0, 0, 0, 0],  # B não alcança ninguém
            [0, 0, 0, 0],  # C isolado
            [0, 0, 0, 0],  # D isolado
        ])

        # Ciclo A→B→C→A: todos alcançam todos (inclusive a si mesmos por transitividade)
        self.assertEqual(self.g_ciclo.warshall(), [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ])

        # DAG A→B→C→D: alcançabilidade apenas para frente, nunca para trás
        resultado_dag = self.g_dag.warshall()
        self.assertEqual(resultado_dag[0], [0, 1, 1, 1])  # A alcança B, C e D (transitivamente)
        self.assertEqual(resultado_dag[1], [0, 0, 1, 1])  # B alcança C e D
        self.assertEqual(resultado_dag[2], [0, 0, 0, 1])  # C alcança apenas D
        self.assertEqual(resultado_dag[3], [0, 0, 0, 0])  # D (sumidouro) não alcança ninguém

        # Laço A→A e A→B: laço não cria alcançabilidade transitiva nova, A ainda alcança B
        resultado_laco = self.g_laco.warshall()
        self.assertEqual(resultado_laco[0][1], 1)  # A alcança B (por A→B)
        self.assertEqual(resultado_laco[1][0], 0)  # B não alcança A
        self.assertEqual(resultado_laco[1][1], 0)  # B não alcança a si mesmo (sem laço em B)

        # Bidirecional A→B e B→A: ambos se alcançam e a si mesmos (ciclo de comprimento 2)
        self.assertEqual(self.g_bidirecional.warshall(), [
            [1, 1],  # A alcança A (pelo ciclo) e B
            [1, 1],  # B alcança B (pelo ciclo) e A
        ])

        # Sumidouro: sink não alcança ninguém, fontes alcançam apenas sink (ordem: A, B, C, sink)
        resultado_sink = self.g_sumidouro.warshall()
        idx_sink = 3
        for i in range(3):
            self.assertEqual(resultado_sink[i][idx_sink], 1)  # A, B, C alcançam sink
            self.assertEqual(resultado_sink[idx_sink][i], 0)  # sink não alcança A, B nem C
        self.assertEqual(resultado_sink[idx_sink][idx_sink], 0)  # sink não alcança a si mesmo
