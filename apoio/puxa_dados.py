import PyPDF2 
import pandas as pd
from io import StringIO

class PopularBanco:
    def __init__(self, arquivo):
        self.df_turmas = self.formata_df(arquivo)

    def formata_df(self, arquivo):
        turmas = pd.read_excel(arquivo)
        #definir o nome das colunas: 'RA' 'CÓDIGO TURMA' 'TURMA'
        turmas.columns = turmas.iloc[2]
        # Seleciona as linhas da 2ª em diante e as 3 primeiras colunas
        turmas = turmas.iloc[3:, 0:3]
        turmas = turmas.reset_index(drop=True)
        return turmas
    
    def puxa_turmas(self):
        turmas = self.df_turmas
        # Exibe o resultado
        minhas_matriculas = turmas[turmas['RA'] == 11201922142]
        return minhas_matriculas

def main():
    arquivo = 'apoio/arquivos/ajuste_2023_1_deferidos_pos_ajuste .xlsx'
    puxa_dados = PopularBanco(arquivo)
    puxa_dados.puxa_turmas()
    
if __name__ == '__main__':
    main()