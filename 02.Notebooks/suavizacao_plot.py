"""
            Este serve apenas para conter uma classe com funções de suavização expoonencial, pode média movel e
    um plot que compara os 5 anos de estação.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class suavizacao_plot:

    """
        Função que plota a comparação dos 7 meses dos 5 anos do serie original e a suavizada
        
        param serie              - pandas.DataFrame série original para calcular a média diária
        param modelo_suavizado   - pandas.DataFrame série suavizada para calcular a média diária
        
        return void 
    """
    def plot_comparacao(self,serie,modelo_suavisado):
        #Plotar valores para verficar visualmente
        plt.figure(figsize=(40,5))
        st_plot = plt.plot(serie.mean(axis='columns'),'*-', color='red',label='Original')
        st_plot = plt.plot(modelo_suavisado,'*-', color='blue',label='Suavizado')
        plt.show(block=False)

    """
        Função para calcular a suavização por média movel
        
        param serie   - pandas.DataFrame série original para ser suavizada
        param janela  - int quantidade de janelas para calcular a média movel
        
        return modelo_suavizado - pandas.DataFrame do modelo suavizado        
    """
    def suavizacao_media_movel(self,serie,janela):

        # Média movel
        modelo_suavisado = serie.rolling(window=janela).mean().dropna()

        plot_comparacao(serie,modelo_suavisado.mean(axis='columns'))

        return modelo_suavisado

    """
        Função para calcular a suavização por suavização
        
        param serie   - pandas.DataFrame série original para ser suavizada
        param janela  - int quantidade de janelas para calcular a exponencial
        
        return modelo_suavizado - pandas.DataFrame do modelo suavizado        
    """
    def suavizacao_exponencial(self,serie,alpha):

        # Suavização exponencial
        modelo_suavisado = [serie.mean(axis='columns')[0]]
        for n in range(1, len(serie)):
            modelo_suavisado.append(alpha * serie.mean(axis='columns')[n] + (1 - alpha) * modelo_suavisado[n-1])                

        plot_comparacao(serie,modelo_suavisado)

        return modelo_suavisado