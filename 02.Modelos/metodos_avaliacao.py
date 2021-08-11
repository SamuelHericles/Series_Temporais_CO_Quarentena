
"""
    Este arquivo serve apenas de uma classe que contém as funções de avaliação 
"""

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
import numpy as np
import warnings
import math
warnings.filterwarnings('ignore')

class metodos_de_avaliacao:

    """
                                         Erro quadrático médio
                                    EQM = (1/n)*sum(V_est - V_obs)²
            n     - Número de amostras;
            V_est - Valor estimado;
            V_obs - Valor observado.
            
            
            param serie           - pandas.DataFrame da base de dados com dados faltantes ou da série original
            param serie_original  - pandas.DataFrame da base de dados com dados preenchidos ou vindo de uma previsão
            
            return float do erro quadrático médio
    """        
    def MQE(self,serie,serie_original):
        return mean_squared_error(serie.fillna(0), serie_original.fillna(0))

    
    
    
    """
                                         Erro absoluto médio
                                    EAM = (1/n)*sum(|V_est - V_obs|)
            n     - Número de amostras;
            V_est - Valor estimado;
            V_obs - Valor observado.
                        
            param serie           - pandas.DataFrame da base de dados com dados faltantes ou da série original
            param serie_original  - pandas.DataFrame da base de dados com dados preenchidos ou vindo de uma previsão
            
            return float do erro absoluto médio
    """  
    def MAE(self,serie,serie_original):  
        return (np.sum(abs(serie-serie_original))/serie.shape[0]).mean()

    def VP(self,serie,serie_original):
        """
                                                Viés percentual
                                        VP = sum(V_est - V_obs)/sum(V_obs)
                V_est - valor estimados
                V_obs - valor observados
                
            param serie           - pandas.DataFrame da base de dados com dados faltantes ou da série original
            param serie_original  - pandas.DataFrame da base de dados com dados preenchidos ou vindo de uma previsão
            
            return float do viés percentual
        """    
        return (np.dot((1/serie.shape[0]),np.sum(serie-serie_original))/np.sum(serie_original)).mean()