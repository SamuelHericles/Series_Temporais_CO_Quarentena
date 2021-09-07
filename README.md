# Arquivos do projeto

01. **Dados**: contem todos os arquivos originais e tratados para análise do projeto;
02. **Notebooks**: contém todos os notebooks das análises e tentativas que foram realizadas neste projeto. Incluindo também arquivos `.py` aos quais serviram para deixar os códigos contidos nos notebooks mais organizados;
03. **Conteudo**: arquivos que serviram como base para levantar as hipóteses de estudo. Além disso, um arquivo `.kml` onde possui a localização de todas as estações e seis respectivos raios de atuação;
04. **Imagens**: as imagens inseridas no documento do trabalho final.


Para executar o ambiente apenas execute o comando:

```
    make run
```

ele irá baixar a imagem docker do dockerhub onde possuí o ambiente com todas as bibliotecas intaladas. Além disso, se não conseguiu receber um saída como esta:

```
    Or copy and paste one of these URLs:
        http://303478ec563f:8888/?token=d8e72c1fad797d80147c4288129e2bb71a409ab4bb9236bf
     or http://127.0.0.1:8888/?token=d8e72c1fad797d80147c4288129e2bb71a409ab4bb9236bf
```

mude a porta local do comando docker para que consigua, ou seja no arquivo makefile mude:

```   
     docker run -p [8888]:8888 samuelhericles2/comportamento-quarentena-up
```
o valor 8888 que está em colchetes para outro valor de porta, assim conseguirá executar o ambiente em sua máquina local.