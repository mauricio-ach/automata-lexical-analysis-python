import re

class Automata(object):
    #Constructor de la clase
    def __init__(self, states, initial, final, transitions):
        self.states = states
        self.initial = initial
        self.final = final
        self.transitions = transitions

    def print(self):
        print("Automata:")
        print(f"Estados: {self.states}")
        print(f"Estado inicial: {self.initial}")
        print(f"Estado final: {self.final}")
        print("Transiciones:")
        for transition in self.transitions:
            print(transition)

    #Funcion delta del automata
    def delta(self, state, character):
        if state in self.states:
            for transition in self.transitions:
                if(transition[0] == [state, character]):
                    return transition[1]
        return None
    
    #Obtiene la epsilon cerradura de un estado
    def e_closure(self, state):
        states = [state]

        for transition in self.transitions:
            if transition[0] == [state, 'epsilon']:
                if transition[1] not in states:
                    states.append(transition[1])
                    states.extend(self.e_closure(transition[1]))
        return states
    
    #Obtiene la epsilon cerradura de un conjunto de estados
    def e_closure_set(self, set):
        states = []

        for state in set:
            e_closure = self.e_closure(state)
            if e_closure not in states:
                states.append(e_closure)

        states = [item for sublist in states for item in sublist]

        unique_states = []

        for item in states:
            if item not in unique_states:
                unique_states.append(item)

        unique_states.sort()
        return [unique_states]
    
    #Elimina una transicion ya registrada
    def remove_transition(self, transition):
        if transition in self.transitions:
            self.transitions.remove(transition)

    #Define si el automata acepta una cadena
    def accepts(self, string):
        
        current_state = self.initial
        #print(f"Empezamos en {current_state}")

        for char in string:
            #print(f"Procesamos caracter '{char}'")
            current_state = self.delta(current_state, char)
            if(current_state == None):
                break
            #print(f"Cambiamos a {current_state}")
        
        if current_state == None or current_state not in self.final:
            return False
        
        return True
        
    #Convierte un automata finito no determinista
    #en un automata finito determinista
    def nfa_to_dfa(self, alphabet):
        s0 = self.e_closure_set([self.initial])
        queue = [s0]
        set_states = [s0]
        transitions = []

        while queue:
            current_state = queue.pop()

            s_i = []
            
            for states in current_state:
                for char in alphabet:
                    for state in states:                        
                        reachable_state = self.delta(state,char)
                        if reachable_state not in s_i and reachable_state is not None:
                            s_i.append(reachable_state)
                            transitions.append([[state, char], reachable_state])
                            
            s_i = self.e_closure_set(s_i)
            
            if s_i != [[]] and s_i not in set_states:
                set_states.append(s_i)
                queue.append(s_i)

        return self.construct_dfa(set_states, transitions)
        

    def construct_dfa(self, set_states, valid_transitions):
        state_label = 0
        states = []
        dfa_states = []
        final_states = []
        initial_state = 0
        transitions = []
        
        #construct the new states
        for state in set_states:
            states.append([state_label,state[0]])
            dfa_states.append(state_label)
            if self.final in state[0]:
                final_states.append(state_label)

            if self.initial in state[0]:
                initial_state = state_label            

            state_label += 1

        #constructut the new transitions
        for state in states:
            for transition in valid_transitions:             
                transition_state = transition[0][0]
                transition_char = transition[0][1]
                transition_target = transition[1]                
                if transition_state in state[1]:                    
                    for aux_state in states:
                        if transition_target in aux_state[1]:
                            target_state = aux_state[0]
                            new_transition = [[aux_state[0]-1, transition_char], target_state]
                            transitions.append(new_transition)

        return Automata(dfa_states, initial_state, final_states, transitions)

    
    #Regresa la posicion de un token cuando 
    #es aceptado por el automata
    def match_token(self, string):
        result = []

        for index,token in enumerate(string):
            if self.accepts(token):
                result.append([index,token])
        
        return result

