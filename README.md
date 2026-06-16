# MemSim — Simulador de Memória Virtual

**Disciplina:** Sistemas Operacionais — 2026/I | PUCRS  
**Professor:** Filipo Mór  
**Grupo 15:** Ana Paula Pereira, Arthur R. Ferreira, João Olivas, Luthero Vargas

---

## O que é

Simula o comportamento da paginação em memória virtual com dois algoritmos de substituição de páginas: **LRU** e **LFU**. A cada acesso, exibe o estado dos frames e ao final mostra as estatísticas.

## Como executar

```bash
python simulador_memoria.py entrada.txt LRU
python simulador_memoria.py entrada.txt LFU
```

O arquivo de entrada tem o número de frames na primeira linha, seguido da sequência de páginas acessadas.

## Resultados (entrada.txt, 3 frames)

LRU

Total de Acessos: 12
Total de Page Faults: 9
Taxa de Page Faults: 75.00%
Mapa final: [F0]: 0, [F1]: 3, [F2]: 2

LFU

Total de Acessos: 12
Total de Page Faults: 8
Taxa de Page Faults: 66.67%
Mapa final: [F0]: 3, [F1]: 0, [F2]: 2

O LFU teve desempenho ligeiramente melhor nessa sequência, economizando 1 page fault em relação ao LRU. Isso acontece porque o LFU protege páginas que já foram carregadas múltiplas vezes — quanto mais vezes uma página gerou page fault, maior sua "prioridade" de permanência na memória. Em sequências onde as mesmas páginas precisam ser recarregadas repetidamente, isso evita substituições desnecessárias.

O LRU toma decisões puramente pela recência do acesso. Isso o prejudica em momentos onde uma página popular ficou brevemente sem ser acessada: ela acaba sendo substituída mesmo sendo útil logo em seguida, gerando page faults evitáveis.

Vale notar que essa vantagem do LFU não é universal. Em sequências com muitos acessos únicos ou padrões sequenciais, páginas antigas acumulam contadores altos e ocupam frames mesmo sem uso recente, o que pode piorar o desempenho. A escolha do melhor algoritmo depende sempre do padrão de acesso da carga de trabalho.
