MemSim — Simulador de Gerência de Memória Virtual
Disciplina: Sistemas Operacionais
Professor: Filipo Mór
---------------------------------------------------
Grupo 15: LRU vs. LFU (3 frames)
Integrantes: Ana Paula Pereira, Arthur R. Ferreira, João Olivas, Luthero Vargas

Descrição:<br>
Simulador de paginação em memória virtual que implementa dois algoritmos de substituição de páginas: LRU (Least Recently Used) e LFU (Least Frequently Used). A cada acesso, o programa exibe o estado completo dos frames físicos e ao final apresenta as estatísticas consolidadas.

Como executar:
Escreva no terminal: 
- python simulador_memoria.py <arquivo_entrada> <algoritmo_desejado>

- Exemplo:
    - python simulador_memoria.py entrada.txt LRU

Estatísticas finais alcançadas:

- LRU
    - Total de Acessos: 12
    - Total de Page Faults: 9
    - Taxa de Page Faults: 75.00%
    - Mapa final: [F0]: 0, [F1]: 3, [F2]: 2


- LFU
    - Total de Acessos: 12
    - Total de Page Faults: 8
    - Taxa de Page Faults: 66.67%
    - Mapa final: [F0]: 3, [F1]: 0, [F2]: 2