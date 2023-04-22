import PyPDF2 
import pandas as pd
from io import StringIO

class PopularBanco:
    def __init__(self, caminho_turmas, caminho_salas):
        self.df_turmas = self.formata_turmas(caminho_turmas)
        self.df_salas = self.formata_salas(caminho_salas)
        print(self.df_salas)

    def formata_turmas(self, arquivo):
        turmas = pd.read_excel(arquivo)
        #definir o nome das colunas: 'RA' 'CÓDIGO TURMA' 'TURMA'
        turmas.columns = turmas.iloc[2]
        # Seleciona as linhas da 2ª em diante e as 3 primeiras colunas
        turmas = turmas.iloc[3:, 0:3]
        turmas = turmas.reset_index(drop=True)
        return turmas
    
    def formata_salas(self, arquivo):
        salas = pd.read_excel(arquivo)
        salas.columns = salas.iloc[44]
        salas = salas.iloc[45:, 0:12]
        #dropar linhas que tenham mesmo valor do cabeçalho
        salas = salas.drop(salas[salas['CURSO'] == 'CURSO'].index)
        salas = salas.reset_index(drop=True)
        return salas

    def puxa_turmas(self):
        turmas = self.df_turmas
        # Exibe o resultado
        minhas_matriculas = turmas[turmas['RA'] == 11201922142]
        return minhas_matriculas

def main():
    base_path = 'apoio/arquivos/'
    turmas = base_path + 'ajuste_2023_1_deferidos_pos_ajuste .xlsx'
    salas = base_path + 'turmas_salas_docentes_2023_1.xlsx'
    puxa_dados = PopularBanco(turmas, salas)
    # puxa_dados.puxa_turmas()
    
if __name__ == '__main__':
    main()