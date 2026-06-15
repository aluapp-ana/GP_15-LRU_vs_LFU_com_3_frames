###
###     S I M U L A D O R    D E    M E M Ó R I A
###
### Prof. Filipo - github.com/ProfessorFilipo/MemSim/
### Sistemas Operacionais – 2026/I | PUCRS
### Grupo 15: LRU vs. LFU (3 frames)

import sys


class Frame:

    def __init__(self, id_frame):
        self.id_frame = id_frame
        self.pagina_alocada = None

        # LRU - instante do último acesso à página neste frame
        # menor valor = usado há mais tempo = candidato à remoção
        self.ultimo_acesso = -1

        # LFU - Total de acessos à página desde que foi carregada
        # menor valor = menos frequente = candidato à remoção
        self.contador = 0

        # LFU - Instante em que a página foi carregada neste frame
        # usado como desempate: página mais antiga é removida primeiro (FIFO)
        self.ordem_entrada = 0

    def esta_vazio(self):
        return self.pagina_alocada is None


class TabelaPaginas:

    def __init__(self, num_frames, algoritmo):
        self.frames = [Frame(i) for i in range(num_frames)]
        self.total_page_faults = 0
        self.total_acessos = 0
        self.algoritmo = algoritmo.upper()

        # relógio global, avança a cada acesso
        # timestamp para LRU e como ordem de carga para LFU
        self.tempo = 0

    def acessar_pagina(self, numero_pagina):
        self.total_acessos += 1
        self.tempo += 1

        # verificar hit
        for frame in self.frames:
            if frame.pagina_alocada == numero_pagina:

                if self.algoritmo == 'LRU':
                    frame.ultimo_acesso = self.tempo

                elif self.algoritmo == 'LFU':
                    frame.contador += 1

                return True, frame.id_frame

        # Page Fault
        self.total_page_faults += 1

        # procura frame vazio
        for frame in self.frames:
            if frame.esta_vazio():
                frame.pagina_alocada = numero_pagina
                frame.ultimo_acesso = self.tempo
                frame.contador = 1
                frame.ordem_entrada = self.tempo
                return False, frame.id_frame

        # memória cheia: aplica o algoritmo de substituição
        frame_vitima_id = self.substituir_pagina(numero_pagina)
        return False, frame_vitima_id

    def substituir_pagina(self, nova_pagina):
        """
        LRU: remove a página cujo último acesso foi há mais tempo
             (menor valor de ultimo_acesso).

        LFU: remove a página com menor número de acessos (contador).
             Empate resolvido pela página carregada há mais tempo
             (menor ordem_entrada) — critério FIFO.
        """

        if self.algoritmo == 'LRU':
            frame_vitima = min(
                self.frames,
                key=lambda frame: frame.ultimo_acesso
            )

        elif self.algoritmo == 'LFU':
            frame_vitima = min(
                self.frames,
                key=lambda frame: (frame.contador, frame.ordem_entrada)
            )

        frame_vitima.pagina_alocada = nova_pagina
        frame_vitima.ultimo_acesso = self.tempo
        frame_vitima.contador = 1
        frame_vitima.ordem_entrada = self.tempo

        return frame_vitima.id_frame

    def imprimir_mapa_memoria(self, passo, pagina_acessada,
                               foi_hit, frame_alterado=None):

        status = "Hit" if foi_hit else "Page Fault"

        print(
            f"\n--- Passo {passo}: "
            f"Acesso à Página {pagina_acessada} ({status}) ---"
        )

        for frame in self.frames:

            if frame.esta_vazio():
                conteudo = "[Vazio]"
            else:
                conteudo = f"Página {frame.pagina_alocada}"

            marcador = ""

            if not foi_hit and frame.id_frame == frame_alterado:
                marcador = " <-- Alterado"

            print(f"[Frame {frame.id_frame}]: {conteudo}{marcador}")

        print("-" * 40)


class Simulador:

    def __init__(self, caminho_arquivo, algoritmo):
        self.caminho_arquivo = caminho_arquivo
        self.algoritmo = algoritmo

    def executar(self):

        try:
            with open(self.caminho_arquivo, 'r') as arquivo:
                linhas = arquivo.readlines()

        except FileNotFoundError:
            print(
                f"Erro: O arquivo '{self.caminho_arquivo}' "
                f"não foi encontrado."
            )
            return

        linhas = [
            l.strip()
            for l in linhas
            if l.strip() and not l.strip().startswith('#')
        ]

        if not linhas:
            print("Erro: Arquivo de entrada vazio.")
            return

        num_frames = int(linhas[0])

        tabela_paginas = TabelaPaginas(num_frames, self.algoritmo)

        print(
            f"Iniciando simulação com "
            f"{num_frames} frames disponíveis."
        )
        print(f"Algoritmo: {self.algoritmo}")
        print("=" * 40)

        passo = 1

        for linha in linhas[1:]:

            numero_pagina = int(linha)

            foi_hit, frame_id = (
                tabela_paginas.acessar_pagina(numero_pagina)
            )

            tabela_paginas.imprimir_mapa_memoria(
                passo,
                numero_pagina,
                foi_hit,
                frame_id
            )

            passo += 1

        print("\n================ STATS FINAIS ================")

        print(
            f"Total de Acessos: "
            f"{tabela_paginas.total_acessos}"
        )

        print(
            f"Total de Page Faults: "
            f"{tabela_paginas.total_page_faults}"
        )

        if tabela_paginas.total_acessos > 0:

            taxa_faults = (
                tabela_paginas.total_page_faults
                / tabela_paginas.total_acessos
            ) * 100

            print(
                f"Taxa de Page Faults: "
                f"{taxa_faults:.2f}%"
            )

        print("==============================================")

# instruções de como rodar cada algoritmo
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Uso: python simulador_memoria.py <arquivo_entrada> <algoritmo>")
        print("     Algoritmos disponíveis: LRU | LFU")
        print("Exemplo: python simulador_memoria.py entrada.txt LRU")
        sys.exit(1)

    arquivo_entrada = sys.argv[1]
    algoritmo = sys.argv[2].upper()

    if algoritmo not in ('LRU', 'LFU'):
        print(f"Erro: Algoritmo '{sys.argv[2]}' não reconhecido.")
        print("      Use LRU ou LFU.")
        sys.exit(1)

    simulador = Simulador(arquivo_entrada, algoritmo)
    simulador.executar()