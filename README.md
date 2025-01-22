# Jokenpô com Visão Computacional

Este é um projeto de um jogo de **Jokenpô (Pedra, Papel e Tesoura)** utilizando a biblioteca OpenCV e um modelo de detecção de gestos treinado com YOLOv8.

## Funcionalidades

- **Detecção em tempo real**: Utiliza a webcam para capturar gestos dos jogadores.
- **Modelo YOLOv8**: Reconhece gestos de "pedra", "papel" e "tesoura".
- **Linha divisória**: Divide a tela para identificar os gestos de cada jogador.
- **Contagem regressiva**: Dá tempo para os jogadores realizarem seus gestos.
- **Decisão automática**: Determina o vencedor ou empate com base nas regras do jogo.

## Pré-requisitos

- Python 3.8 ou superior
- Dependências listadas no arquivo `requirements.txt`:
  - OpenCV
  - Ultralytics (para YOLOv8)

## Como usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/jokenpo.git
   cd jokenpo
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Certifique-se de que o modelo YOLOv8 está treinado e o arquivo de pesos (`best.pt`) está no caminho correto.

4. Execute o script:
   ```bash
   pip install opencv-python
   pip install ultralytics
   ```

5. Para encerrar o jogo, pressione a tecla `Q`.

## Arquitetura do Projeto

- **`testeScript.py`**: Script principal do jogo.
- **`weights/best.pt`**: Pesos do modelo YOLOv8s treinado para detecção de gestos.
- **`requirements.txt`**: Lista de dependências necessárias.

## Como funciona

1. A câmera é ativada e os jogadores posicionam suas mãos na área visível.
2. O programa exibe uma contagem regressiva antes de capturar os gestos.
3. O modelo YOLOv8s processa a imagem e detecta os gestos.
4. O resultado é exibido na tela, indicando o vencedor ou empate.

