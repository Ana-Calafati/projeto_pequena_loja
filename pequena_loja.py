import ttkbootstrap as ttk
from tkinter import Listbox # Importar Listbox do tkinter (ttkbootstrap não tem Listbox estilizado)
import tkinter.messagebox as messagebox
import sqlite3

class Pequena_Loja:
    def __init__(self):
        # Configuração da Janela
        self.menu_principal = ttk.Window(themename="darkly") 
        self.menu_principal.title("Catálogo de Inventário de Loja")
        self.menu_principal.geometry("900x1000")
        input_frame = ttk.LabelFrame(self.menu_principal, text="Detalhes do Produto", padding=15)
        input_frame.pack(padx=20, pady=10)

        #criando com conteiner invisivel para colocar os dados
        janela_principal = ttk.Frame(self.menu_principal)
        janela_principal.pack(pady=10)

        # Campo produto
        ttk.Label(janela_principal, text="Produto:").pack()
        self.nome_produto = ttk.Entry(janela_principal, width=20)
        self.nome_produto.pack()

        # Campo descrição do produto
        ttk.Label(janela_principal, text="Descrição:").pack()
        self.descricao_produto = ttk.Entry(janela_principal, width=20)
        self.descricao_produto.pack()

        # Campo quantidade
        ttk.Label(janela_principal, text="Quantidade:").pack()
        self.quantidade_estoque = ttk.Entry(janela_principal, width=20)
        self.quantidade_estoque.pack()

        # Campo preço
        ttk.Label(janela_principal, text="Preço:").pack()
        self.preco_produto= ttk.Entry(janela_principal, width=20)
        self.preco_produto.pack()

        # --- Treeview (Tabela) ---
        self.treeview = ttk.Treeview()
        self.treeview.pack()
        self.treeview["show"] = "headings"

        self.treeview["columns"] = ("ID", "Nome", "Descrição", "Estoque", "Preço")
        # Configuração das colunas e cabeçalhos
        self.treeview.heading("ID", text="ID", anchor=ttk.CENTER)
        self.treeview.heading("Nome", text="Nome do Produto", anchor=ttk.CENTER)
        self.treeview.heading("Descrição", text="Descrição", anchor=ttk.CENTER)
        self.treeview.heading("Estoque", text="Estoque",anchor=ttk.CENTER)
        self.treeview.heading("Preço", text="Preço (R$)",anchor=ttk.CENTER)
        

        self.treeview.column("ID",width=200, anchor="center")
        self.treeview.column("Nome",width=200, anchor="center")
        self.treeview.column("Descrição",width=200, anchor="center")
        self.treeview.column("Estoque",width=200, anchor="center")
        self.treeview.column("Preço",width=200, anchor="center")

        # --- Frame de Botões ---
        botao_frame = ttk.Frame(self.menu_principal)
        botao_frame.pack(pady=10)
        ttk.Button(botao_frame, text="Adicionar Produto",width=200).pack(side="left",pady=30,padx=20)
        ttk.Button(botao_frame, text="Atualizar Produto",width=200).pack(pady=30,padx=20)
        ttk.Button(botao_frame, text="Excluir Produto",width=200).pack(pady=30,padx=20)
        ttk.Button(botao_frame, text="Limpar Campos",width=200).pack(pady=30, padx=20)
        ttk.Button(botao_frame, text="Adicione as informações",width=200,command=self.adicionar_dados).pack(pady=30, padx=20)        

    def adicionar_dados(self):
    # pega os valores digitados nas caixinhas
        produto = self.nome_produto.get()
        descricao = self.descricao_produto.get()
        quantidade = self.quantidade_estoque.get()
        preco = self.preco_produto.get()
        if not produto or not descricao or not quantidade or not preco:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return  # sai da função se algo estiver vazio

    def apagar_item(self):
        item_selecionado = self.treeview.selection()
        self.treeview.delete(item_selecionado)





    
       
    def run(self):
      self.menu_principal.mainloop()

if __name__ == "__main__":
    loja = Pequena_Loja()
    loja.menu_principal.mainloop()
