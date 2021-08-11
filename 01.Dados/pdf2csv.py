import os
import tabula

from tabula.io import read_pdf

for _, dirs, arquivo in os.walk(os.getcwd()+'\PDF'):
    if dirs != 'Nova pasta':
        for arq in arquivo:
            arq_pdf = tabula.read_pdf(os.getcwd()+'\PDF\\'+arq,pages='1')
            print(arq_pdf)
            tabula.convert_into('PDF/'+arq, arq[:-4]+'.csv',output_format='csv',pages='all')
print('Feito!')