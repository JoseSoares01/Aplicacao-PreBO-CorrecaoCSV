import pandas as pd
import FreeSimpleGUI as sg
from datetime import datetime
import os

def corrigir_ficheiro(caminho_entrada, pasta_saida, formato_saida):
    df_original = pd.read_csv(caminho_entrada, sep='|', encoding='latin1')

    colunas_especificas = {
        'A': 'appid pco',
        'B': 'referencia',
        'E': 'source code',
        'G': 'data de entrada',
        'Q': 'codigo de agente',
        'AD': 'primeiro nome',
        'AF': 'apelido',
        'AG': 'nif',
        'CM': 'telefone fixo',
        'CN': 'telemóvel'
    }

    def letra_para_indice(col):
        return sum([(ord(c) - ord('A') + 1) * (26 ** i) for i, c in enumerate(reversed(col))]) - 1

    indices_validos = []
    nova_linha = []
    max_colunas = df_original.shape[1]

    for letra, titulo in colunas_especificas.items():
        idx = letra_para_indice(letra)
        if idx < max_colunas:
            indices_validos.append(idx)
            nova_linha.append((idx, titulo))

    df = df_original.iloc[:, indices_validos]

    titulos_ordenados = [titulo for _, titulo in sorted(nova_linha)]
    df.columns = titulos_ordenados

    if "referencia" in df.columns:
        df["referencia"] = df["referencia"].astype(str).apply(
            lambda x: f"0{x.lstrip('0')}" if x.strip() != '' else x
        )

    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
    extensao = 'csv' if formato_saida == 'CSV' else 'xlsx'
    nome_ficheiro = f"WZPRE_{agora}.{extensao}"
    caminho_saida = os.path.join(pasta_saida, nome_ficheiro)

    if formato_saida == 'CSV':
        df.to_csv(caminho_saida, sep=';', index=False, encoding='latin1')
    else:
        df.to_excel(caminho_saida, index=False)

    return caminho_saida

def main():
    sg.theme("DarkBlue3")

    ficheiro_input = sg.Input(size=(50, 1), key="ficheiro", expand_x=True)
    pasta_input = sg.Input(size=(50, 1), key="pasta", expand_x=True)

    botao_estilizado = {
        'pad': (8, 8),
        'border_width': 2,
        'button_color': ('white', 'green'),
        'font': ('Helvetica', 11, 'bold'),
        'size': (12, 1)
    }

    layout = [
        [sg.Text("Aplicação Pós BO", font=("Helvetica", 18, "bold"), justification='center', expand_x=True)],
        [sg.Text("Ficheiro Pre_BO:", size=(15, 1)), ficheiro_input, sg.FileBrowse(file_types=(("CSV Files", "*.csv"),))],
        [sg.Text("Guardar em:", size=(15, 1)), pasta_input, sg.FolderBrowse()],
        [sg.Text("Formato de saída:", size=(15, 1)), sg.Combo(['CSV', 'XLS'], default_value='CSV', key='formato', readonly=True)],
        [sg.Text("CSV: Para importar ao sistema  |  XLS: Para o Pre_BO", font=('Helvetica', 9), text_color='orange')],
        [
            sg.Button("Corrigir", **botao_estilizado),
            sg.Button("Limpar", button_color=('white', 'orange'), border_width=2, size=(12, 1)),
            sg.Button("Ajuda", button_color=('white', 'blue'), border_width=2, size=(10, 1)),
            sg.Button("Sair", button_color=('white', 'firebrick'), border_width=2, size=(10, 1))
        ]
    ]


    window = sg.Window("Aplicação Pré BO", layout, size=(650, 260), resizable=True, finalize=True, element_justification='center')
    window.move_to_center()

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Sair"):
            break
        elif event == "Limpar":
            window["ficheiro"].update("")
            window["pasta"].update("")
        elif event == "Corrigir":
            try:
                saida = corrigir_ficheiro(values["ficheiro"], values["pasta"], values["formato"])
                sg.popup("✅ Ficheiro corrigido com sucesso!", f"Guardado em:\n{saida}")
            except Exception as e:
                sg.popup_error("❌ Erro ao corrigir o ficheiro:", str(e))
        elif event == "Ajuda":
            sg.popup(
                "ℹ️ Sobre esta aplicação",
                "Esta aplicação permite importar um ficheiro CSV delimitado por '|', extrair colunas específicas, "
                "ajustar os dados da coluna 'referencia' e salvar um novo ficheiro formatado.\n\n"
                "➤ Passos:\n"
                "1. Selecione o ficheiro de entrada (.csv).\n"
                "2. Escolha a pasta onde o novo ficheiro será guardado.\n"
                "3. Escolha o formato de saída (CSV ou XLS).\n"
                "4. Clique em 'Corrigir'.\n\n"
                "O novo ficheiro será salvo com prefixo 'WZPRE_' e a data/hora atuais."
            )

    window.close()

if __name__ == "__main__":
    main()
