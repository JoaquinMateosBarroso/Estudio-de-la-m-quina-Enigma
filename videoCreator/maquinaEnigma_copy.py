import sys
def charToInt(char):
    return ord(char) - ord('A')

def intToChar(n: int):
    return chr(ord('A')+n)

class Rotor:
    def __init__(self, cadenaDerecha: list[str], cadenaIzquierda: list[str]):
        '''
            Inicializa un rotor que transforma las letras de cadenaDerecha en las de cadenaIzquierda
        
            :param cadenaDerecha: lista de letras que se transforman
            :param cadenaIzquierda: lista de letras a las que se transforman
        '''
        self.cadenaDerecha = cadenaDerecha
        self.cadenaIzquierda = cadenaIzquierda
        
    def transformarDerechaIzquierda(self, letra: str, verbose: bool = False) -> str:
        '''
            Transforma la letra dada por la letra correspondiente en la cadenaIzquierda
        
            :param letra: letra a transformar
            :return: letra transformada
        '''
        if verbose:
            print(f"{self.cadenaIzquierda[self.cadenaDerecha.index(letra)]}<-{letra}")
        
        return self.cadenaIzquierda[self.cadenaDerecha.index(letra)]
    
    def transformarIzquierdaDerecha(self, letra: str, verbose: bool = False) -> str:
        '''
            Transforma la letra dada por la letra correspondiente en la cadenaDerecha
        
            :param letra: letra a transformar
            :return: letra transformada
        '''
        if verbose:
            print(f"{letra}->{self.cadenaDerecha[self.cadenaIzquierda.index(letra)]}")
        
        return self.cadenaDerecha[self.cadenaIzquierda.index(letra)]
    
    def rotar(self):
        '''
            Rota el rotor
        '''
        self.cadenaDerecha = self.cadenaDerecha[1:] + [self.cadenaDerecha[0]]
        self.cadenaIzquierda = self.cadenaIzquierda[1:] + [self.cadenaIzquierda[0]]
    
    def clone(self):
        return Rotor(self.cadenaDerecha.copy(), self.cadenaIzquierda.copy())


class Reflector:
    def __init__(self, pares: list[tuple[str]]):
        '''
            Inicializa un reflector que transforma cada letra en su pareja asociada
        
            :param pares: lista de pares de letras que se transforman entre sí
        '''
        self.pares = pares
    
    def transformar(self, letra: str) -> str:
        '''
            Transforma la letra dada por la letra correspondiente en la cadena
        
            :param letra: letra a transformar
            :return: letra transformada
        '''
        par = tuple(filter(lambda x: letra in x, self.pares))[0]
        return par[0] if par[0] != letra else par[1]


