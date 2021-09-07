"""
    Este arquivo é muito importante pois conta os métodos para preenchimento de dados e funções auxiliares para ele
"""
import math
import warnings
import statistics

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import impyute.imputation as imp

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing

import metodos_avaliacao as m_avaliacao

warnings.filterwarnings('ignore')
mavaliacao = m_avaliacao.metodos_de_avaliacao()

class metodos_de_imputacao:
    
    # Função para testar qual melhor método de imputação usando Suavização Exponencial
    def testa_melhor_metodo(self,base_completada,base_original,tipo):

        base_completada = base_completada.mean(axis='columns').fillna(0)
        base_original   = base_original.mean(axis='columns').fillna(0)
        df_diff = pd.DataFrame(columns={'MQE','MAE','VP'})

        for periodos in [10,15,20,25,30]:
            for intervalo in [150,200,250]:
                modelo_prever_completado = ExponentialSmoothing(base_completada.iloc[0:intervalo].values,
                                                                trend="multiplicative",
                                                                seasonal="multiplicative",
                                                                seasonal_periods=periodos).fit()
                modelo_previsto_completado = modelo_prever_completado.predict(start=(intervalo+1),end=299)

                modelo_prever_original = ExponentialSmoothing(base_original.iloc[0:intervalo].values,
                                                              trend=tipo,
                                                              seasonal=tipo,
                                                              seasonal_periods=periodos).fit()
                modelo_previsto_original = modelo_prever_original.predict(start=(intervalo+1),end=299)

                # Original - Completado
                df_diff = df_diff.append({
                    'MQE': mavaliacao.MQE(modelo_previsto_original,base_original.iloc[intervalo+1:])- mavaliacao.MQE(modelo_previsto_completado,base_completada.iloc[intervalo+1:]),
                    'MAE': mavaliacao.MAE(modelo_previsto_original,base_original.iloc[intervalo+1:])- mavaliacao.MAE(modelo_previsto_completado,base_completada.iloc[intervalo+1:]),
                    'VP' : mavaliacao.VP( modelo_previsto_original,base_original.iloc[intervalo+1:])- mavaliacao.VP( modelo_previsto_completado,base_completada.iloc[intervalo+1:])
                },ignore_index=True)

        return df_diff

    # Concatena 5 grupos de dfs
    def concatena(self,dfs):
        df_aux = pd.concat([dfs[0],dfs[1],dfs[2],dfs[3],dfs[4]])
        df_aux.reset_index(drop=True, inplace=True)
        return df_aux 

    # Função para pegar linhas aleatório
    def random_rows(self,dados,num_linhas):
        df_aux = dados.iloc[[np.random.choice(dados.index) for _ in range(num_linhas)],:]
        df_aux.reset_index(drop=True,inplace=True)
        return df_aux

    # Função para colocar NaN aleatoriamente
    def random_nan(self,dados,porcentagem):
        ramdom_cells = (dados.shape[0]*dados.shape[1])*porcentagem
        df_aux = dados.copy()
        for i in range(int(ramdom_cells)):
            col = np.random.choice([i for i in range(dados.shape[1])])
            row = np.random.choice([i for i in range(dados.shape[0])])
            df_aux.iloc[row,col] = np.nan
        return df_aux

    # Função para adicioncar linhas(dias) sem mediadas faltantes
    def linha_no_nan(self,base):
        df_test = pd.DataFrame(columns=[str(i) for i in range(1,25)])
        df_aux = pd.DataFrame({})
        for row in range(base.shape[0]):
            if base.iloc[row,:].isna().sum()==0 and df_test.shape[0]<60:
                df_test = df_test.append(base.iloc[row,:],ignore_index=True)
        return pd.DataFrame(data=df_test.values, columns=[str(i) for i in range(1,25)])

    # Função para verificar quantidade dados faltantes
    def porcetagem_nan(self,dados,ano):
        # Verifica a quantidade de dados faltantes
        miss_dados = dados.isna().sum().sum()/(dados.shape[0]*dados.shape[1])*100
        print(f'{ano}=>{miss_dados.round(2)}% dos dados da bases são faltantes')

    # Função que pega indices de da base que estão NaN
    def getIndex_nan(self,base):

        # Vetor para colocar os indices
        indexs_nan = []

        # Percorre cada coluna da base
        for col in range(base.shape[1]):
            rows = base.index[base.iloc[:,col].isna() == True].tolist()
            for row in rows:
                indexs_nan.append([row,col])                  
        return indexs_nan

    # Função para pegar os indices NaN dividindo os dados pelo mês
    def getIndex_nan_mes(self,base):

        # Dividir as bases por mes
        dfs = self.divide_p_mes(base)

        # Criar um vetor para armazenar os indeces por mês
        indeces_mes = []

        # Adiciona no vetor de indeces_mes
        for i in range(len(dfs)):
            indeces_mes.append(self.getIndex_nan(dfs[i]))
        return indeces_mes

    # Funçao para pegar o dado mensal
    def pega_M(self,base):

        # Vetor para pegar as médias
        M = []

        # Função para dividir o mês
        dfs = self.divide_p_mes(base)

        # Adicionar de colocar as médias
        for i in range(len(dfs)):
            M.append(dfs[i].mean().mean())
        return M

    # Função para dividir a base por meses de 30 dias
    def divide_p_mes(self,base):

        # Definir o limite superior
        sup = 0
        df = pd.DataFrame({})
        dfs = []

        # Percorrer os limites e reatribuir o Data Frame
        for i in range(int(base.shape[0]/30)):
            inf = sup+1
            sup = 30*(i+1)
            df = df.append(base.iloc[inf:sup,:])
            dfs.append(df)
            df = pd.DataFrame({})
        return dfs

    # Função para completar dados pela média da base toda
    def completa_serie_Media(self,dados):
        # Completa os dados por Média
        dados_completados = dados.fillna(dados.mean().mean())

        mqe = mavaliacao.MQE(dados_completados.mean(axis='columns'),dados.fillna(0).mean(axis='columns'))
        mae = mavaliacao.MAE(dados_completados.mean(axis='columns'),dados.fillna(0).mean(axis='columns'))
        vp  = mavaliacao.VP(dados_completados.mean(axis='columns'),dados.fillna(0).mean(axis='columns'))

        return dados_completados,mqe,mae,vp

    # Função para completar dados pela Expect Maximazation
    def completa_serie_EM(self,dados):

        # Completa os dados por Expect Maximization(EM)
        dados_filled = imp.cs.em(dados.values,loops=50)    
        d = [str(i) for i in range(1,25)]
        dados_completados = pd.DataFrame(data=dados_filled.round(0),columns=d)

        mqe =  mavaliacao.MQE(dados_completados.mean(axis='columns'),dados.fillna(0).mean(axis='columns'))
        mae =  mavaliacao.MAE(dados_completados.mean(axis='columns'),dados.fillna(0).mean(axis='columns'))
        vp  =  mavaliacao.VP(dados_completados.mean(axis='columns'),dados.mean(axis='columns'))

        return dados_completados,mqe,mae,vp

    # Função que completa série por ponderação regional
    def completa_serie_ponderacao_regional(self,dados):

        # A falha nos dados na estação metereológia de inteese é estimada da seguinte forma:
        """
            D_x = (1/n)*(sum_{i=1}^n(M_x/M_i))*D_i

            D_x - Dados mensal faltante a ser estimado para estação teste;
            D_i - Dado ocorrido na estação vizinha de ordem 'i' no mês de ocorrência da falha na estação de teste;
            M_x - Dado médio mensal da estação teste;
            M_i - Dado médio mensal da estação vizinha de ordem 'i';
            n   - Número de estações vizinhas utilizadas no cálculo.

        """
        # Dx
        Dx = self.getIndex_nan(dados[0])

        # Mx
        Mx = self.pega_M(dados[0])

        # Mi
        Mi = [self.pega_M(dados[i]) for i in range(1,len(dados))]

        # n
        n = len(dados)-1

        # Processo de completar
        aux_dados = dados[0].copy()    
        for indices in Dx:    
            a,b = indices
            ponderacao = 0
            for mes in range(12):
                Ms = [Mx[mes]/Mi[estacao][mes] for estacao in range(n)]
                Di = [0 if math.isnan(dados[i].iloc[a,b]) else dados[i].iloc[a,b] for i in range(1,n+1)]
                ponderacao += np.dot((1/n),np.sum([Ms[i]*Di[i] for i in range(len(Di))]))
            aux_dados.iloc[a,b] = ponderacao

        mqe =  mavaliacao.MQE(aux_dados.mean(axis='columns'),dados[0].fillna(0).mean(axis='columns'))
        mae =  mavaliacao.MAE(aux_dados.mean(axis='columns'),dados[0].fillna(0).mean(axis='columns'))
        vp  =  mavaliacao.VP(aux_dados.mean(axis='columns'),dados[0].fillna(0).mean(axis='columns'))  

        return aux_dados,mqe,mae,vp

    # Função que completa a série por Interpolação do inverso da distância(IID)
    def completa_serie_IID(self,dados,di):
        """
                                            Dx = sum(Di/di)/sum(1/di)

            Dx - dado mensal faltante a ser preenchido na estação teste;
            Di - dado ocorrido na estação vizinha de ordem 'i' no mês de ocorrência da falha na estação;
            di - distância entre a estação teste e a estação vizinha de ordem 'i'.

        """    

        Dx = self.getIndex_nan(dados[0])
        indeces_mes = self.getIndex_nan_mes(dados[0])
        aux_dados = dados[0].copy()
        for indeces in Dx:
            a,b = indeces
            Di = [0 if math.isnan(dados[i].iloc[a,b]) else dados[i].iloc[a,b] for i in range(1,len(dados))]
            aux_dados.iloc[a,b] = np.sum([Di[i]/di[i] for i in range(len(Di))])/np.sum([1/di[i] for i in range(len(Di))])

        mqe =  mavaliacao.MQE(aux_dados.mean(axis='columns'),dados[0].fillna(0).mean(axis='columns'))
        mae =  mavaliacao.MAE(aux_dados.mean(axis='columns'),dados[0].fillna(0).mean(axis='columns'))
        vp  =  mavaliacao.VP(aux_dados.mean(axis='columns'),dados[0].fillna(0).mean(axis='columns'))

        return aux_dados,mqe,mae,vp    
    
    def testar_series_com_media(self,df1,df2,df3,df4,df5,Tipo,metodo,raio=0):
        Completos = pd.DataFrame(columns={'VP','MAE','MQE','Tipo'})

        if raio == 0:    
            completa_1,mqe,mae,vp = metodo(df1)
            Completos = Completos.append({'VP':mqe,'MAE':mae,'MQE':vp,'Tipo':Tipo}, ignore_index=True)

            completa_2,mqe,mae,vp = metodo(df2)
            Completos = Completos.append({'VP':mqe,'MAE':mae,'MQE':vp,'Tipo':Tipo}, ignore_index=True)

            completa_3,mqe,mae,vp = metodo(df3)
            Completos = Completos.append({'VP':mqe,'MAE':mae,'MQE':vp,'Tipo':Tipo}, ignore_index=True)

            completa_4,mqe,mae,vp = metodo(df4)
            Completos = Completos.append({'VP':mqe,'MAE':mae,'MQE':vp,'Tipo':Tipo}, ignore_index=True)

            completa_5,mqe,mae,vp = metodo(df5)
            Completos = Completos.append({'VP':mqe,'MAE':mae,'MQE':vp,'Tipo':Tipo}, ignore_index=True)
            
        else:
            completa_1,mqe,mae,vp = metodo(df1,raio)
            Completos = Completos.append({'VP':mqe,'MAE':mae,'MQE':vp,'Tipo':Tipo}, ignore_index=True)

            completa_2,mqe,mae,vp = metodo(df2,raio)
            Completos = Completos.append({'VP':mqe,'MAE':mae,'MQE':vp,'Tipo':Tipo}, ignore_index=True)

            completa_3,mqe,mae,vp = metodo(df3,raio)
            Completos = Completos.append({'VP':mqe,'MAE':mae,'MQE':vp,'Tipo':Tipo}, ignore_index=True)

            completa_4,mqe,mae,vp = metodo(df4,raio)
            Completos = Completos.append({'VP':mqe,'MAE':mae,'MQE':vp,'Tipo':Tipo}, ignore_index=True)

            completa_5,mqe,mae,vp = metodo(df5,raio)
            Completos = Completos.append({'VP':mqe,'MAE':mae,'MQE':vp,'Tipo':Tipo}, ignore_index=True)        
            
        return Completos

    def verficar_melhor_metodo(self,dfs,dfs_raio,raio):

        # Verificar porcetagem de dados faltatantes
        self.porcetagem_nan(dfs[0],2016)
        self.porcetagem_nan(dfs[1],2017)
        self.porcetagem_nan(dfs[2],2018)
        self.porcetagem_nan(dfs[3],2019)
        self.porcetagem_nan(dfs[4],2020)

        # Tratamento de dados com a Média 
        Media = self.testar_series_com_media(dfs[0],dfs[1],dfs[2],dfs[3],dfs[4],
                                        'Média',self.completa_serie_Media)

        # Tratamento de dados com Expected Maximization
        EM = self.testar_series_com_media(dfs[0],dfs[1],dfs[2],dfs[3],dfs[4],
                                     'EM',self.completa_serie_EM)

        # Tratamento de dados com Ponderação Regional
        PR = self.testar_series_com_media(dfs_raio[0],dfs_raio[1],dfs_raio[2],
                                          dfs_raio[3],dfs_raio[4],
                                         'PR',self.completa_serie_ponderacao_regional)

        # Tratamento de dados com Interpolação do inverso da distância
        # Raio de atuação e banco de dados do Cerqueira Cesar
        IID = self.testar_series_com_media(dfs_raio[0],dfs_raio[1],dfs_raio[2],
                                           dfs_raio[3],dfs_raio[4],
                                     'IID',self.completa_serie_IID,raio)

        resultados = pd.concat([Media,EM,PR,IID])
        fig, axes = plt.subplots(1,3,sharex=True, figsize=(16,8))
        sns.boxplot(ax=axes[0],x="Tipo", y="MQE", data=resultados)
        axes[0].set_title("MQE")

        sns.boxplot(ax=axes[1],x="Tipo", y="VP" , data=resultados)
        axes[1].set_title("VP")

        sns.boxplot(ax=axes[2],x="Tipo", y="MAE", data=resultados)
        axes[2].set_title("MAE")