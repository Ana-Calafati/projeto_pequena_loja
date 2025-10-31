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
        
        # --- ADIÇÃO: Variável de Controle para o Update ---
        # Armazena o ID do produto selecionado para edição
        self.id_selecionado = None 
        # --------------------------------------------------

        # Inicialização do Banco de Dados
        self.criar_tabela_usuario() 

        Input_frame = ttk.Labelframe(self.menu_principal, text="Detalhes do Produto", padding=15)
        Input_frame.pack(padx=20, pady=10)

        # Seu Frame interno para campos
        self.janela_principal = ttk.Frame(Input_frame) 
        self.janela_principal.pack(pady=10)

        # Campos de Entrada (Utilizando seus nomes de variáveis)
        
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
        
        # Conexão dos botões às funções CRUD
        ttk.Button(self.botao_frame, text="Adicionar Produto", width=20, command=self.adicionar_dados).pack(pady=10, padx=10, side="left")
        # Botão Atualizar Produto (Ligado à nova função)
        ttk.Button(self.botao_frame, text="Atualizar Produto", width=20, command=self.atualizar_dados).pack(pady=10, padx=10, side="left") 
        ttk.Button(self.botao_frame, text="Excluir Produto", width=20, command=self.apagar_item).pack(pady=10, padx=10, side="left")
        ttk.Button(self.botao_frame, text="Limpar Campos", width=20, command=self.limpar_campos).pack(pady=10, padx=10, side="left")

        # Configuração do Treeview (Tabela)
        
        # Frame para a Tabela e Barra de Rolagem
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
        self.treeview["show"] = "headings" 

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
        
        # Estilo para Estoque Baixo
        self.treeview.tag_configure('estoque_baixo', background='#C88585', foreground='white')

        # --- ADIÇÃO: Evento de Clique para Carregar Dados ---
        # Conecta o clique na linha da Treeview à função de carregamento
        self.treeview.bind('<<TreeviewSelect>>', self.carregar_campos_edicao) 
        # --------------------------------------------------

        # Carrega os dados do banco na Treeview ao iniciar
        self.atualizar_treeview()


    # ----------------------------------------------------------------------
    # MÉTODOS DE MANIPULAÇÃO DO BANCO DE DADOS (CRUD)
    # ----------------------------------------------------------------------
    
    def criar_tabela_usuario(self):
        """Cria a tabela de produtos se ela não existir."""
        conexao = None
        try:
            conexao = sqlite3.connect("banco_pequena_loja.sqlite") 
            cursor = conexao.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS DETALHES_DO_PRODUTO (
                    nome_do_produto TEXT,
                    descricao_do_produto TEXT,
                    quantidade_do_estoque INTEGER,
                    preco_do_produto REAL
                )
            """)
            conexao.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Erro de BD", f"Erro ao criar a tabela: {e}")
        finally:
            if conexao:
                conexao.close()

    # --- NOVO MÉTODO: Carrega Campos para Edição ---
    def carregar_campos_edicao(self, event):
        """Carrega os dados da linha selecionada para os campos de entrada."""
        self.limpar_campos() 
        item_selecionado = self.treeview.focus() 
        
        if item_selecionado:
            valores = self.treeview.item(item_selecionado, 'values')
            
            if valores:
                # Armazena o ID no nosso controle para o UPDATE
                self.id_selecionado = valores[0] 
                
                # Prepara o preço limpando a formatação (R$ ,)
                preco_limpo = valores[4].replace("R$ ", "").replace(",", ".")
                
                # Insere os valores nos campos (Entry)
                self.nome_produto.insert(0, valores[1])
                self.descricao_produto.insert(0, valores[2])
                self.quantidade_estoque.insert(0, valores[3])
                self.preco_produto.insert(0, preco_limpo)
        else:
             self.id_selecionado = None
    # ---------------------------------------------


    # --- FUNÇÃO ATUALIZAR DADOS (U do CRUD) ---
    def atualizar_dados(self):
        """Pega os dados dos campos e salva as alterações no produto selecionado."""
        
        if self.id_selecionado is None:
            messagebox.showwarning("Aviso", "Selecione um produto na lista para atualizar!")
            return

        # 1. Coleta e Valida os Dados
        produto = self.nome_produto.get()
        descricao = self.descricao_produto.get()
        quantidade_str = self.quantidade_estoque.get()
        preco_str = self.preco_produto.get()
        
        if not all([produto, descricao, quantidade_str, preco_str]):
            messagebox.showwarning("Aviso", "Preencha todos os campos para atualizar!")
            return

        try:
            quantidade = int(quantidade_str)
            preco = float(preco_str.replace(',', '.')) 
        except ValueError:
            messagebox.showerror("Erro de Formato", "Quantidade e Preço devem ser números válidos!")
            return

        # 2. Atualiza no Banco de Dados (UPDATE)
        conexao = None
        try:
            conexao = sqlite3.connect("banco_pequena_loja.sqlite")
            cursor = conexao.cursor()
            
            sql_update = """
            UPDATE DETALHES_DO_PRODUTO 
            SET nome_do_produto = ?, 
                descricao_do_produto = ?, 
                quantidade_do_estoque = ?, 
                preco_do_produto = ?
            WHERE rowid = ?
            """
            
            cursor.execute(sql_update, (produto, descricao, quantidade, preco, self.id_selecionado))
            conexao.commit()
            
            messagebox.showinfo("Sucesso", f"Produto ID {self.id_selecionado} atualizado com sucesso!")
            
            # 3. Limpa os campos e reseta o controle
            self.limpar_campos() 
            self.id_selecionado = None 
            self.atualizar_treeview() 

        except Exception as e:
            messagebox.showerror("Erro de BD", f"Não foi possível atualizar o produto. Erro: {e}")
        finally:
            if conexao:
                conexao.close()
    # -----------------------------------------
    
    
    # --- FUNÇÃO ADICIONAR DADOS (C do CRUD) ---
    def adicionar_dados(self):
        """Pega os dados do Entry e insere no banco de dados e na Treeview."""
        produto = self.nome_produto.get()
        descricao = self.descricao_produto.get()
        quantidade_str = self.quantidade_estoque.get()
        preco_str = self.preco_produto.get()
        
        if not all([produto, descricao, quantidade_str, preco_str]):
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            quantidade = int(quantidade_str)
            preco = float(preco_str.replace(',', '.')) 
        except ValueError:
            messagebox.showerror("Erro de Formato", "Quantidade e Preço devem ser números válidos!")
            return

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
            
            self.limpar_campos() 
            self.atualizar_treeview() 

        except Exception as e:
            messagebox.showerror("Erro de BD", f"Não foi possível inserir o produto. Erro: {e}")
        finally:
            if conexao:
                conexao.close()


    # --- FUNÇÃO APAGAR ITEM (D do CRUD) ---
    def apagar_item(self):
        """Remove o item selecionado do banco de dados e da Treeview (Exclusão Permanente)."""
        item_selecionado = self.treeview.focus() 
        
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
            return

        produto_id = self.treeview.item(item_selecionado, 'iid')
        
        conexao = None
        try:
            confirmar = messagebox.askyesno("Confirmar Exclusão", 
                                            f"Tem certeza que deseja excluir o produto ID {produto_id}?")
            
            if not confirmar:
                return 

            conexao = sqlite3.connect("banco_pequena_loja.sqlite")
            cursor = conexao.cursor()
            
            sql_delete = "DELETE FROM DETALHES_DO_PRODUTO WHERE rowid = ?"
            cursor.execute(sql_delete, (produto_id,)) 
            
            conexao.commit()
            
            self.treeview.delete(item_selecionado)
            self.limpar_campos() # Limpa os campos se o item excluído estava em edição
            
            messagebox.showinfo("Sucesso", f"Produto ID {produto_id} excluído permanentemente.")

        except Exception as e:
            messagebox.showerror("Erro de BD", f"Não foi possível excluir o produto. Erro: {e}")
        finally:
            if conexao:
                conexao.close()
    
    
    # --- FUNÇÃO ATUALIZAR TREEVIEW (R do CRUD) ---
    def atualizar_treeview(self):
        """Lê todos os dados do banco e recarrega a Treeview."""
        for item in self.treeview.get_children():
            self.treeview.delete(item)
            
        conexao = None
        try:
            conexao = sqlite3.connect("banco_pequena_loja.sqlite")
            cursor = conexao.cursor()
            cursor.execute("SELECT rowid, * FROM DETALHES_DO_PRODUTO ORDER BY rowid DESC")
            produtos = cursor.fetchall() 
            conexao.close()
            
            for produto in produtos:
                produto_id = produto[0]
                nome = produto[1]
                descricao = produto[2]
                estoque = produto[3]
                preco = produto[4]
                
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

    
    # --- FUNÇÃO LIMPAR CAMPOS ---
    def limpar_campos(self):
        """Limpa o conteúdo de todos os campos de entrada (Entry) e reseta o controle de ID."""
        self.nome_produto.delete(0, 'end')
        self.descricao_produto.delete(0, 'end')
        self.quantidade_estoque.delete(0, 'end')
        self.preco_produto.delete(0, 'end')
        
        # Reseta o ID selecionado quando os campos são limpos
        self.id_selecionado = None 


    def run(self):
        """Inicia o loop principal da interface gráfica."""
        self.menu_principal.mainloop()

# Inicia o programa
if __name__ == '__main__':
    loja = Pequena_Loja()
    loja.run()