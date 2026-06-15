###
###     S I M U L A D O R    D E    M E M Ó R I A
###
### Prof. Filipo - github.com/ProfessorFilipo/MemSim/
###

import sys


class Frame:
    def __init__(self, id_frame):
        self.id_frame = id_frame
        self.pagina_alocada = None
        self.ultimo_acesso = -1  


class TabelaPaginas:
    #start
    
    
    
    
    #end

    def acessar_pagina(self, numero_pagina):
        self.total_acessos += 1
        self.tempo += 1

        # Verifica Hit
        for frame in self.frames:
            if frame.pagina_alocada == numero_pagina:
                frame.ultimo_acesso = self.tempo
                return True, frame.id_frame

        # Page Fault
        self.total_page_faults += 1

        # Procura frame vazio
        for frame in self.frames:
            if frame.pagina_alocada is None:
                frame.pagina_alocada = numero_pagina
                frame.ultimo_acesso = self.tempo
                return False, frame.id_frame

        # Memória cheia -> aplica LRU
        frame_vitima_id = self.substituir_pagina(numero_pagina)

        return False, frame_vitima_id

    def substituir_pagina(self, nova_pagina):
        """
        Algoritmo LRU (Least Recently Used)
        Remove a página menos recentemente utilizada.
        """

        frame_vitima = min(
            self.frames,
            key=lambda frame: frame.ultimo_acesso
        )

        frame_vitima.pagina_alocada = nova_pagina
        frame_vitima.ultimo_acesso = self.tempo

        return frame_vitima.id_frame

    def imprimir_mapa_memoria(self, passo, pagina_acessada,
                               foi_hit, frame_alterado=None):

        status = "Hit" if foi_hit else "Page Fault"

        print(
            f"\n--- Passo {passo}: "
            f"Acesso à Página {pagina_acessada} ({status}) ---"
        )

        for frame in self.frames:

            if frame.pagina_alocada is None:
                conteudo = "[Vazio]"
            else:
                conteudo = f"Página {frame.pagina_alocada}"

            marcador = ""

            if not foi_hit and frame.id_frame == frame_alterado:
                marcador = " <-- Alterado"

            print(f"[Frame {frame.id_frame}]: {conteudo}{marcador}")

        print("-" * 40)


class Simulador:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo

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

        tabela_paginas = TabelaPaginas(num_frames)

        print(
            f"Iniciando simulação com "
            f"{num_frames} frames disponíveis."
        )

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


if __name__ == "__main__":

    arquivo_entrada = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "entrada.txt"
    )

    simulador = Simulador(arquivo_entrada)

    simulador.executar()