class MaquinaEnigma:
    def __init__(self, rotores: list[Rotor], reflector: Reflector, verbose: bool=False):
        '''
        '''
        self.rotores = rotores
        self.reflector = reflector
        self.verbose = verbose
    
    # Este se ha modificado para que sea más visualmente atractivo
    def moverEntreRotores(self, letra: str, rotor1_index: int, rotor2_index: int) -> str:
        '''
            Mueve la letra entre dos rotores. Rotor 1 es el de origen y Rotor 2 es el de destino
        '''
        rotor1 = self.rotores[rotor1_index]
        rotor2 = self.rotores[rotor2_index]
        # Notar que aquí usamos la cadena derecha siempre porque es ella la que indica la altura de las letra
        return rotor2.cadenaDerecha[rotor1.cadenaDerecha.index(letra)]
    
    def transformar(self, letra: str) -> str:
        '''
            Dada una letra, la transforma a través de los rotores y el reflector
        '''
        letra = letra.upper()
        for i, rotor in enumerate(self.rotores):
            letra = rotor.transformarDerechaIzquierda(letra, self.verbose)
            if i != len(self.rotores) - 1:
                letra = self.moverEntreRotores(letra, i, i+1)
            
        letra = self.reflector.transformar(letra)
        
        for i, rotor in enumerate(self.rotores[::-1]):
            letra = rotor.transformarIzquierdaDerecha(letra, self.verbose)
            if i != len(self.rotores) - 1:
                letra = self.moverEntreRotores(letra, len(self.rotores)-i-1, len(self.rotores)-i-2)
            
        self.rotar()
        
        return letra
    
    def transformarFrase(self, frase: str) -> str:
        respuesta = ''
        for letra in frase:
            letra = self.transformar(letra)
            respuesta += letra
        return f'E({frase}) = {respuesta}'
        
    def rotar(self):
        '''
            Rota los rotores
        '''
        for rotor in self.rotores:
            rotor.rotar()
            # Solamente rotar el siguiente rotor si el rotor actual ha dado una vuelta completa
            if rotor.cadenaDerecha[0] != 'A':
                break

    def __str__(self):
        text = ''
        for i, rotor in enumerate(self.rotores):
            text += f'Rotor {i}\n' + \
                    f'\tDer -> {rotor.cadenaDerecha}\n' + \
                    f'\tIzq -> {rotor.cadenaIzquierda}\n'
                    
        text += 'Reflector:' + \
                f'\t{self.reflector.pares}\n'
                
        return text
    
    def clone(self):
        return MaquinaEnigma([rotor.clone() for rotor in self.rotores], self.reflector, self.verbose)
            

import random
def maquinaRandom():    
    random.seed(0)
    abecedario = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    rotor1 = Rotor(abecedario.copy(), random.sample(abecedario, len(abecedario)))
    rotor2 = Rotor(abecedario.copy(), random.sample(abecedario, len(abecedario)))
    rotor3 = Rotor(abecedario.copy(), random.sample(abecedario, len(abecedario)))
    
    reordenAleatorio = random.sample(abecedario, len(abecedario))
    reflector = Reflector([(reordenAleatorio[i], reordenAleatorio[i+1]) for i in range(0, len(reordenAleatorio), 2)])
    
    maquina = MaquinaEnigma([rotor1, rotor2, rotor3], reflector, verbose=False)
    
    return maquina

rotacionesIniciales = 0
if __name__ == '__main__':
    maquina = maquinaRandom()
    
    for i in range(rotacionesIniciales):
        maquina.rotar()
        
    if len(sys.argv) > 1:
        if sys.argv[1] == '-i': # Modo interactivo
            while True:
                frase = input('Introduce una frase: ')
                print(maquina.transformarFrase(frase))
                
        elif sys.argv[1] == '-g': # Modo gráfico
            import tkinter as tk
            from tkinter import font
            ventana = tk.Tk()
            ventana.title("Transformador Enigma")
            etiqueta_instruccion = tk.Label(ventana, text="Introduce una frase:", font=font.Font(size=20))
            ventana.geometry('500x300')
            etiqueta_instruccion.pack()
            
            font_large = font.Font(family='Times', size=20)

            entrada_frase = tk.Entry(ventana, width=50, font=font_large)
            entrada_frase.pack()

            
            copiaMaquina = maquina.clone()
            def transformarFrase_grafico():
                frase = entrada_frase.get()
                resultado = maquina.transformarFrase(frase)
                etiqueta_resultado.config(text=resultado)
            
            def reiniciarMaquina():
                global maquina
                maquina = copiaMaquina.clone()
                print('Máquina reiniciada')
            
            boton_transformar = tk.Button(ventana, text="Transformar", command=transformarFrase_grafico, font=font_large)
            boton_transformar.pack()
            
            boton_reiniciar = tk.Button(ventana, text="Reiniciar Máquina", command=reiniciarMaquina, font=font_large)
            boton_reiniciar.pack()

            etiqueta_resultado = tk.Label(ventana, text="E() = ", font=font_large)
            etiqueta_resultado.pack()

            # Ejecutar la interfaz gráfica
            ventana.mainloop()
    else:
        frase = 'JCKW'
        print(maquina.transformarFrase(frase))
