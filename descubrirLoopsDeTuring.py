from maquinaEnigma import MaquinaEnigma, maquinaRandom


def descubrirLoopsDeTuring(maquinaOriginal: MaquinaEnigma):
    '''
        Descubre los loops de Turing de una máquina Enigma
        
        :param maquina: máquina Enigma a atacar
    '''
    turingLoops = []
    letrasIniciales = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    # Probamos todas las combinaciones posibles de rotaciones
    for letraInicial in letrasIniciales:
        # Probamos tomando la letra inicial como la primera, segunda o tercera introducida
        for rotorIndex in range(3):
            maquina = maquinaOriginal.clone()
            for _ in range(rotorIndex):
                maquina.rotar()
            turingLoop = [(rotorIndex, letraInicial)]
            rotacionesActuales = rotorIndex
            letraOrigen = letraInicial
            while True:
                letraTransformada = maquina.transformar(letraOrigen)
                rotacionesActuales += 1
                if letraTransformada == letraInicial:
                    break
                turingLoop.append((rotacionesActuales, letraTransformada))
                letraOrigen = letraTransformada
            
            if len(turingLoop) <= 3:
                turingLoops.append(turingLoop)
    
    return turingLoops


if __name__ == '__main__':
    from maquinaEnigma import rotacionesIniciales
    maquinaBase = maquinaRandom()
    for i in range(rotacionesIniciales):
        maquinaBase.rotar()
        
    turingLoops = descubrirLoopsDeTuring(maquinaBase)
    print(turingLoops)