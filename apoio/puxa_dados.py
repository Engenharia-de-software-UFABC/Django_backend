from django.core.exceptions import ObjectDoesNotExist
from app.models import Professor, Materia, RelacaoMateriaHorarioProfessor, RelacaoAlunoMateria
import pandas as pd

class PopularBanco:
    def __init__(self, caminho_turmas, caminho_salas):
        self.df_turmas = self.formata_turmas(caminho_turmas)
        self.df_salas = self.formata_salas(caminho_salas)

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

    def puxa_turmas(self, ra: int):
        turmas = self.df_turmas
        # Exibe o resultado
        minhas_matriculas = turmas[turmas['RA'] == ra]
        return minhas_matriculas

    def popular_banco(self):
        # Popula a tabela Professor
        for professor in self.df_salas['PROFESSOR'].unique():
            try:
                professor_obj = Professor.objects.get(nome=professor)
            except ObjectDoesNotExist:
                professor_obj = Professor(nome=professor)
                professor_obj.save()

        dict_campus = {'SA': 'Santo André', 'SB': 'São Bernardo do Campo'}
        # Popula a tabela Materia
        for turma in self.df_turmas['CÓDIGO TURMA'].unique():
            materia_info = self.df_turmas[self.df_turmas['CÓDIGO TURMA'] == turma].iloc[0]
            turma = turma.strip()
            try:
                materia_obj = Materia.objects.get(codigo_turma=turma)
            except ObjectDoesNotExist:
                
                materia_obj = Materia(codigo_turma=turma, turma=materia_info['TURMA'], campus=dict_campus[turma[-2:]])
                materia_obj.save()

        # Popula a tabela RelacaoMateriaHorarioProfessor
        for _, row in self.df_salas.iterrows():
            try:
                materia_obj = Materia.objects.get(codigo_turma=row['CÓDIGO TURMA'])
                professor_obj = Professor.objects.get(nome=row['PROFESSOR'])
                #Adicionar lógica que pega o campo 'TEORIA' ou 'PRÁTICA' e  transforma 
                relacao_obj = RelacaoMateriaHorarioProfessor(codigo_turma=materia_obj, id_professor=professor_obj, dia_semana=row['DIA'], horario=row['HORÁRIO'], sala=row['SALA'], tipo_semanal=row['TIPO'])
                relacao_obj.save()
            except ObjectDoesNotExist:
                pass

        # Popula a tabela RelacaoAlunoMateria
        for _, row in self.df_turmas.iterrows():
            # Cria ou pega o professor a partir do nome
            professor, created = Professor.objects.get_or_create(nome=row['PROFESSOR'])
            # Cria ou pega a materia a partir do codigo_turma
            materia, created = Materia.objects.get_or_create(codigo_turma=row['CÓDIGO TURMA'], turma=row['TURMA'],
                                                                campus=row['CAMPUS'], turno=row['TURNO'])
            # Cria o objeto de RelacaoMateriaHorarioProfessor
            RelacaoMateriaHorarioProfessor.objects.create(codigo_turma=materia, id_professor=professor,
                                                            dia_semana=row['DIA'], horario=row['HORARIO'], sala=row['SALA'],
                                                            tipo_semanal=row['TIPO'])
            # Cria o objeto de RelacaoAlunoMateria
            RelacaoAlunoMateria.objects.create(codigo_turma=materia, ra=row['RA'])



def main():
    base_path = 'apoio/arquivos/'
    turmas = base_path + 'ajuste_2023_1_deferidos_pos_ajuste .xlsx'
    salas = base_path + 'turmas_salas_docentes_2023_1.xlsx'
    puxa_dados = PopularBanco(turmas, salas)
    print(puxa_dados.df_turmas.columns)
    # variacoes_teoria = puxa_dados.df_salas['TEORIA'].unique()
    # variacoes_pratica = puxa_dados.df_salas['PRÁTICA'].unique()
    # print(variacoes_teoria)
    # print(variacoes_pratica)
    # puxa_dados.puxa_turmas()
    
if __name__ == '__main__':
    main()