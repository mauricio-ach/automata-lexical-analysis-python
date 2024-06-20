# Implementación de un autómata para análisis léxico en Python

## Objetivo
En este repositorio se encuetra la implementación de diversos algoritmos que se aplican en el análisis léxico de compiladores (principalmente en automátas). Se deja la implementación como pública para ser reutilizada o mejorada, cualquier comentario es bienvenido.

## Funcionamiento

1. Se define una expresión regular
2. Se utiliza el algoritmo de construcción de Thompson para NFA (Nondeterministic Finite Automata)
3. Se utiliza el algoritmo para conversión de NFA a DFA (Deterministic Finite Automata)
4. Se procesan cadenas para verificar si son aceptadas por el autómata construido

## Posibles mejoras
1. Implementación del algoritmo de DFA mínimo después de construir el DFA.
