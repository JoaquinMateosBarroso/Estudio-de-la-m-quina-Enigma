from maquinaEnigma import MaquinaEnigma, maquinaRandom
import numpy as np

class Bombe:
    def __init__(self, maquina: MaquinaEnigma):
        '''
            Inicializa una Bombe con una máquina Enigma
            
            :param enigma: máquina Enigma a atacar
        '''
        self.maquina = maquina


    def descubrirPosicionRotores(self, turingLoops: list[list[tuple[int,str]]]):
        '''
            Descubre la posición inicial de los rotores de la máquina Enigma
            
            :param turingLoop: lista de letras que se sabe que forman parte del turing loop, de la forma [(0,a), (1,b), (3,c)].
                                Tiene que cumplirse que, al inicio, 'a' se convierta en 'b', tras una rotación, 'b' se convierta en 'c',
                                y tras 3 rotaciones, 'c' se convierta en 'a'.
        '''
        maquinasValidas: list = []
        # Probamos todas las combinaciones posibles de rotaciones
        for rotacionesRealizadas in range(26**3):
            maquina = self.maquina.clone()
            esValida = np.all([self.verificarTuringLoop(maquina.clone(), tl) for tl in turingLoops])
            if esValida:
                maquinasValidas.append((rotacionesRealizadas, maquina))

            # Rotamos la máquina para la siguiente iteración
            self.maquina.rotar()
        
        return maquinasValidas
    
    def verificarTuringLoop(self, maquina, turingLoop):
        # Recorremos el loop para ver si se cumplen las condiciones
        rotacionesActuales = 0
        for i, item in enumerate(turingLoop):
            rotorIndex, letraOriginal = item
            # Ponemos la máquina en la posición asociada a la letra actual
            while rotacionesActuales < rotorIndex:
                maquina.rotar()
                rotacionesActuales += 1
            
            # Comprobamos si la letra actual se convierte en la siguiente; si no lo hace, esta máquina no es válida
            letraTransformada = maquina.transformar(letraOriginal)
            rotacionesActuales += 1 # Se rota siempre que se transforma una letra
            if letraTransformada != turingLoop[(i+1)%len(turingLoop)][1]:
                return False
            
        # Si no se ha roto el bucle, la máquina es válida
        return True

    
if __name__ == '__main__':
    maquinaBase = maquinaRandom()
    bombe = Bombe(maquinaBase)
    maquinasValidas = bombe.descubrirPosicionRotores([[(2, 'G'), (3, 'Z'), (4, 'J')],
                                                      [(2, 'H')]])
    
    for rotaciones, maquina in maquinasValidas:
        print(f'Rotaciones realizadas: {rotaciones}')
        print(f'Máquina válida: {maquina}')
        print('')
        
    print('***********************************')
    print('En total, se han encontrado', len(maquinasValidas), 'máquinas válidas')
    print('Sus rotaciones iniciales son las siguientes:')
    print([rotaciones for rotaciones, _ in maquinasValidas])