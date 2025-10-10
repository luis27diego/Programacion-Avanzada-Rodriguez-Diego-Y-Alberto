from unittest import TestCase
import unittest
from modules.Frutas import Manzana, Kiwi
from modules.Verduras import Zanahoria, Papa

class TestFrutas(TestCase):
    def test_manzana_calcular_aw(self):
        manzana = Manzana(peso=0.4)
        aw = manzana.calcular_aw()
        self.assertAlmostEqual(aw, 0.94, places=2)

    def test_kiwi_calcular_aw(self):
        kiwi = Kiwi(peso=0.1)
        aw = kiwi.calcular_aw()
        self.assertAlmostEqual(aw, 0.68, places=1)

    def test_obtener_nombre(self):
        manzana = Manzana(peso=0.5)
        self.assertEqual(manzana.nombre, "Manzana")
        kiwi = Kiwi(peso=0.1)
        self.assertEqual(kiwi.nombre, "Kiwi") 

    def test_peso_valido(self):
        with self.assertRaises(ValueError):
            Manzana(peso=-50)

class TestVerduras(TestCase):
    def test_zanahoria_calcular_aw(self):
        zanahoria = Zanahoria(peso=0.2)
        aw = zanahoria.calcular_aw()
        self.assertAlmostEqual(aw, 0.83, places=2)

    def test_papa_calcular_aw(self):
        papa = Papa(peso=0.3)
        aw = papa.calcular_aw()
        self.assertAlmostEqual(aw, 0.915, places=2)

    def test_obtener_nombre(self):
        zanahoria = Zanahoria(peso=0.2)
        self.assertEqual(zanahoria.nombre, "Zanahoria")
        papa = Papa(peso=0.3)
        self.assertEqual(papa.nombre, "Papa")

    def test_peso_valido(self):
        with self.assertRaises(ValueError):
            Papa(peso=0)

if __name__ == "__main__":
    unittest.main()