from manim import *
from aux import *
from maquinaEnigma_copy import *

class EnigmaMachineTransformation(Scene):
    def dibujarRotor(self, rotor: Rotor, position):
        letrasDerecha = rotor.cadenaDerecha
        verticesDerecha = VGroup()
        for i, letra in enumerate(letrasDerecha):
            letra = Text(letra, font_size=14).shift(DOWN * 0.25*i + RIGHT * 0.5)
            circunferencia = Circle(radius=0.15, color=WHITE).move_to(letra.get_center())
            verticesDerecha.add(VGroup(letra, circunferencia))

        
        verticesIzquierda = VGroup()
        for i, letra in enumerate(rotor.cadenaIzquierda):
            letra = Text(letra, font_size=14).shift(DOWN * 0.25*i + LEFT * 0.5)
            circunferencia = Circle(radius=0.12, color=WHITE).move_to(letra.get_center())
            verticesIzquierda.add(VGroup(letra, circunferencia))
        
        aristas = VGroup()
        for derecha, izquierda in zip(verticesDerecha, verticesIzquierda):
            linea = Line(derecha[1].get_center()+0.1*LEFT, izquierda[1].get_center()+0.1*RIGHT, color=WHITE)
            aristas.add(linea)
        
        nombre = Text(f"Rotor {position+1}", font_size=24).move_to(verticesDerecha[0].get_center() + UP * 0.5 + LEFT * 0.5)
        
        rectangulo = Rectangle(width=1.8, height=6.7, color=BLUE).move_to(verticesDerecha.get_center() + LEFT * 0.5)
        
        rotorGrafico = VGroup(verticesDerecha, verticesIzquierda, aristas, nombre, rectangulo)
    
        rotorGrafico.move_to(RIGHT * (4-2.5*position))
        
        self.play(Write(rotorGrafico))
        
        return rotorGrafico
    
    def unirRotores(self, rotor1, rotor2):
        lineas = VGroup()
        for i in range(len(rotor1[0])):
            linea = Line(rotor1[1][i][1].get_center() + 0.25*LEFT, rotor2[0][i][1].get_center() + 0.25*RIGHT, color=BLUE)
            lineas.add(linea)
            
        self.play(Write(lineas))
        
        return linea
    
    
    def dibujarReflector(self, reflector: Reflector):
        abecedario = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        letras = VGroup()
        for i, letra in enumerate(abecedario):
            letra = Text(letra, font_size=14).shift(DOWN * 0.25*i)
            circunferencia = Circle(radius=0.15, color=WHITE).move_to(letra.get_center())
            letras.add(VGroup(letra, circunferencia))
        
        letras.move_to(LEFT * 4)
        
        uniones = VGroup()
        for i, par in enumerate(reflector.pares):
            a, b = par
            
            posicionA = letras[abecedario.index(a)][1].get_center()
            posicionB = letras[abecedario.index(b)][1].get_center()
            
            horizontalPosition = 0.1*LEFT*(2+i)
            lineaIzquierda = Line(posicionA + 0.1*LEFT, posicionA + horizontalPosition)
            lineaVertical = Line(posicionA + horizontalPosition, posicionB + horizontalPosition)
            lineaDerecha = Line(posicionB + horizontalPosition, posicionB + 0.1*LEFT)
            
            union = VGroup(lineaIzquierda, lineaVertical, lineaDerecha)
            
            uniones.add(union)
        
        texto = Text("Reflector", font_size=24).move_to(letras[0][0].get_center() + UP * 0.5)
        
        reflectorGrafico = VGroup(letras, uniones, texto)
        self.play(Write(reflectorGrafico))
        
        return reflectorGrafico
    
    def pasarLetra
    
    
    def construct(self):
        self.maquina = maquinaRandom()
        
        rotoresGraficos = [self.dibujarRotor(rotor, i) for i, rotor in enumerate(self.maquina.rotores)]
        
        unionesRotoresGraficos = [self.unirRotores(rotoresGraficos[i], rotoresGraficos[i+1]) for i in range(len(rotoresGraficos)-1)]
        
        reflectorGrafico = self.dibujarReflector(self.maquina.reflector)
        
        self.wait(20)
        