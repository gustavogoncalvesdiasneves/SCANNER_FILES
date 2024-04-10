import os
import webbrowser
from tkinter import Tk, Button, Label, filedialog, Text, Scrollbar

def count_folders_in_folder(folder):
    if not os.path.isdir(folder):
        return 0
    return sum(1 for item in os.listdir(folder) if os.path.isdir(os.path.join(folder, item)))

def count_files_in_folder(folder):
    if not os.path.isdir(folder):
        return 0
    return sum(1 for item in os.listdir(folder) if os.path.isfile(os.path.join(folder, item)))

def generate_file_explorer_html(folder):
    if not os.path.isdir(folder):
        return f'O caminho "{folder}" não é uma pasta válida.'
    
    html = '<ul>'
    html += f'<li><span class="folder" onclick="toggleFolder(this)">&#128193; {os.path.basename(folder)} ({count_folders_in_folder(folder)} pastas, {count_files_in_folder(folder)} arquivos)</span>'
    html += '<ul style="display: none;">'

    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
        if os.path.isdir(item_path):
            html += f'<li>{generate_file_explorer_html(item_path)}</li>'  # Ajuste aqui
        else:
            html += f'<li><span>&#128462; {item} (arquivo)</span></li>'

    html += '</ul></li>'
    html += '</ul>'
    return html

def explore_folder():
    folder_path = filedialog.askdirectory()
    html_content = f"""
    <html>
    <head>
        <link rel="stylesheet" href="css_explorer.css">
        <style>
            .folder:before {{
                content: "\\25B6";
                display: inline-block;
                margin-right: 5px;
            }}
            .file:before {{
                content: "\\1F4C4"; /* Ícone para arquivo */
                display: inline-block;
                margin-right: 5px;
            }}
            .folder.open:before {{
                content: "\\25BC";
            }}
        </style>
    </head>
    <body>
        {generate_file_explorer_html(folder_path)}
        <script>
            function toggleFolder(folder) {{
                var ul = folder.nextElementSibling;
                if (ul.style.display === 'none') {{
                    ul.style.display = 'block';
                    folder.classList.add('open');
                    folder.classList.add('selected');  // Adiciona a classe .selected à pasta clicada
                }} else {{
                    ul.style.display = 'none';
                    folder.classList.remove('open');
                    folder.classList.remove('selected');  // Remove a classe .selected da pasta clicada
                }}
            }}
        </script>
    </body>
    </html>
    """

    with open("file_explorer.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_content)
    
    print("Arquivo file_explorer.html gerado com sucesso.")
    log_text.insert('end', f"HTML gerado em: {os.path.abspath('file_explorer.html')}\n")

def open_in_browser():
    webbrowser.open("file_explorer.html")

root = Tk()
root.title("Explorador de Arquivos")

label = Label(root, text="Selecione a pasta:")
label.pack()

button = Button(root, text="Explorar", command=explore_folder)
button.pack()

log_label = Label(root, text="Logs:")
log_label.pack()

log_text = Text(root, height=10, width=50)
log_text.pack()

scrollbar = Scrollbar(root, command=log_text.yview)
scrollbar.pack(side='right', fill='y')

log_text.config(yscrollcommand=scrollbar.set)

open_button = Button(root, text="Abrir HTML no navegador", command=open_in_browser)
open_button.pack()

root.mainloop()
