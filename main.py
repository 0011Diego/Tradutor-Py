import requests
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import pyperclip
import threading

idiomas = {
    'Inglês': 'en',
    'Espanhol': 'es',
    'Francês': 'fr',
    'Alemão': 'de',
    'Italiano': 'it',
    'Português': 'pt',
    # Adicione mais idiomas conforme necessário
}

def traduzir_texto():
    texto = entrada_texto.get()
    idioma_origem = idiomas[opcao_idioma_origem.get()]
    idioma_destino = idiomas[opcao_idioma_destino.get()]

    def realizar_traducao():
        url = f"https://api.mymemory.translated.net/get?q={texto}&langpair={idioma_origem}|{idioma_destino}"

        resposta = requests.get(url)
        dados = resposta.json()

        if dados["responseStatus"] == 200:
            texto_traduzido = dados["responseData"]["translatedText"]
            label_resultado.config(text=f"Texto traduzido: {texto_traduzido}")
            botao_copiar.config(state="normal")
        else:
            label_resultado.config(text="Erro ao traduzir o texto")
            botao_copiar.config(state="disabled")

    thread_traducao = threading.Thread(target=realizar_traducao)
    thread_traducao.start()

def copiar_texto_traduzido():
    texto_traduzido = label_resultado.cget("text").split("Texto traduzido: ")[-1]
    pyperclip.copy(texto_traduzido)

# Configuração da janela principal
root = tk.Tk()
root.title("Aplicativo de Tradução")

# Estilo moderno para os widgets
style = ThemedStyle(root)
style.set_theme("equilux")  # Escolha de um tema (equilux) semelhante ao Discord

# Configuração de cores personalizadas
cor_primaria = '#2C2F33'  # Cor de fundo
cor_secundaria = '#7289da'  # Cor secundária
cor_texto = 'white'  # Cor do texto

root.config(bg=cor_primaria)
frame = ttk.Frame(root, padding="20", style='TFrame', width=300, height=300)
frame.grid(row=0, column=0, sticky="nsew")

style.configure('TLabel', background=cor_primaria, foreground=cor_texto)
style.configure('TButton', background=cor_secundaria, foreground=cor_texto, font=('Segoe UI', 10))
style.configure('TFrame', background=cor_primaria)
style.configure('TCombobox', fieldbackground='white')

ttk.Label(frame, text="Digite o texto e selecione os idiomas para tradução:", style='TLabel').grid(row=0, column=0, columnspan=2, pady=10)

entrada_texto = ttk.Entry(frame, width=50)
entrada_texto.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

ttk.Label(frame, text="Idioma de origem:", style='TLabel').grid(row=2, column=0, padx=5, pady=5)

opcao_idioma_origem = ttk.Combobox(frame, values=list(idiomas.keys()))
opcao_idioma_origem.grid(row=2, column=1, padx=5, pady=5)
opcao_idioma_origem.current(0)  # Define o idioma de origem padrão

ttk.Label(frame, text="Idioma de destino:", style='TLabel').grid(row=3, column=0, padx=5, pady=5)

opcao_idioma_destino = ttk.Combobox(frame, values=list(idiomas.keys()))
opcao_idioma_destino.grid(row=3, column=1, padx=5, pady=5)
opcao_idioma_destino.current(1)  # Define o idioma de destino padrão

ttk.Button(frame, text="Traduzir", command=traduzir_texto).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

label_resultado = ttk.Label(frame, text="", style='TLabel')
label_resultado.grid(row=5, column=0, columnspan=2, pady=10)

botao_copiar = ttk.Button(frame, text="Copiar", state="disabled", command=copiar_texto_traduzido)
botao_copiar.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()