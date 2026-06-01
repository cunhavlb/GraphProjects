import unittest

from bibgrafo.aresta import ArestaDirecionada
from bibgrafo.grafo_builder import GrafoBuilder
from bibgrafo.grafo_errors import *
from bibgrafo.grafo_json import GrafoJSON
from bibgrafo.vertice import Vertice
from meu_grafo_lista_adj_dir import *


class TestGrafo(unittest.TestCase):
    def setUp(self):
        # Grafo da Paraíba
        self.g_p = GrafoJSON.json_to_grafo("test_json/grafo_pb.json", MeuGrafo())

        # Clone do Grafo da Paraíba para ver se o metodo equals está funcionando
        self.g_p2 = GrafoJSON.json_to_grafo("test_json/grafo_pb2.json", MeuGrafo())

        # Outro clone do Grafo da Paraíba para ver se o metodo equals está funcionando
        # Esse tem um pequena diferença na primeira aresta
        self.g_p3 = GrafoJSON.json_to_grafo("test_json/grafo_pb3.json", MeuGrafo())

        # Outro clone do Grafo da Paraíba para ver se o metodo equals está funcionando
        # Esse tem um pequena diferença na segunda aresta
        self.g_p4 = GrafoJSON.json_to_grafo("test_json/grafo_pb5.json", MeuGrafo())

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

        # Grafo de 1 vértice sem arestas
        self.g_single = GrafoBuilder().tipo(MeuGrafo()).vertices(1).build()

        # Grafo com apenas um laço: A→A
        v_a = Vertice("A")
        self.g_laco_simples = MeuGrafo()
        self.g_laco_simples.adiciona_vertice(v_a)
        self.g_laco_simples.adiciona_aresta(ArestaDirecionada("l1", v_a, v_a))

        # Grafo bidirecional: A→B e B→A (não são paralelas em dígrafo)
        v_a2 = Vertice("A")
        v_b2 = Vertice("B")
        self.g_bidirecional = MeuGrafo()
        self.g_bidirecional.adiciona_vertice(v_a2)
        self.g_bidirecional.adiciona_vertice(v_b2)
        self.g_bidirecional.adiciona_aresta(ArestaDirecionada("a1", v_a2, v_b2))
        self.g_bidirecional.adiciona_aresta(ArestaDirecionada("a2", v_b2, v_a2))

        # DAG: A→B→C→D (sem ciclos, sem paralelas)
        self.g_dag = MeuGrafo()
        for r in ["A", "B", "C", "D"]:
            self.g_dag.adiciona_vertice(r)
        self.g_dag.adiciona_aresta("e1", "A", "B")
        self.g_dag.adiciona_aresta("e2", "B", "C")
        self.g_dag.adiciona_aresta("e3", "C", "D")

        # Grafo com ciclo: A→B→C→A
        self.g_ciclo = MeuGrafo()
        for r in ["A", "B", "C"]:
            self.g_ciclo.adiciona_vertice(r)
        self.g_ciclo.adiciona_aresta("e1", "A", "B")
        self.g_ciclo.adiciona_aresta("e2", "B", "C")
        self.g_ciclo.adiciona_aresta("e3", "C", "A")

        # Sumidouro: A, B, C, D apontam para "sink", que não tem saída
        self.g_sumidouro = MeuGrafo()
        for r in ["A", "B", "C", "D", "sink"]:
            self.g_sumidouro.adiciona_vertice(r)
        for r in ["A", "B", "C", "D"]:
            self.g_sumidouro.adiciona_aresta(f"e_{r}", r, "sink")

        # Grafo com dois caminhos de mesmo custo até D (empate no Dijkstra)
        self.g_empate = MeuGrafo()
        for r in ["A", "B", "C", "D"]:
            self.g_empate.adiciona_vertice(r)
        self.g_empate.adiciona_aresta("1", "A", "B", 2)
        self.g_empate.adiciona_aresta("2", "A", "C", 2)
        self.g_empate.adiciona_aresta("3", "B", "D", 1)
        self.g_empate.adiciona_aresta("4", "C", "D", 1)

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

        # Grafo de 1 vértice sem arestas
        self.g_single = GrafoBuilder().tipo(MeuGrafo()).vertices(1).build()

        # Grafo com apenas um laço: A→A
        v_a = Vertice("A")
        self.g_laco_simples = MeuGrafo()
        self.g_laco_simples.adiciona_vertice(v_a)
        self.g_laco_simples.adiciona_aresta(ArestaDirecionada("l1", v_a, v_a))

        # Grafo bidirecional: A→B e B→A (não são paralelas em dígrafo)
        v_a2 = Vertice("A")
        v_b2 = Vertice("B")
        self.g_bidirecional = MeuGrafo()
        self.g_bidirecional.adiciona_vertice(v_a2)
        self.g_bidirecional.adiciona_vertice(v_b2)
        self.g_bidirecional.adiciona_aresta(ArestaDirecionada("a1", v_a2, v_b2))
        self.g_bidirecional.adiciona_aresta(ArestaDirecionada("a2", v_b2, v_a2))

        # DAG: A→B→C→D (sem ciclos, sem paralelas)
        self.g_dag = MeuGrafo()
        for r in ["A", "B", "C", "D"]:
            self.g_dag.adiciona_vertice(r)
        self.g_dag.adiciona_aresta("e1", "A", "B")
        self.g_dag.adiciona_aresta("e2", "B", "C")
        self.g_dag.adiciona_aresta("e3", "C", "D")

        # Grafo com ciclo: A→B→C→A
        self.g_ciclo = MeuGrafo()
        for r in ["A", "B", "C"]:
            self.g_ciclo.adiciona_vertice(r)
        self.g_ciclo.adiciona_aresta("e1", "A", "B")
        self.g_ciclo.adiciona_aresta("e2", "B", "C")
        self.g_ciclo.adiciona_aresta("e3", "C", "A")

        # Sumidouro: A, B, C, D apontam para "sink", que não tem saída
        self.g_sumidouro = MeuGrafo()
        for r in ["A", "B", "C", "D", "sink"]:
            self.g_sumidouro.adiciona_vertice(r)
        for r in ["A", "B", "C", "D"]:
            self.g_sumidouro.adiciona_aresta(f"e_{r}", r, "sink")

        # Grafo com dois caminhos de mesmo custo até D (empate no Dijkstra)
        self.g_empate = MeuGrafo()
        for r in ["A", "B", "C", "D"]:
            self.g_empate.adiciona_vertice(r)
        self.g_empate.adiciona_aresta("1", "A", "B", 2)
        self.g_empate.adiciona_aresta("2", "A", "C", 2)
        self.g_empate.adiciona_aresta("3", "B", "D", 1)
        self.g_empate.adiciona_aresta("4", "C", "D", 1)

    def test_grau_entrada(self):
        with self.assertRaises(VerticeInvalidoError):
            self.g_dag.grau_entrada("Z")  # vértice inexistente → erro

        v = self.g_single.vertices[0].rotulo
        self.assertEqual(self.g_single.grau_entrada(v), 0)  # vértice isolado → entrada 0

        self.assertEqual(self.g_laco_simples.grau_entrada("A"),
                         1)  # laço A→A contribui +1 para entrada (não +2 como no não-dir)
        self.assertEqual(self.g_sumidouro.grau_entrada("sink"), 4)  # sumidouro recebe 4 arestas → entrada 4
        self.assertEqual(self.g_sumidouro.grau_entrada("A"), 0)  # fonte do sumidouro → entrada 0
        self.assertEqual(self.g_dag.grau_entrada("A"), 0)  # fonte do DAG → entrada 0
        self.assertEqual(self.g_bidirecional.grau_entrada("A"), 1)  # A→B e B→A: A recebe 1 aresta
        self.assertEqual(self.g_bidirecional.grau_entrada("B"), 1)  # idem para B

    def test_grau_saida(self):
        with self.assertRaises(VerticeInvalidoError):
            self.g_dag.grau_saida("Z")  # vértice inexistente → erro

        v = self.g_single.vertices[0].rotulo
        self.assertEqual(self.g_single.grau_saida(v), 0)  # vértice isolado → saída 0

        self.assertEqual(self.g_laco_simples.grau_saida("A"),
                         1)  # laço A→A contribui +1 para saída (diferente do não-dir)
        self.assertEqual(self.g_sumidouro.grau_saida("sink"), 0)  # sumidouro não tem saída → 0
        self.assertEqual(self.g_sumidouro.grau_saida("A"), 1)  # fonte aponta para sink → saída 1
        self.assertEqual(self.g_dag.grau_saida("A"), 1)  # A→B: saída 1
        self.assertEqual(self.g_dag.grau_saida("D"), 0)  # D é sumidouro no DAG → saída 0
        self.assertEqual(self.g_bidirecional.grau_saida("A"), 1)  # A envia 1 aresta
        self.assertEqual(self.g_bidirecional.grau_saida("B"), 1)  # idem B

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
        self.assertTrue(self.g_p.ha_paralelas())  # X
        self.assertFalse(self.g_p_sem_paralelas.ha_paralelas())  # X
        self.assertFalse(self.g_c.ha_paralelas())
        self.assertFalse(self.g_c2.ha_paralelas())
        self.assertFalse(self.g_c3.ha_paralelas())
        self.assertTrue(self.g_l1.ha_paralelas())  # X
        self.assertTrue(self.g_p3.ha_paralelas())
        self.assertFalse(self.g_p4.ha_paralelas())

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

    def test_dijkstra(self):
        # Todos os caminhos na base fornecida (g_p) possuem peso 1.

        # Testando caminho entre M e Z (passa por T) = Distância 2
        dist, caminho = self.g_p.dijkstra("M", "Z")
        self.assertEqual(dist, 2)
        self.assertEqual(caminho, ["M", "T", "Z"])

        # Testando caminho entre J e E (passa por C) = Distância 2
        dist, caminho = self.g_p.dijkstra("J", "E")
        self.assertEqual(dist, 2)
        self.assertEqual(caminho, ["J", "C", "E"])

        # Testando caminho inalcançável (de Z, que não tem aresta de saída, para J)
        dist, caminho = self.g_p.dijkstra("Z", "J")
        self.assertEqual(dist, float("inf"))

        # Criando um grafo pequeno com pesos diferentes
        g_pesos = MeuGrafo()
        g_pesos.adiciona_vertice("A")
        g_pesos.adiciona_vertice("B")
        g_pesos.adiciona_vertice("C")
        g_pesos.adiciona_vertice("D")
        g_pesos.adiciona_aresta("1", "A", "B", 2)
        g_pesos.adiciona_aresta("2", "A", "C", 5)  # Direto custa 5
        g_pesos.adiciona_aresta("3", "B", "C", 1)
        g_pesos.adiciona_aresta("4", "B", "D", 2)
        g_pesos.adiciona_aresta("5", "C", "D", 3)

        # Caminho mais rápido para C é por B (custa 3), e não direto por A (custa 5)
        dist_c, caminho_c = g_pesos.dijkstra("A", "C")
        self.assertEqual(dist_c, 3)
        self.assertEqual(caminho_c, ["A", "B", "C"])

        # Caminho mais rápido para D é por B (custa 4)
        dist_d, caminho_d = g_pesos.dijkstra("A", "D")
        self.assertEqual(dist_d, 4)
        self.assertEqual(caminho_d, ["A", "B", "D"])

        with self.assertRaises(VerticeInvalidoError):
            self.g_dag.dijkstra("Z", "A")  # origem inexistente → erro
        with self.assertRaises(VerticeInvalidoError):
            self.g_dag.dijkstra("A", "Z")  # destino inexistente → erro

        dist, caminho = self.g_dag.dijkstra("A", "A")
        self.assertEqual(dist, 0)
        self.assertEqual(caminho, ["A"])  # origem == destino → distância 0, caminho [A]

        dist, caminho = self.g_dag.dijkstra("A", "D")
        self.assertEqual(dist, 3)
        self.assertEqual(caminho, ["A", "B", "C", "D"])  # DAG com peso 1: caminho completo A→B→C→D custa 3

        dist, caminho = self.g_sumidouro.dijkstra("sink", "A")
        self.assertEqual(dist, float("inf"))
        self.assertEqual(caminho, [])  # sink não tem saída → inalcançável

        dist, caminho = self.g_ciclo.dijkstra("A", "C")
        self.assertEqual(dist, 2)
        self.assertEqual(caminho, ["A", "B", "C"])  # ciclo não trava o Dijkstra: A→B→C custa 2

        # Caminho direto mais caro perde para caminho indireto mais barato
        g_atalho = MeuGrafo()
        for r in ["A", "B", "C"]:
            g_atalho.adiciona_vertice(r)
        g_atalho.adiciona_aresta("direto", "A", "C", 10)
        g_atalho.adiciona_aresta("p1", "A", "B", 1)
        g_atalho.adiciona_aresta("p2", "B", "C", 2)
        dist, caminho = g_atalho.dijkstra("A", "C")
        self.assertEqual(dist, 3)
        self.assertEqual(caminho, ["A", "B", "C"])  # A→B→C (custo 3) vence A→C direto (custo 10)

        dist, caminho = self.g_empate.dijkstra("A", "D")
        self.assertEqual(dist, 3)  # dois caminhos de custo 3: verifica apenas a distância
        self.assertIn(caminho, [["A", "B", "D"], ["A", "C", "D"]])  # qualquer um dos dois caminhos válidos é aceito