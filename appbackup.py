import tkinter as tk
import pyautogui
import time
import threading

# Lista para armazenar as posições de clique esquerdo
posicoes_esquerdo = []
posicao_direito = None  # Inicializa a variável global
executando = False  # Flag para controlar a execução
pausado = False  # Flag para pausar

def capturar_posicao_direito():
    """Captura a posição do mouse para o clique direito."""
    global posicao_direito
    time.sleep(2)  # Dá tempo para mover o mouse
    posicao_direito = pyautogui.position()
    label_direito.config(text=f"Direito: {posicao_direito}")
    print(f"Posição do clique direito capturada: {posicao_direito}")

def capturar_posicao_esquerdo():
    """Captura a posição do mouse para cliques esquerdos e adiciona à lista."""
    time.sleep(2)  # Dá tempo para mover o mouse
    posicao = pyautogui.position()
    posicoes_esquerdo.append(posicao)
    atualizar_lista()
    print(f"Posição adicionada para clique esquerdo: {posicao}")

def atualizar_lista():
    """Atualiza a interface com a lista de cliques esquerdos."""
    lista_posicoes.delete(0, tk.END)
    for i, pos in enumerate(posicoes_esquerdo, start=1):
        lista_posicoes.insert(tk.END, f"{i}: {pos}")

def executar_cliques():
    """Executa a sequência de cliques alternando entre direito e esquerdo."""
    global executando, pausado
    if not posicao_direito or not posicoes_esquerdo:
        print("Defina as posições antes de iniciar!")
        return

    executando = True
    print("Iniciando cliques automatizados...")

    while executando:
        if pausado:
            print("Automação pausada...")
            time.sleep(1)
            continue

        for posicao in posicoes_esquerdo:
            # Clique direito
            pyautogui.click(posicao_direito[0], posicao_direito[1], button='right')
            print(f"Clique direito em {posicao_direito}")
            time.sleep(1)  # Pequeno atraso

            # Clique esquerdo
            pyautogui.click(posicao[0], posicao[1], button='left')
            print(f"Clique esquerdo em {posicao}")
            time.sleep(1)  # Pequeno atraso

        print("Reiniciando sequência...")  
        time.sleep(2)  # Espera antes de reiniciar a sequência

def iniciar_thread():
    """Inicia a automação em uma thread separada."""
    thread = threading.Thread(target=executar_cliques, daemon=True)
    thread.start()

def pausar_automacao():
    """Pausa ou retoma a automação."""
    global pausado
    pausado = not pausado
    btn_pausar.config(text="Retomar" if pausado else "Pausar")

def parar_automacao():
    """Para completamente a automação."""
    global executando
    executando = False
    print("Automação interrompida.")

# Criar a interface gráfica
root = tk.Tk()
root.title("Automação de Cliques")
root.geometry("400x400")  # Aumentando o tamanho da janela

# Botões e labels
btn_direito = tk.Button(root, text="Capturar Clique Direito", command=capturar_posicao_direito)
btn_direito.pack(pady=5)
label_direito = tk.Label(root, text="Direito: Não definido")
label_direito.pack()

btn_esquerdo = tk.Button(root, text="Capturar Clique Esquerdo", command=capturar_posicao_esquerdo)
btn_esquerdo.pack(pady=5)
label_esquerdo = tk.Label(root, text="Esquerdos:")
label_esquerdo.pack()

# Lista de posições esquerdas
lista_posicoes = tk.Listbox(root, height=5)
lista_posicoes.pack()

btn_executar = tk.Button(root, text="Iniciar Cliques", command=iniciar_thread)
btn_executar.pack(pady=5)

btn_pausar = tk.Button(root, text="Pausar", command=pausar_automacao)
btn_pausar.pack(pady=5)

btn_parar = tk.Button(root, text="Parar", command=parar_automacao, fg="red")
btn_parar.pack(pady=10)

root.mainloop()