import tabula
import os


for _, _, arquivo in os.walk('/Users/desconhecido/Desktop/Analise_Quaretena/01.Dados/PDF'):
    for arq in arquivo:
        arq_pdf = tabula.read_pdf('PDF/'+arq,pages='1')
        print(arq_pdf)
        tabula.convert_into('PDF/'+arq, arq[:-4]+'.csv',output_format='csv',pages='all')