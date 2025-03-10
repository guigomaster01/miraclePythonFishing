import pyautogui
import win32gui
import win32con
import time
import threading
import tkinter as tk
from tkinter import messagebox

# Variáveis globais
posicao_direito = (0, 0)
posicoes_esquerdo = []
executando = False
janela_jogo = ""  # Definida pelo usuário na interface

# Função para ativar a janela do jogo
def ativar_janela():
    global janela_jogo
    hwnd = win32gui.FindWindow(None, janela_jogo)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        return True
    else:
        messagebox.showerror("Erro", f"Janela '{janela_jogo}' não encontrada!")
        return False

# Atualiza as coordenadas do mouse em tempo real
def atualizar_coordenadas():
    x, y = pyautogui.position()
    label_coordenadas.config(text=f"Mouse: {x}, {y}")
    janela.after(100, atualizar_coordenadas)

# Captura a posição do clique direito
def capturar_direito():
    global posicao_direito
    posicao_direito = pyautogui.position()
    entry_direito_x.delete(0, tk.END)
    entry_direito_x.insert(0, posicao_direito[0])
    entry_direito_y.delete(0, tk.END)
    entry_direito_y.insert(0, posicao_direito[1])

# Captura a posição do clique esquerdo e adiciona à lista
def capturar_esquerdo():
    posicao = pyautogui.position()
    adicionar_posicao_esquerdo(posicao[0], posicao[1])

# Adiciona manualmente coordenadas à lista de cliques esquerdos
def adicionar_posicao_esquerdo(x, y):
    global posicoes_esquerdo
    if x.isdigit() and y.isdigit():  # Verifica se os valores são números
        posicoes_esquerdo.append((int(x), int(y)))
        atualizar_label_esquerdo()
    else:
        messagebox.showerror("Erro", "Digite coordenadas válidas antes de adicionar!")


# Atualiza a exibição das posições esquerda
def atualizar_label_esquerdo():
    texto = "\n".join([f"{i + 1}: {pos}" for i, pos in enumerate(posicoes_esquerdo)])
    label_esquerdo.config(text=f"Posições Esquerdo:\n{texto}")

# Definir a janela do jogo
def definir_janela():
    global janela_jogo
    janela_jogo = entry_janela.get()
    messagebox.showinfo("Janela Definida", f"Janela do jogo definida como: {janela_jogo}")

# Executa a automação alternando entre posicao_direito e posicoes_esquerdo
def executar_automatizacao():
    global executando, posicao_direito, posicoes_esquerdo

    if not ativar_janela():
        return

    executando = True
    i = 0
    while executando and i < len(posicoes_esquerdo):
        if not ativar_janela():
            break

        # Pega coordenadas digitadas manualmente
        direito_x = int(entry_direito_x.get())
        direito_y = int(entry_direito_y.get())

        # Clique com botão direito
        pyautogui.click(direito_x, direito_y, button='right')
        time.sleep(0.5)

        # Pega a posição esquerda da lista
        posicao = posicoes_esquerdo[i]
        pyautogui.click(posicao[0], posicao[1], button='left')
        time.sleep(0.5)

        i += 1

    executando = False

# Iniciar a automação em uma thread separada
def iniciar():
    global executando
    if not executando:
        threading.Thread(target=executar_automatizacao, daemon=True).start()

# Parar a automação
def parar():
    global executando
    executando = False

# Criar janela
janela = tk.Tk()
janela.title("Automação de Cliques")
janela.geometry("450x550")

# Entrada para definir a janela do jogo
frame_janela = tk.Frame(janela)
frame_janela.pack(pady=5)
tk.Label(frame_janela, text="Nome da Janela do Jogo:").pack(side="left")
entry_janela = tk.Entry(frame_janela, width=20)
entry_janela.pack(side="left")
btn_definir_janela = tk.Button(frame_janela, text="Definir", command=definir_janela)
btn_definir_janela.pack(side="left")

# Monitor de coordenadas
label_coordenadas = tk.Label(janela, text="Mouse: 0, 0", font=("Arial", 12))
label_coordenadas.pack(pady=10)
atualizar_coordenadas()

# Entrada para posição do clique direito
frame_direito = tk.Frame(janela)
frame_direito.pack(pady=5)
tk.Label(frame_direito, text="Posição Direito:").pack(side="left")
entry_direito_x = tk.Entry(frame_direito, width=5)
entry_direito_x.pack(side="left")
entry_direito_y = tk.Entry(frame_direito, width=5)
entry_direito_y.pack(side="left")
btn_direito = tk.Button(frame_direito, text="Capturar", command=capturar_direito)
btn_direito.pack(side="left")

# Entrada para posição do clique esquerdo
frame_esquerdo = tk.Frame(janela)
frame_esquerdo.pack(pady=5)
tk.Label(frame_esquerdo, text="Adicionar Esquerdo (X, Y):").pack(side="left")
entry_esquerdo_x = tk.Entry(frame_esquerdo, width=5)
entry_esquerdo_x.pack(side="left")
entry_esquerdo_y = tk.Entry(frame_esquerdo, width=5)
entry_esquerdo_y.pack(side="left")
btn_add_esquerdo = tk.Button(frame_esquerdo, text="Adicionar", 
                              command=lambda: adicionar_posicao_esquerdo(entry_esquerdo_x.get(), entry_esquerdo_y.get()))
btn_add_esquerdo.pack(side="left")

# Exibição das posições de clique esquerdo
label_esquerdo = tk.Label(janela, text="Posições Esquerdo:\nNenhuma", font=("Arial", 10))
label_esquerdo.pack(pady=10)

# Botões de controle
btn_iniciar = tk.Button(janela, text="Iniciar Automação", command=iniciar, bg="green", fg="white")
btn_iniciar.pack(pady=10)

btn_parar = tk.Button(janela, text="Parar Automação", command=parar, bg="red", fg="white")
btn_parar.pack(pady=10)

# Iniciar janela
janela.mainloop()