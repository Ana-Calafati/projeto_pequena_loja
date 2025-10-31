import ttkbootstrap as ttk
from tkinter import Listbox # Importado para usar messagebox e variáveis
import tkinter.messagebox as messagebox
import sqlite3



class Pequena_Loja:
    def __init__(self):
        # 1. Configuração da Janela
        self.menu_principal = ttk.Window(themename="darkly")
        self.menu_principal.title("Catálogo de Inventário de Loja")
        self.menu_principal.geometry("900x1000")
        
        
        self.criar_tabela_usuario() 


        input_frame = ttk.Labelframe(self.menu_principal, text="Detalhes do Produto", padding=15)
        input_frame.pack(padx=20, pady=10)

        # Seu Frame interno para campos
        self.janela_principal = ttk.Frame(input_frame) 
        self.janela_principal.pack(pady=10)

        # Campo Produto (Nome)
        ttk.Label(self.janela_principal, text="Produto:").pack()
        self.nome_produto = ttk.Entry(self.janela_principal, width=20)
        self.nome_produto.pack()

        # Campo Descrição
        ttk.Label(self.janela_principal, text="Descrição:").pack()
        self.descricao_produto = ttk.Entry(self.janela_principal, width=20)
        self.descricao_produto.pack()

        # Campo Quantidade/Estoque
        ttk.Label(self.janela_principal, text="Quantidade:").pack()
        self.quantidade_estoque = ttk.Entry(self.janela_principal, width=20)
        self.quantidade_estoque.pack()
        
        # Campo Preço
        ttk.Label(self.janela_principal, text="Preço:").pack()
        self.preco_produto = ttk.Entry(self.janela_principal, width=20)
        self.preco_produto.pack()

        # Frame de Botões
        self.botao_frame = ttk.Frame(self.menu_principal)
        self.botao_frame.pack(pady=10)
        
        # Conectando os botões às funções
        ttk.Button(self.botao_frame, text="Adicionar Produto", width=20, command=self.adicionar_dados).pack(pady=10, padx=10, side="left")
        ttk.Button(self.botao_frame, text="Atualizar Produto", width=20, command=self.atualizar_dados_placeholder).pack(pady=10, padx=10, side="left")
        ttk.Button(self.botao_frame, text="Excluir Produto", width=20, command=self.apagar_item).pack(pady=10, padx=10, side="left")
        ttk.Button(self.botao_frame, text="Limpar Campos", width=20, command=self.limpar_campos).pack(pady=10, padx=10, side="left")

        
        # Frame para a Tabela e Barra de Rolagem (mantido o seu .pack simples)
        self.tree_frame = ttk.Frame(self.menu_principal, padding=10)
        self.tree_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Barra de Rolagem
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")
        
        # Criação do Treeview
        self.treeview = ttk.Treeview(self.tree_frame, selectmode="browse", yscrollcommand=self.scrollbar.set)
        self.treeview.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.treeview.yview)

        colunas = ("ID", "Nome", "Descrição", "Estoque", "Preço")
        self.treeview["columns"] = colunas
        self.treeview["show"] = "headings" # Esconde a coluna #0 padrão, como no seu rascunho.

        # Configuração das Colunas e Cabeçalhos
        self.treeview.column("ID", width=50, anchor=ttk.CENTER)
        self.treeview.heading("ID", text="ID")
        self.treeview.column("Nome", width=150, anchor=ttk.W)
        self.treeview.heading("Nome", text="Nome do Produto")
        self.treeview.column("Descrição", width=300, anchor=ttk.W)
        self.treeview.heading("Descrição", text="Descrição")
        self.treeview.column("Estoque", width=80, anchor=ttk.CENTER)
        self.treeview.heading("Estoque", text="Estoque")
        self.treeview.column("Preço", width=100, anchor=ttk.E)
        self.treeview.heading("Preço", text="Preço (R$)")
        
        # Estilo para o Desafio Extra (Estoque Baixo)
        self.treeview.tag_configure('estoque_baixo', background='#C88585', foreground='white')

        # Carrega os dados do banco na Treeview ao iniciar
        self.atualizar_treeview()
        # ----------------------------------------------------

    # ----------------------------------------------------------------------
    # MÉTODOS DE MANIPULAÇÃO DO BANCO DE DADOS (SQLite)
    # ----------------------------------------------------------------------

    # --- NOVO MÉTODO: Criação da Tabela ---
    def criar_tabela_usuario(self):
        """Cria a tabela de produtos se ela não existir."""
        conexao = None
        try:
            # Usando "banco_pequena_loja.sqlite" como no seu rascunho
            conexao = sqlite3.connect("banco_pequena_loja.sqlite") 
            cursor = conexao.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS DETALHES_DO_PRODUTO (
                    nome_do_produto VARCHAR(20),
                    descricao_do_produto VARCHAR(200) PRIMARY KEY,
                    quantidade_do_estoque FLOAT,
                    preco_do_produto FLOAT
                )
            """)
            
            conexao.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Erro de BD", f"Erro ao criar a tabela: {e}")
        finally:
            if conexao:
                conexao.close()

    # --- NOVO MÉTODO: Adicionar Dados (C do CRUD) ---
    def adicionar_dados(self):
        """Pega os dados do Entry e insere no banco de dados e na Treeview."""
        # Pega os valores digitados nas caixinhas
        produto = self.nome_produto.get()
        descricao = self.descricao_produto.get()
        quantidade_str = self.quantidade_estoque.get()
        preco_str = self.preco_produto.get()
        
        # Validação de campos vazios
        if not all([produto, descricao, quantidade_str, preco_str]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        # Validação e conversão de tipos
        try:
            quantidade = int(quantidade_str)
            preco = float(preco_str.replace(',', '.')) 
        except ValueError:
            messagebox.showerror("Erro de Formato", "Quantidade e Preço devem ser números válidos!")
            return

        # Insere no Banco de Dados
        conexao = None
        try:
            conexao = sqlite3.connect("banco_pequena_loja.sqlite")
            cursor = conexao.cursor()
            
            sql_insert = """
            INSERT INTO DETALHES_DO_PRODUTO (nome_do_produto, descricao_do_produto, quantidade_do_estoque, preco_do_produto)
            VALUES (?, ?, ?, ?)
            """
            
            cursor.execute(sql_insert, (produto, descricao, quantidade, preco))
            conexao.commit()
            
            messagebox.showinfo("Sucesso", f"Produto '{produto}' cadastrado com sucesso!")
            
            # Limpa os campos e atualiza a Tabela
            self.limpar_campos() 
            self.atualizar_treeview() 

        except Exception as e:
            messagebox.showerror("Erro de BD", f"Não foi possível inserir o produto. Erro: {e}")
        finally:
            if conexao:
                conexao.close()


    # --- NOVO MÉTODO: Ler Dados e Atualizar Treeview (R do CRUD) ---
    def atualizar_treeview(self):
        """Lê todos os dados do banco e recarrega a Treeview."""
        # Limpa itens existentes na tabela
        for item in self.treeview.get_children():
            self.treeview.delete(item)
            
        conexao = None
        try:
            conexao = sqlite3.connect("banco_pequena_loja.sqlite")
            cursor = conexao.cursor()
            
            # Seleciona o ID da linha (rowid) junto com os dados
            cursor.execute("SELECT rowid, * FROM DETALHES_DO_PRODUTO ORDER BY rowid DESC")
            produtos = cursor.fetchall() 
            
            conexao.close()
            
            # Insere os dados na Treeview
            for produto in produtos:
                produto_id = produto[0] # rowid
                nome = produto[1]
                descricao = produto[2]
                estoque = produto[3]
                preco = produto[4]
                
                # Lógica de Estoque Baixo (Desafio Extra)
                tags = ('estoque_baixo',) if int(estoque) < 10 else ('',)
                
                self.treeview.insert(
                    parent='', 
                    index='end', 
                    iid=produto_id, 
                    values=(produto_id, nome, descricao, estoque, f"R$ {preco:.2f}".replace('.', ',')), 
                    tags=tags 
                )

        except Exception as e:
            messagebox.showerror("Erro de BD", f"Erro ao ler os dados: {e}")
        finally:
            if conexao:
                conexao.close()

    
    # --- NOVO MÉTODO: Limpar Campos ---
    def limpar_campos(self):
        """Limpa o conteúdo de todos os campos de entrada (Entry)."""
        self.nome_produto.delete(0, 'end')
        self.descricao_produto.delete(0, 'end')
        self.quantidade_estoque.delete(0, 'end')
        self.preco_produto.delete(0, 'end')

    
    # --- AJUSTE NO MÉTODO APAGAR ITEM (sem exclusão de BD ainda) ---
    def apagar_item(self):
        """Remove o item selecionado da Treeview. A exclusão permanente será implementada a seguir."""
        item_selecionado = self.treeview.focus() 
        
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
            return

        # Pega o ID (iid) do banco de dados que está associado à linha
        produto_id = self.treeview.item(item_selecionado, 'iid')
        
        # Apenas remove da tabela (Temporário)
        self.treeview.delete(item_selecionado)
        messagebox.showinfo("Sucesso", f"Produto com ID {produto_id} excluído da tabela (Conectaremos ao BD em seguida!).")
    
    
    # --- PLACEHOLDER para o botão "Atualizar Produto" ---
    def atualizar_dados_placeholder(self):
        """Função placeholder para o botão Atualizar."""
        messagebox.showinfo("Aviso", "A função de Atualizar Produto será implementada na próxima etapa!")


    def run(self):
        self.menu_principal.mainloop()

# Inicia o programa
if __name__ == '__main__':
    loja = Pequena_Loja()
    loja.run()