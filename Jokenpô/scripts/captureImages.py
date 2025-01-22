import cv2
import os
import time

output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

symbols = ["pedra", "papel", "tesoura"]

num_images = 300
images_per_press = 5  
capture_interval = 0.2  

def countdown_timer(seconds, cap, message=""):
    """
    Mostra um timer na tela enquanto exibe a câmera ao vivo.
    """
    for i in range(seconds, 0, -1):
        ret, frame = cap.read()
        if not ret:
            print("Erro ao acessar a câmera.")
            return
        if message:
            cv2.putText(frame, message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Iniciando em {i} segundos...",
                    (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow("Captura de Imagens", frame)
        cv2.waitKey(1000)  

def capture_images_on_key_press(symbol, num_images, images_per_press, interval, cap):
    """
    Função para capturar imagens ao pressionar a tecla 'K'.
    """
    print(f"Iniciando a captura para: {symbol}")

    output_path = os.path.join(output_dir, symbol)
    os.makedirs(output_path, exist_ok=True)

    count = 0
    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao acessar a câmera.")
            break
        cv2.imshow("Captura de Imagens", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('k'):
            for _ in range(images_per_press):
                if count >= num_images:
                    break
                image_name = f"{symbol}_{count}.jpg"
                cv2.imwrite(os.path.join(output_path, image_name), frame)
                print(f"Imagem capturada: {image_name}")
                count += 1
                time.sleep(interval)

        if key == ord('q'):
            print("Captura interrompida pelo usuário.")
            break

    print(f"Captura para {symbol} concluída!\n")

cap = cv2.VideoCapture(0)

while True:
    print("\nEscolha o símbolo para capturar:")
    for i, symbol in enumerate(symbols, 1):
        print(f"{i}. {symbol}")
    print("4. Sair")

    choice = input("Digite o número da sua escolha: ")
    if choice == "4":
        print("Encerrando o programa.")
        break

    try:
        choice = int(choice)
        if 1 <= choice <= 3:
            selected_symbol = symbols[choice - 1]
            print(f"Abrindo câmera para {selected_symbol}. Posicione-se!")
            time.sleep(1)  
            countdown_timer(5, cap, "Posicione-se e prepare-se!")
            capture_images_on_key_press(selected_symbol, num_images, images_per_press, capture_interval, cap)
        else:
            print("Opção inválida. Tente novamente.")
    except ValueError:
        print("Por favor, digite um número válido.")

cap.release()
cv2.destroyAllWindows()
