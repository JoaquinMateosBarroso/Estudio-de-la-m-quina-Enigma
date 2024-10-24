
class Rotor:
    def __init__(self, cadenaDerecha: list[str], cadenaIzquierda: list[str]):
        '''
            Inicializa un rotor que transforma las letras de cadenaDerecha en las de cadenaIzquierda
        
            :param cadenaDerecha: lista de letras que se transforman
            :param cadenaIzquierda: lista de letras a las que se transforman
        '''
        self.cadenaDerecha = cadenaDerecha
        self.cadenaIzquierda = cadenaIzquierda
        
    def transformarDerechaIzquierda(self, letra: str, verbose: bool) -> str:
        '''
            Transforma la letra dada por la letra correspondiente en la cadenaIzquierda
        
            :param letra: letra a transformar
            :return: letra transformada
        '''
        if verbose:
            print(f"{self.cadenaIzquierda[self.cadenaDerecha.index(letra)]}<-{letra}")
        
        return self.cadenaIzquierda[self.cadenaDerecha.index(letra)]
    
    def transformarIzquierdaDerecha(self, letra: str, verbose: bool) -> str:
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
        self.cadenaDerecha = self.cadenaDerecha[1:] + list(self.cadenaDerecha[0])
        self.cadenaIzquierda = self.cadenaIzquierda[1:] + list(self.cadenaIzquierda[0])


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
    
    def moverEntreRotores(self, letra: str, rotor1_index: int, rotor2_index: int) -> str:
        '''
            Mueve la letra entre dos rotores. Rotor 1 es el de origen y Rotor 2 es el de destino
        '''
        rotor1 = self.rotores[rotor1_index]
        rotor2 = self.rotores[rotor2_index]
        if rotor1_index < rotor2_index:
            # Movemos de derecha a izquierda
            return rotor2.cadenaDerecha[rotor1.cadenaIzquierda.index(letra)]
        else:
            # Movemos de izquierda a derecha
            return rotor2.cadenaIzquierda[rotor1.cadenaDerecha.index(letra)]
    
    def transformar(self, letra: str) -> str:
        '''
            Dada una letra, la transforma a través de los rotores y el reflector
        '''
        for i, rotor in enumerate(self.rotores):
            letra = rotor.transformarDerechaIzquierda(letra, self.verbose)
            if i != len(self.rotores) - 1:
                letra = self.moverEntreRotores(letra, i, i+1)
            
        letra = self.reflector.transformar(letra)
        
        for i, rotor in list(enumerate(self.rotores))[::-1]:
            letra = rotor.transformarIzquierdaDerecha(letra, self.verbose)
            if i != len(self.rotores) - 1:
                letra = self.moverEntreRotores(letra, i, i-1)
            
        self.rotar()
        
        return letra
    
    def rotar(self):
        '''
            Rota los rotores
        '''
        for rotor in self.rotores:
            rotor.rotar()
            # Solamente rotar el siguiente rotor si el rotor actual ha dado una vuelta completa
            if rotor.cadenaDerecha[0] != 'A':
                break
            

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


if __name__ == '__main__':
    maquina = maquinaRandom()
    letra = maquina.transformar('A')
    i = 1
    while letra != 'A':
        letra = maquina.transformar(letra)
        i+=1
    print(i)