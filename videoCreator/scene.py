from manim import *
from aux import *
from maquinaEnigma_copy import *
from parametros import fraseIntroducida

class EnigmaMachineTransformation(Scene):
    def crearRotor(self, rotor: Rotor, position):
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
        nodos = VGroup()
        for i, letra in enumerate(abecedario):
            letra = Text(letra, font_size=14).shift(DOWN * 0.25*i)
            circunferencia = Circle(radius=0.15, color=WHITE).move_to(letra.get_center())
            nodos.add(VGroup(letra, circunferencia))
        
        nodos.move_to(LEFT * 4)
        
        uniones = VGroup()
        for i, par in enumerate(reflector.pares):
            a, b = par
            
            posicionA = nodos[abecedario.index(a)][1].get_center()
            posicionB = nodos[abecedario.index(b)][1].get_center()
            
            horizontalPosition = 0.1*LEFT*(2+i)
            lineaIzquierda = Line(posicionA + 0.1*LEFT, posicionA + horizontalPosition)
            lineaVertical = Line(posicionA + horizontalPosition, posicionB + horizontalPosition)
            lineaDerecha = Line(posicionB + horizontalPosition, posicionB + 0.1*LEFT)
            
            union = VGroup(lineaIzquierda, lineaVertical, lineaDerecha)
            
            uniones.add(union)
        
        texto = Text("Reflector", font_size=24).move_to(nodos[0][0].get_center() + UP * 0.5)
        
        reflectorGrafico = VGroup(nodos, uniones, texto)
        self.play(Write(reflectorGrafico))
        
        return reflectorGrafico
    
    def pasarLetra(self, letra: str):
        # Primero pasamos la letra de derecha a izquierda
        for i, rotores in enumerate(zip(self.maquina.rotores, self.rotoresGraficos)):
            # Aquí recuperamos los nombres de las variables del VGroup
            rotor = rotores[0]
            rotorGrafico = rotores[1]
            verticesDerecha = rotorGrafico[0]
            verticesIzquierda = rotorGrafico[1]
            aristas = rotorGrafico[2]
            
            indice = rotor.cadenaDerecha.index(letra)
            
            # Aquí cambiamos el color de los elementos, de derecha a izquierda
            self.play(Transform(verticesDerecha[indice][1], verticesDerecha[indice][1].copy().set_color(GREEN)))
            self.play(Transform(aristas[indice], aristas[indice].copy().set_color(GREEN)))
            self.play(Transform(verticesIzquierda[indice][1], verticesIzquierda[indice][1].copy().set_color(GREEN)))
            
            # Aquí cambiamos la letra
            letra = rotor.transformarDerechaIzquierda(letra)
            # Si no hemos llegado al último rotor, movemos entre rotores
            if i < len(self.maquina.rotores) - 1:
                letra = self.maquina.moverEntreRotores(letra, i, i+1)
        
        # Pasamos la letra por el reflector
        letraReflectada = self.maquina.reflector.transformar(letra)
        try:
            indice = self.maquina.reflector.pares.index((letra, letraReflectada))
        except ValueError: # Si no está en la lista, entonces está al revés
            indice = self.maquina.reflector.pares.index((letraReflectada, letra))
            
        union = self.reflectorGrafico[1][indice]
        
        # Color verde para el reflector
        self.play(Transform(union, union.copy().set_color(GREEN)))
        
        letra = letraReflectada
        
        # Pasamos la letra de izquierda a derecha
        for i, rotores in enumerate(zip(self.maquina.rotores[::-1], self.rotoresGraficos[::-1])):
            # Aquí recuperamos los nombres de las variables del VGroup
            rotor = rotores[0]
            rotorGrafico = rotores[1]
            verticesDerecha = rotorGrafico[0]
            verticesIzquierda = rotorGrafico[1]
            aristas = rotorGrafico[2]
            
            indice = rotor.cadenaIzquierda.index(letra)
            
            # Aquí cambiamos el color de los elementos, de derecha a izquierda
            self.play(Transform(verticesIzquierda[indice][1], verticesIzquierda[indice][1].copy().set_color(GREEN)))
            self.play(Transform(aristas[indice], aristas[indice].copy().set_color(GREEN)))
            self.play(Transform(verticesDerecha[indice][1], verticesDerecha[indice][1].copy().set_color(GREEN)))
            
            # Aquí cambiamos la letra
            letra = rotor.transformarIzquierdaDerecha(letra)
            # Si no hemos llegado al último rotor, movemos entre rotores
            if i < len(self.maquina.rotores) - 1:
                letra = self.maquina.moverEntreRotores(letra, len(self.maquina.rotores)-i-1, len(self.maquina.rotores)-i-2)
        
        self.wait(2)
        self.rotarMaquina()

    def rotarMaquina(self):
        self.maquina.rotar()
        
        # Volvemos a poner los rotores y la union en blanco
        for rotorGrafico in self.rotoresGraficos:
            verticesDerecha = rotorGrafico[0]
            verticesIzquierda = rotorGrafico[1]
            aristas = rotorGrafico[2]
            
            verticesDerecha.set_color(WHITE)
            verticesIzquierda.set_color(WHITE)
            aristas.set_color(WHITE)
            
        self.reflectorGrafico[1].set_color(WHITE)
        
        
        self.wait(0.5)
        
        nuevosRotoresGraficos = VGroup()
        for i, rotorGrafico in enumerate(self.rotoresGraficos):
            nuevoRotorGrafico = self.crearRotor(self.maquina.rotores[i], i)
            nuevosRotoresGraficos.add(nuevoRotorGrafico)
            # Si la primera letra ha cambiado, entonces lo cambiamos
            if nuevoRotorGrafico[0][0][0].text != rotorGrafico[0][0][0].text:
                self.play(FadeOut(rotorGrafico))
                self.play(Write(nuevoRotorGrafico))
                self.rotoresGraficos[i] = nuevoRotorGrafico
    
    def construct(self):
        self.maquina = maquinaRandom()
        
        self.rotoresGraficos = VGroup(*[self.crearRotor(rotor, i) for i, rotor in enumerate(self.maquina.rotores)])
        for rotorGrafico in self.rotoresGraficos:
            self.play(Write(rotorGrafico))
        
        self.unionesRotoresGraficos = [self.unirRotores(self.rotoresGraficos[i], self.rotoresGraficos[i+1]) for i in range(len(self.rotoresGraficos)-1)]
        
        self.reflectorGrafico = self.dibujarReflector(self.maquina.reflector)
        
        self.wait(2)
        
        for letra in fraseIntroducida:
            self.pasarLetra(letra)