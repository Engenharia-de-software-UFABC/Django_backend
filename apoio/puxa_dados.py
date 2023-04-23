from django.core.exceptions import ObjectDoesNotExist
from app.models import Professor, Materia, RelacaoMateriaHorarioProfessor, RelacaoAlunoMateria
import pandas as pd
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto.settings')
django.setup()
import apoio.interpretador_regex as ir

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
        turmas['CÓDIGO TURMA'] = turmas['CÓDIGO TURMA'].astype(str)
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
        for coluna in ['DOCENTE TEORIA', 'DOCENTE PRÁTICA', 'DOCENTE TEORIA 2', 'DOCENTE PRÁTICA 2']:
            for professor in self.df_salas[coluna].unique():
                try:
                    professor_obj = Professor.objects.get(nome=professor)
                except ObjectDoesNotExist:
                    if professor == None or professor.strip() == '' or professor == 'nan.0':
                        continue
                    professor_obj = Professor(nome=professor)
                    professor_obj.save()

        dict_campus = {'SA': 'Santo André', 'SB': 'São Bernardo do Campo'}
        # Popula a tabela Materia
        for turma in self.df_turmas['CÓDIGO TURMA'].unique():
            if len(self.df_turmas[self.df_turmas['CÓDIGO TURMA'] == turma]) > 0:
                materia_info = self.df_turmas[self.df_turmas['CÓDIGO TURMA'] == turma].iloc[0]
            else:
                print("Index out of bounds: ", turma)
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
                horarios = []
                if len(row['TEORIA'].strip()) > 2:
                    professor = row['DOCENTE TEORIA'] if row['DOCENTE TEORIA'] == None else row['DOCENTE TEORIA 2']
                    horarios += ir.dia_horario_regex(row['TEORIA'], professor)

                if len(row['PRÁTICA'].strip()) > 2:
                    professor = row['DOCENTE PRÁTICA'] if row['DOCENTE PRÁTICA'] == None else row['DOCENTE PRÁTICA 2']
                    horarios += ir.dia_horario_regex(row['PRÁTICA'], professor)

                for horario in horarios:
                    relacao_obj = RelacaoMateriaHorarioProfessor(codigo_turma=materia_obj, id_professor=horario['professor'],
                                                                 dia_semana=horario['dia_semana'], horario=horario['horario'],
                                                                 sala=horario['sala'], tipo_semanal=horario['tipo_recorrencia'])
                    relacao_obj.save()
            except ObjectDoesNotExist:
                print('Materia não encontrada')
                pass

        # Popula a tabela RelacaoAlunoMateria
        for _, row in self.df_turmas.iterrows():
            # Itera pelas linhas do dataframe pegando o codigo da turma e o RA do aluno
            try:
                materia_obj = Materia.objects.get(codigo_turma=row['CÓDIGO TURMA'])
                relacao_obj = RelacaoAlunoMateria(codigo_turma=materia_obj, ra=row['RA'])
                relacao_obj.save()
            except ObjectDoesNotExist:
                print('Erro ao inserir aluno na turma')
                pass



def main():
    base_path = 'apoio/arquivos/'
    turmas = base_path + 'ajuste_2023_1_deferidos_pos_ajuste .xlsx'
    salas = base_path + 'turmas_salas_docentes_2023_1.xlsx'
    puxa_dados = PopularBanco(turmas, salas)
    puxa_dados.popular_banco()

if __name__ == '__main__':
    main()