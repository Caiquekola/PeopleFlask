# gui_app.py

import tkinter as tk
from tkinter import ttk, messagebox
import requests # Biblioteca para fazer as requisições HTTP

class UserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Usuários")
        self.root.geometry("600x600")

        self.api_url = "http://localhost:3001"
        self.current_user_id = None 

        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TEntry", font=("Helvetica", 12), padding=5)
        style.configure("TButton", font=("Helvetica", 11, "bold"))
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        style.configure("Treeview", rowheight=25, font=("Helvetica", 11))

        # --- Layout com Frames ---
        form_frame = ttk.Frame(root, padding="10")
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        list_frame = ttk.Frame(root, padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # --- Formulário para Adicionar/Editar ---
        ttk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(form_frame, width=40)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.email_entry = ttk.Entry(form_frame, width=40)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Botões do formulário
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=1, pady=10, sticky="e")
        
        self.save_button = ttk.Button(button_frame, text="Salvar", command=self.save_user)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Limpar", command=self.clear_form)
        self.clear_button.pack(side=tk.LEFT)

        # --- Lista de Usuários (usando Treeview) ---
        self.user_tree = ttk.Treeview(list_frame, columns=("ID", "Nome", "Email"), show="headings")
        self.user_tree.heading("ID", text="ID")
        self.user_tree.heading("Nome", text="Nome")
        self.user_tree.heading("Email", text="Email")

        # Configurando a largura das colunas
        self.user_tree.column("ID", width=200, anchor=tk.W)
        self.user_tree.column("Nome", width=150, anchor=tk.W)
        self.user_tree.column("Email", width=200, anchor=tk.W)
        
        self.user_tree.pack(fill=tk.BOTH, expand=True)

        # Botões de ação da lista
        list_button_frame = ttk.Frame(list_frame)
        list_button_frame.pack(fill=tk.X, pady=10)

        self.edit_button = ttk.Button(list_button_frame, text="Editar Selecionado", command=self.edit_user)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = ttk.Button(list_button_frame, text="Deletar Selecionado", command=self.delete_user)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        # Carregar os usuários ao iniciar
        self.load_users()

    def load_users(self):
        """Busca usuários da API e popula a lista (Treeview)."""
        try:
            for item in self.user_tree.get_children():
                self.user_tree.delete(item)

            response = requests.get(self.api_url)
            response.raise_for_status() # Lança um erro se a requisição falhar
            users = response.json()
            
            for user in users:
                self.user_tree.insert("", tk.END, values=(user["_id"], user["name"], user["email"]))
        
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar à API: {e}")

    def save_user(self):
        """Salva um novo usuário (POST) ou atualiza um existente (PUT)."""
        name = self.name_entry.get()
        email = self.email_entry.get()

        if not name or not email:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha nome e email.")
            return

        payload = {"name": name, "email": email}
        
        try:
            if self.current_user_id:
                # Atualizar (PUT)
                url = f"{self.api_url}/{self.current_user_id}"
                response = requests.put(url, json=payload)
            else:
                # Criar (POST)
                response = requests.post(self.api_url, json=payload)
            
            response.raise_for_status()
            
            self.clear_form()
            self.load_users()
            messagebox.showinfo("Sucesso", "Usuário salvo com sucesso!")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Falha ao salvar usuário: {e}")
            
    def edit_user(self):
        """Preenche o formulário com os dados do usuário selecionado."""
        selected_item = self.user_tree.focus()
        if not selected_item:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione um usuário para editar.")
            return
        
        user_data = self.user_tree.item(selected_item, "values")
        user_id, name, email = user_data
        
        self.current_user_id = user_id
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, email)

    def delete_user(self):
        """Deleta o usuário selecionado da lista."""
        selected_item = self.user_tree.focus()
        if not selected_item:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione um usuário para deletar.")
            return

        user_id = self.user_tree.item(selected_item, "values")[0]
        
        if messagebox.askyesno("Confirmar Deleção", "Você tem certeza que deseja deletar este usuário?"):
            try:
                url = f"{self.api_url}/{user_id}"
                response = requests.delete(url)
                response.raise_for_status()
                
                self.load_users()
                messagebox.showinfo("Sucesso", "Usuário deletado com sucesso!")

            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"Falha ao deletar usuário: {e}")

    def clear_form(self):
        """Limpa os campos do formulário e reseta o ID de edição."""
        self.current_user_id = None
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = UserApp(root)
    root.mainloop()