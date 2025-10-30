import ttkbootstrap as ttk
from tkinter import Listbox # Importar Listbox do tkinter (ttkbootstrap não tem Listbox estilizado)
import tkinter.messagebox
import sqlite3

class Pequena_Loja:
    def __init__(self):
        # 1. Configuração da Janela
        self.menu_principal = ttk.Window(themename="darkly") 
        self.menu_principal.title("Catálogo de Inventário de Loja")
        self.menu_principal.geometry("850x600")


        

    
    def adicionar_dados(self):
        id1 = self.proximo_id; self.proximo_id += 1
        self.produtos.append({'id': id1, 'nome_produto': "Lightstick Da P1harmony",
                                'descricao': "Para fãs do grupo de k-pop!", 
                                'quantidade_stock': 15, 
                                'preco_unitario': 120.50})
        self.produtos.append({'id': id2, 'nome_produto': "Photocard Oficial New Jeans", 
                              'descricao': "Estoque baixo! Atenção.", 
                              'quantidade_stock': 5, 'preco_unitario': 15.00})
    
        self.carregar_produtos()

        def criar_interface(self):
            input_frame = ttk.LabelFrame(self.root, text="Detalhes do Produto", padding=15)
            input_frame.pack(padx=20, pady=10)

        # Labels e Entradas
        campos = [
            ("Nome do Produto:", "nome"),
            ("Descrição:", "desc"),
            ("Estoque (Qtd):", "stock"),
            ("Preço Unitário:", "preco")
        ]
        
        
          
        # --- Frame de Botões ---
        botao_frame = ttk.Frame(self.menu_principal)
        botao_frame.pack(pady=10)

        ttk.Button(botao_frame, text="Adicionar Produto", command=self.adicionar_produto).pack()
        ttk.Button(botao_frame, text="Atualizar Produto", command=self.atualizar_produto_selecionado).pack()
        ttk.Button(botao_frame, text="Excluir Produto", command=self.deletar_produto_selecionado).pack()
        ttk.Button(botao_frame, text="Limpar Campos", command=self.limpar_campos).pack()

        # --- Treeview (Tabela) ---

        def apagar_item():
            item_selecionado = treeview.selection()
            treeview.delete(item_selecionado)

        janela = ttk.Window(themename="minty")

        treeview = ttk.Treeview(janela)
        colunas = ("ID", "Nome", "Descrição", "Estoque", "Preço (R$)")
        # Configuração das colunas e cabeçalhos
        self.tree.heading("ID", text="ID"); self.tree.column("ID", width=50, anchor=ttk.CENTER)
        self.tree.heading("Nome", text="Nome do Produto", width=150, anchor=ttk.CENTER)
        self.tree.heading("Descrição", text="Descrição", width=300, anchor=ttk.CENTER)
        self.tree.heading("Estoque", text="Estoque", width=80, anchor=ttk.CENTER)
        self.tree.heading("Preço (R$)", text="Preço (R$)", width=100, anchor=ttk.CENTER)
        

        treeview.column("ID",width=200, anchor="center")
        treeview.column("Nome",width=200, anchor="center")
        treeview.column("Descrição",width=200, anchor="center")
        treeview.column("Estoque",width=200, anchor="center")
        treeview.column("Preço",width=200, anchor="center")

    def run(self):
      self.menu_principal.mainloop()

if __name__ == "__main__":
    loja = Pequena_Loja()
    loja.menu_principal.mainloop()