# A partir de una expresion regular, se construye un automata utilizando el algoritmo
# de Thompson
def compile(regex):
    automatons = []
    process_next = True

    for index,char in enumerate(regex):
        if process_next:
            if char == '|':
                nfa1 = automatons.pop()
                nfa1_qf = max(nfa1.states)
                                
                if [[nfa1_qf -1, regex[index - 1]], nfa1_qf] in nfa1.transitions:
                    nfa1.remove_transition([[nfa1_qf -1, regex[index - 1]], nfa1_qf])
                    q_previous = nfa1_qf -1
                    qi_1 = nfa1_qf + 1
                    qf_1 = nfa1_qf + 2
                    qi_2 = nfa1_qf + 3
                    qf_2 = nfa1_qf + 4
                    qf = nfa1.final
                    next_char = regex[index+1]
                    previous_char = regex[index-1]

                    new_transititions = [
                        [[q_previous, 'epsilon'], qi_1],
                        [[q_previous, 'epsilon'], qi_2],
                        [[qi_1, previous_char], qf_1],
                        [[qi_2, next_char], qf_2],
                        [[qf_1, 'epsilon'], qf],
                        [[qf_2, 'epsilon'], qf]
                    ]

                    states = nfa1.states + [qi_1,qf_1,qi_2,qf_2]

                    transitions = nfa1.transitions + new_transititions

                    automatons.append(Automata(states, nfa1.initial, qf, transitions))
                process_next = False

            elif char == '*':
                nfa1 = automatons.pop()
                nfa1_qi = nfa1.initial
                nfa1_qf = max(nfa1.states)
                qi = nfa1_qf + 1
                qf = nfa1_qf + 2

                new_transititions = [
                    [[nfa1_qf, 'epsilon'], qf],
                    [[nfa1_qf, 'epsilon'], nfa1_qi],
                    [[qi, 'epsilon'], nfa1_qi],
                    [[qi, 'epsilon'], qf]
                ]

                transitions = nfa1.transitions + new_transititions

                automatons.append(Automata(states + [qi,qf], qi, qf, transitions))
                process_next = True

            elif char == '?':                
                nfa1 = automatons.pop()
                nfa1_qf = nfa1.final
                last_transition = nfa1.transitions.pop()
                nfa1.remove_transition(last_transition)
                q_previous = last_transition[0][0]
                qi_1 = nfa1_qf + 1
                qf_1 = nfa1_qf + 2
                qi_2 = nfa1_qf + 3
                qf_2 = nfa1_qf + 4
                qf = nfa1.final
                previous_char = regex[index-1]

                new_transititions = [
                        [[q_previous, 'epsilon'], qi_1],
                        [[q_previous, 'epsilon'], qi_2],
                        [[qi_1, previous_char], qf_1],
                        [[qi_2, 'epsilon'], qf_2],
                        [[qf_1, 'epsilon'], qf],
                        [[qf_2, 'epsilon'], qf]
                    ]

                states = nfa1.states + [qi_1,qf_1,qi_2,qf_2]

                transitions = nfa1.transitions + new_transititions

                automatons.append(Automata(states, nfa1.initial, qf, transitions))
                    
                process_next = True
                    
            else:
                if automatons == []:
                    qi = 0
                    qf = 1
                    transitions = [
                        [[qi,char], qf]
                    ]
                    automatons.append(Automata([qi,qf], qi, qf, transitions))
                else:
                    nfa1 = automatons.pop()
                    qi = nfa1.initial
                    nfa1_qf = nfa1.final
                    qf = max(nfa1.states) + 1

                    states = nfa1.states + [qf]
                    new_transititions = [
                        [[nfa1_qf, char],qf]
                    ]
                    transitions = nfa1.transitions + new_transititions

                    automatons.append(Automata(states, qi, qf, transitions))
                process_next = True
        else:            
            process_next = True
    
    return automatons.pop()

def tokenize(string):
    tokens = re.findall(r'\b\w+\b', string)
    return tokens

regex = "niña|os?"
print("Expresion regular: ", regex)
nfa = compile(regex)
print("Automata NFA")
nfa.print()
dfa = nfa.nfa_to_dfa("niñaos")

print()
print("Automata DFA")
dfa.print()

#Cadenas que acepta
print()
print("DFA acepta niño: ",dfa.accepts("niño"))
print("DFA acepta niña: ",dfa.accepts("niña"))
print("DFA acepta niñas: ",dfa.accepts("niñas"))
print("DFA acepta niños: ",dfa.accepts("niños"))
print("DFA acepta niñs: ",dfa.accepts("niñs"))

text = 'Las niñas extranjeras jugaban con el niño y la niña en el patio.'
tokens = tokenize('Las niñas extranjeras jugaban con el niño y la niña en el patio.')

print()
print("Procesando el texto y obteniendo la posicion de los tokens aceptados")
print("Texto: ", text)
print(dfa.match_token(tokens))