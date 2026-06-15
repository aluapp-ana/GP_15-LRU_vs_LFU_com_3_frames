###
###     S I M U L A D O R    D E    M E M Ó R I A
###
### Prof. Filipo - github.com/ProfessorFilipo/MemSim/
###

import sys

class Frame:
    
    def __init__(self, id_frame: int):
        self.id_frame = id_frame
        self.pagina_alocada = None   # frame começa vazio
        self.contador = 0
        self.ordem_entrada = 0

    def esta_vazio(self) -> bool:
        return self.pagina_alocada is None

class TabelaPaginas:
    
    def __init__(self, num_frames: int):
        self.frames = [Frame(i) for i in range(num_frames)]
        self.ordem_global = 0   # desempate FIFO: página mais antiga tem menor valor

    def buscar_pagina(self, pagina: int):
        for frame in self.frames:
            if frame.pagina_alocada == pagina:
                return frame
        return None

    def primeiro_frame_vazio(self):
        for frame in self.frames:
            if frame.esta_vazio():
                return frame
        return None

    def escolher_vitima(self) -> "Frame":
        frame_vitima = min(
            self.frames,
            key=lambda frame: (frame.contador, frame.ordem_entrada)
        )
        return frame_vitima

    def substituir_pagina(self, frame: "Frame", nova_pagina: int) -> int:
        self.ordem_global += 1            # avança relógio global a cada nova carga
        frame.pagina_alocada = nova_pagina
        frame.contador = 1                # entrada já conta como 1 acesso
        frame.ordem_entrada = self.ordem_global
        return frame.id_frame

class Simulador:

    def __init__(self, num_frames: int, sequencia: list):
        self.tabela = TabelaPaginas(num_frames)
        self.sequencia = sequencia
        self.total_acessos = 0
        self.total_page_faults = 0

    def acessar_pagina(self, pagina: int):
        self.total_acessos += 1

        # --- HIT: página já está na memória ---
        frame_hit = self.tabela.buscar_pagina(pagina)
        if frame_hit is not None:
            frame_hit.contador += 1   # incrementa frequência da página
            return "Hit", None

        # --- PAGE FAULT ---
        self.total_page_faults += 1

        # Caso 1: ainda existe frame vazio → usa o primeiro disponível
        frame_livre = self.tabela.primeiro_frame_vazio()
        if frame_livre is not None:
            id_alterado = self.tabela.substituir_pagina(frame_livre, pagina)
            return "Page Fault", id_alterado

        # Caso 2: memória cheia → LFU escolhe a vítima
        vitima = self.tabela.escolher_vitima()
        id_alterado = self.tabela.substituir_pagina(vitima, pagina)
        return "Page Fault", id_alterado

    def imprimir_mapa_memoria(self, passo: int, pagina: int,
                               tipo_acesso: str, id_frame_alterado):
        print(f"--- Passo {passo}: Acesso à Página {pagina} ({tipo_acesso}) ---")

        for frame in self.tabela.frames:
            if frame.esta_vazio():
                conteudo = "[Vazio]"
            else:
                conteudo = f"Página {frame.pagina_alocada}"

            marcador = " <-- Alterado" if frame.id_frame == id_frame_alterado else ""
            print(f"[Frame {frame.id_frame}]: {conteudo}{marcador}")

        print("-" * 40)

    def executar(self):
        num_frames = len(self.tabela.frames)
        print(f"Iniciando simulação com {num_frames} frames disponíveis.")
        print("=" * 40)

        for passo, pagina in enumerate(self.sequencia, start=1):
            tipo_acesso, id_frame_alterado = self.acessar_pagina(pagina)
            self.imprimir_mapa_memoria(passo, pagina, tipo_acesso, id_frame_alterado)

        self.imprimir_stats()


    def imprimir_stats(self):
        taxa_faults = (self.total_page_faults / self.total_acessos) * 100
        print("=" * 16 + " STATS FINAIS " + "=" * 16)
        print(f"Total de Acessos: {self.total_acessos}")
        print(f"Total de Page Faults: {self.total_page_faults}")
        print(f"Taxa de Page Faults: {taxa_faults:.2f}%")
        print("=" * 46)


def ler_arquivo(caminho: str):

    with open(caminho, "r") as f:
        linhas = f.readlines()

    # Remove espaços, ignora vazias e comentários
    linhas = [l.strip() for l in linhas]
    linhas = [l for l in linhas if l and not l.startswith("#")]

    num_frames = int(linhas[0])
    sequencia = [int(l) for l in linhas[1:]]
    return num_frames, sequencia


if __name__ == "__main__":
    # Aceita caminho do arquivo por argumento; padrão: entrada.txt
    caminho = sys.argv[1] if len(sys.argv) > 1 else "entrada.txt"

    num_frames, sequencia = ler_arquivo(caminho)
    sim = Simulador(num_frames, sequencia)
    sim.executar()