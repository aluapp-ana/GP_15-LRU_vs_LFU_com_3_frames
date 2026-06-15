MemSim — Simulador de Gerência de Memória Virtual
Disciplina: Sistemas Operacionais
Professor: Filipo Mór
---------------------------------------------------
Grupo 15: LRU vs. LFU (3 frames)
Integrantes: Ana Paula Pereira, Arthur R. Ferreira, João Olivas, Luthero Vargas

Descrição:
Simulador de paginação em memória virtual que implementa dois algoritmos de substituição de páginas: LRU (Least Recently Used) e LFU (Least Frequently Used). A cada acesso, o programa exibe o estado completo dos frames físicos e ao final apresenta as estatísticas consolidadas.

Como executar:
Escreva no terminal: 
        python simulador_memoria.py <arquivo_entrada> <algoritmo>

    - Exemplo: python simulador_memoria.py entrada.txt LRU
