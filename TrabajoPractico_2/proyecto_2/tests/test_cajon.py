from unittest import TestCase
import unittest
from modules.Frutas import Manzana, Kiwi
from modules.Verduras import Zanahoria, Papa
from modules.Cajon import Cajon

class TestCajon(TestCase):
    def test_agregar_alimento(self):
        cajon = Cajon(capacidad_maxima=3)
        manzana = Manzana(peso=0.15)
        kiwi = Kiwi(peso=0.1)
        cajon.agregar_alimento(manzana)
        cajon.agregar_alimento(kiwi)
        self.assertEqual(cajon.cantidad_actual, 2)

    def test_agregar_alimento_excede_capacidad(self):
        cajon = Cajon(capacidad_maxima=1)
        manzana = Manzana(peso=0.15)
        kiwi = Kiwi(peso=0.1)
        cajon.agregar_alimento(manzana)
        with self.assertRaises(ValueError):
            cajon.agregar_alimento(kiwi)

    # def test_es_susceptible(self):
    #     cajon = Cajon(capacidad_maxima=2)
    #     manzana = Manzana(peso=0.5)  
    #     papa = Papa(peso=0.3)         
    #     cajon.agregar_alimento(manzana)
    #     cajon.agregar_alimento(papa)
    #     self.assertTrue(cajon.es_susceptible())


    # def test_obtener_peso_total(self):
    #     cajon = Cajon(capacidad_maxima=3)
    #     manzana = Manzana(peso=0.15)
    #     kiwi = Kiwi(peso=0.1)
    #     cajon.agregar_alimento(manzana)
    #     cajon.agregar_alimento(kiwi)
    #     self.assertEqual(cajon.peso_total(), 0.25)

    # def test_aw_promedio_por_tipo(self):
    #     cajon = Cajon(capacidad_maxima=4)
    #     manzana = Manzana(peso=0.15)  # aw ~ 0.97
    #     kiwi = Kiwi(peso=0.1)        # aw ~ 0.98
    #     zanahoria = Zanahoria(peso=0.12)  # aw ~ 0.97
    #     papa = Papa(peso=0.2)            # aw ~ 1.0
    #     cajon.agregar_alimento(manzana)
    #     cajon.agregar_alimento(kiwi)
    #     cajon.agregar_alimento(zanahoria)
    #     cajon.agregar_alimento(papa)
    #     resultado = cajon.aw_promedio_por_tipo()
    #     # Calcula los promedios esperados
    #     aw_prom_frutas = (manzana.calcular_aw() + kiwi.calcular_aw()) / 2
    #     aw_prom_verduras = (zanahoria.calcular_aw() + papa.calcular_aw()) / 2
    #     self.assertAlmostEqual(resultado["aw_prom_frutas"], aw_prom_frutas)
    #     self.assertAlmostEqual(resultado["aw_prom_verduras"], aw_prom_verduras)

    # def test_obtener_advertencias(self):
    #     cajon = Cajon(capacidad_maxima=4)
        
    #     kiwi = Kiwi(peso=0.4)          
    #     zanahoria = Zanahoria(peso=0.5)  
    #     papa = Papa(peso=0.4)            
    #     cajon.agregar_alimento(kiwi)
    #     cajon.agregar_alimento(zanahoria)
    #     cajon.agregar_alimento(papa)
    #     advertencias = cajon.obtener_advertencias()
    #     # Debe haber advertencias para total, frutas, verduras y cada alimento
    #     self.assertTrue(any("Actividad acuosa total elevada" in adv for adv in advertencias))
    #     self.assertTrue(any("Promedio frutas elevado" in adv for adv in advertencias))
    #     self.assertTrue(any("Promedio verduras elevado" in adv for adv in advertencias))
    #     self.assertTrue(any("kiwi" in adv for adv in advertencias))
    #     self.assertTrue(any("zanahoria" in adv for adv in advertencias))
    #     self.assertTrue(any("papa" in adv for adv in advertencias))

    # def test_obtener_advertencias_sin_advertencias(self):
    #     class FrutaBajaAw(Manzana):
    #         def calcular_aw(self):
    #             return 0.5
    #     class VerduraBajaAw(Papa):
    #         def calcular_aw(self):
    #             return 0.5

    #     cajon = Cajon(capacidad_maxima=2)
    #     fruta = FrutaBajaAw(peso=0.1)
    #     verdura = VerduraBajaAw(peso=0.1)
    #     cajon.agregar_alimento(fruta)
    #     cajon.agregar_alimento(verdura)
    #     advertencias = cajon.obtener_advertencias()
    #     self.assertEqual(advertencias, [])
if __name__ == "__main__":
    unittest.main()
