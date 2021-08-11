"""
    Este arquivo são funções que fiz quando precisei simplificar um processo.
"""

from statsmodels.tsa.stattools import adfuller
import impyute.imputation as imp
import matplotlib.pyplot as plt
import pandas as pd
import metodos_imputacao as m_imputacao
mimputacao = m_imputacao.metodos_de_imputacao()

class funcoes_importantes():

    """
        Função par aplicar o Teste de Dickey-Fuller
        
        param serie_tempral - pandas.DataFrames de uma base dados
        
        retorn void
    """
    def teste_estacionariedade(self,serie_temporal):
        
        # Pega média do dia
        serie_temporal = serie_temporal.mean(axis='columns')
        
        #Realiza o teste estatístico
        print('Resultados do teste Dickey Fuller:')
        dftest = adfuller(serie_temporal.values)
        p_value = dftest[1]
        
        # Pega os valores retornados e exibir da melhor forma
        dfoutput = pd.Series(dftest[0:4], index=['Teste estatístico','p-value','#Lags Usados','Número de observações usadas'])
        for key,value in dftest[4].items():
            dfoutput['Valores críticos (%s)'%key] = value
        print(dfoutput)
        
       
    
    """
        Função para juntar os DataFrames pelo indices e a média diária
        
        param base1 - pandas.DataFrame
        param base2 - pandas.DataFrame
        param base3 - pandas.DataFrame
        param base4 - pandas.DataFrame
        param base5 - pandas.DataFrame
        
        return séries unidas dos 5 anos
    
    """
    def junta(self,base1,base2,base3,base4,base5,ids):
        
        ts_ccesar_16 = pd.DataFrame({
                                    'id': [ids[0] for i in range(base1.shape[0])],
                                    'time': base1.index,
                                    'value':base1.mean(axis='columns')})
        
        ts_ccesar_17 = pd.DataFrame({
                                    'id': [ids[1] for i in range(base2.shape[0])],
                                    'time': base2.index,
                                    'value':base2.mean(axis='columns')})
        
        ts_ccesar_18 = pd.DataFrame({
                                    'id': [ids[2] for i in range(base3.shape[0])],
                                    'time': base3.index,
                                    'value':base3.mean(axis='columns')}) 
        
        ts_ccesar_19 = pd.DataFrame({
                                    'id': [ids[3] for i in range(base4.shape[0])],
                                    'time': base4.index,
                                    'value':base4.mean(axis='columns')})
        
        ts_ccesar_20 = pd.DataFrame({
                                    'id': [ids[4] for i in range(base5.shape[0])],
                                    'time': base5.index,
                                    'value':base5.mean(axis='columns')})
        
        return pd.concat([ts_ccesar_16,ts_ccesar_17,ts_ccesar_18,ts_ccesar_19,ts_ccesar_20])


    """
        Função para potar um line plot com anotação do ano
        
        param dados - array(pandas.DataFrame) vetor de 5 anos de data frames
        
        return void        
    """
    def plot_anotate(self,dados,nome):
        
        # Usa a função aggregate para calcular variância ou média
        y = [dados[0].agg(nome).agg(nome),
             dados[1].agg(nome).agg(nome),
             dados[2].agg(nome).agg(nome),
             dados[3].agg(nome).agg(nome),
             dados[4].agg(nome).agg(nome)]
        
        # Usa z e n pata anotar o nome no gráfico
        z = [1, 2, 3, 5, 6]
        n = [2016, 2017, 2018, 2019, 2020]

        # Cria o gráfico e faz anotação do valor do ano com annotate
        fig, ax = plt.subplots()
        ax.plot(z, y)
        for i, txt in enumerate(n):
            ax.annotate(txt, (z[i], y[i]))

    """
                Função que calcula a diferença de um valor com seu sucessor e plota na forma de uma
        seta indicando se foi muito alto a diferença.
        
        param antes  - pandas.DataFrame ano de 2019
        param depois - pandas.DataFrame ano de 2020
        
        return void     
    """
    def gradiente_2019_2020(self,antes,depois):

        # Calcula a média e diária e depois calcula a diferença com .diff()
        x1    = antes.mean(axis='columns').index.values
        y1    = antes.mean(axis='columns')
        grad1 = pd.DataFrame(y1).diff().fillna(0).values*1000

        x2    = depois.mean(axis='columns').index.values
        y2    = depois.mean(axis='columns')
        grad2 = pd.DataFrame(y2).diff().fillna(0).values*1000


        # Configuro os subplots para ter dois, um sem a o eixo x e com tamanho (40,10)[horizontal]
        fig, (ax1, ax2) = plt.subplots(2,sharex=True, sharey=True, gridspec_kw={'hspace': 0},figsize=(40,10))

        # Gráfico do ano de 2019
        ax1.plot(antes.mean(axis='columns'),'*-',color='red',label='2019')
        ax1.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
        ax1.quiver(x1,y1,x1,grad1[:,0],scale=10,scale_units='dots')
        
        # Gráfico do ano de 2020
        ax2.quiver(x2,y2,x2,grad2[:,0],scale=10,scale_units='dots')
        ax2.plot(depois.mean(axis='columns'),'*-',label='2020')

        # Ativar o grid(grade) para poder facilitar a comparação
        ax1.legend(loc='best')
        ax2.legend(loc='best')
        ax1.grid()
        ax2.grid()

    """
        Função calcula o gradiente mensalmente
        
        param antes  - pandas.DataFrame do ano de 2019
        param depois - pandas.DataFrame do ano de 2020
        
        return void    
    """
    def gradientes_mes(self,antes,depois):
        
        # Pega um ano anterior e sucessor e calcula a média mensal
        antes  = self.media_mes(mimputacao.divide_p_mes(antes))
        depois = self.media_mes(mimputacao.divide_p_mes(depois))
        
        # Configura os subplots para ter dois gráficos, tirar o eixo x e tamanho de (40,10)
        fig, (ax1, ax2) = plt.subplots(2,sharex=True, sharey=True, gridspec_kw={'hspace': 0},figsize=(40,10))
        
        # Configura o gráfico de 2019
        ax1.plot(antes,'*-',color='red',label='2019')
        ax1.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
        ax1.set_ylim([0,1])
        ax1.legend(loc='best')
        ax1.grid()
                
        # Configura o gráfico de 2020
        ax2.plot(depois,'*-',label='2020')        
        ax2.set_ylim([0,1])
        ax2.legend(loc='best')
        ax2.grid()
        
        plt.show()


    """
       Função que calcula a média mensal de uma base de dados
       
       param bases - array(pandas.DataFrame) vetor de 5 data frames 
                     referente a 7 meses de 5 anos de medidas de uma estação
                     
       return pandas.DataFrame - média mensal do dataframes inseridos    
    """
    def media_mes(self,bases):
        media = []
        for df in bases:
             media.append(df.mean().mean())
        return media    
    
    """    
        Testa 5 anos de uma série de uma estação
        
        param dfs - array(pandas.DataFrame) array de 7 meses de 5 anos de medidas de uma estação
        
        return void    
    """
    def testar_series(self,dfs):
        print('*'*100)
        print('*'*50,'2016','*'*43)
        print('*'*100)
        print(self.teste_estacionariedade(dfs[0]))

        print('*'*100)
        print('*'*50,'2017','*'*43)
        print('*'*100)
        print(self.teste_estacionariedade(dfs[1]))

        print('*'*100)
        print('*'*50,'2018','*'*43)
        print('*'*100)
        print(self.teste_estacionariedade(dfs[2]))

        print('*'*100)
        print('*'*50,'2019','*'*43)
        print('*'*100)
        print(self.teste_estacionariedade(dfs[3]))

        print('*'*100)
        print('*'*50,'2020','*'*43)
        print('*'*100)
        print(self.teste_estacionariedade(dfs[4]))