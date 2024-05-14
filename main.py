
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)




class MonteCarlo:

    def __init__(self, *args):

        self.lines = args[0] # Linhas da matriz
        self.columns = args[1] # colunas da matriz
        self.p = args[2] # Seed aleatória
        self.obj_size = args[3] # tamanho do objeto de preenchimento
        self.omega = np.zeros((self.lines, self.columns))
        self.matrix_columns = np.arange(self.columns) # Colunas restantes para aleatoriedade
        self.matrix_lines = np.arange(self.lines)   # Linhas restantes para aleatoriedade
        self.memory = [[(i, j) for j in range(self.columns)] for i in range(self.lines)] # Memória de todas as casas (ocupadas ou não) [ocupadas representadas por coordenadas negativas]
        self.partial_alteration()

    def is_there_impossibility(self, coor):
        """ Método que verifica quais possibilidades não geram impossibilidades
        Entrada => coor (= coordenada inicial aleatória [linha, coluna]); t := (= instante de tempo atual)
        Saída => Vazia
        """
        array = [] # Return do método
        memory_vertical = [] # Armazena todas as possibilidades verticais
        memory_horizontal = [] # Armazena todas as possibilidades horizontais
        list =  [i for i in range(1, self.obj_size)] # Cria todos os indices possiveis de se encontrar uma possibilidade


        for counter in list: # Possibilidades conforme o tamanho do objeto de preenchimento
            try:
                memory_horizontal.append((coor[0], coor[1]-counter)) if (coor[0], coor[1]-counter) == self.memory[coor[0]][coor[1]-counter] else print(f"horizontal negativo {-counter}")
            except (IndexError, TypeError):
                pass
            try:
                memory_horizontal.append((coor[0], coor[1]+counter)) if (coor[0], coor[1]+counter) == self.memory[coor[0]][coor[1]+counter] else print(f"horizontal positivo {counter}")
            except (IndexError, TypeError):
                pass
            try:
                memory_vertical.append((coor[0]-counter, coor[1])) if (coor[0]-counter, coor[1]) == self.memory[coor[0]-counter][coor[1]] else print(f"vertical negativo {-counter}")
            except (IndexError, TypeError):
                pass
            try:
                memory_vertical.append((coor[0]+counter, coor[1])) if (coor[0]+counter, coor[1]) == self.memory[coor[0]+counter][coor[1]] else print(f"vertical positivo {counter}")
            except (IndexError, TypeError):
                pass
        sorted(memory_horizontal, key= lambda horizontal: horizontal[1]) # Ordena as possibilidades horizontais conforme o y da coordenas
        sorted(memory_vertical, key= lambda vertical: vertical[0]) # Ordena as possibilidades verticais conforme o x da coordenas


        return([memory_vertical, memory_horizontal])



    def choices(self, array, coor):
        """ Metodo que recebe as possibilidades que não geram impossibilidades futuras, escolhe se o objeto ficará na vertical ou na horizontal
        e escolhe as coordenadas adjacentes de uma forma aleatória
        Entrada => array (:= array bidimensional onde a primeira linha são as possibilidades verticais e a segunda horizontais)
        Saída => array (:= array com as escolhas aleatorias de como e onde o objeto ocupará no espaço)
        """

        choice = array[np.random.choice([0, 1], 1, p=[1/2 for i in range(2)])[0]]
        choice = choice[np.random.choice([i for i in range(len(choice))], 1, p=[1/len(choice) for i in range(len(choice))])[0]]
        final = []
        index = 0
        for i in range(2):

            if (choice in array[i]):
                index = array[i].index(choice)
                if (len(array[i]) == self.obj_size-1):
                    final.append(array[i])
                    break
                if (choice < tuple(coor)): # movimentos horizontais
                    if (len(array[i][index::]) >= self.obj_size):
                        final.append(array[i][index:index+self.obj_size-1]) # Adiciona as coordenadas restantes do objeto e que são unica e excluivamente menores que a coordenada final escolhida ao acaso
                        break

                    else:
                        final.append(array[i][index-self.obj_size-len(array[i][index:]):]) # Adicona as coordenas restantes do objeto de preenchimento e que podem ser maiores ou menores que a coordenada final escolhida ao acaso
                        break

                else:
                    if ((len(array[i][:index+1]) >= self.obj_size)):
                        final.append(array[i][index-(self.obj_size-1):index])
                        break

                    else:
                        final.append(array[i][:len(array[i][:index+1])-(len(array[i][:index+1])-(self.obj_size-1))])
                        break

        return final, coor



    def partial_alteration(self):

        """
        Metodo que verifica se a coordenada aletória está ocupada ou não e encaixa o objeto de preenchimento
        Entrada => Vazia
        Saída => Vazia
        """
        for t in range(int((self.lines*self.columns)/self.obj_size)):
            random_variable_column = np.random.choice(self.matrix_columns, 1, p=[1/len(self.matrix_columns) for i in range(len(self.matrix_columns))])[0]
            random_variable_line = np.random.choice(self.matrix_lines, 1, p=[1/len(self.matrix_lines) for i in range(len(self.matrix_lines))])[0]
            self.memory[random_variable_line][random_variable_column] = (-random_variable_line, -random_variable_column) if (random_variable_line, random_variable_column) == self.memory[random_variable_line][random_variable_column] else print(f"memoria ja ocupada {self.memory[random_variable_line][random_variable_column]}")
            self.omega[random_variable_line, random_variable_column] = t+1 if self.memory[random_variable_line][random_variable_column] == (-random_variable_line, -random_variable_column) else print(f"omega ocupado {self.memory[random_variable_line][random_variable_column]}")
            self.alteration(self.choices(self.check_impossibility(self.is_there_impossibility([random_variable_line, random_variable_column]), [random_variable_line, random_variable_column]), [random_variable_line, random_variable_column]), t+1)



    def check_impossibility(self, array, coor):
        """ Método que ao receber as possibilidades de uma coordenada aleatória, remove as possibilidades que fariam a cadeia não ficar
            homogenea no final do processo
            Entada => array (:= array com duas dimensoes, onde a primeira representa as possibilidades verticais e a segunda, as possibilidades horizontais)
            Saída => filtered_array (:= array de duas dimensões filtrada)
        """
        dict = {1 : 1, 0.99 : 0, 0.98 : -1, -1: 1, -0.99 : -1, -0.98 : 0}
        possibility = []
        pos = []
        possible = False
        for line in array:
            for column in line:
                for x, y in dict.items():
                    try:
                        if ([column[0]+int(x), column[1]+int(y)] != [coor[0], coor[1]]):
                            for i in self.is_there_impossibility([column[0]+int(x), column[1]+int(y)]):
                                if (len(i) < self.obj_size-1):
                                    continue

                                else:
                                    possible = True
                    except:
                        continue

                    if (possible == True):
                        possibility.append(column)
                        possible = False
            pos.append(list(set(possibility)))
            possibility = []


        pos[0] = sorted(pos[0], key=lambda j: j[0])
        pos[1] = sorted(pos[1], key=lambda j: j[1])

        return pos


    def alteration(self, list, t):
        """ Metodo de interação que remove as coordenadas aleatorias que compõem o objeto de preenchimento e a diferencia na matriz da cadeia
            Entrada => args := (= choice [escolha aleatória], = t [instante de tempo atual])
            Saída => Vazia
        """

        breakpoint()


        # choice = args[0]
        # t = args[1]
        # for line, column in choice:
        #     self.memory[line][column] = (-line, -column)
        #     self.omega[line, column] = t
