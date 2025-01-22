import cv2
import time
from ultralytics import YOLO

model = YOLO(r"C:\Users\lucas\Desktop\jokenpo_git\detect2\train\weights\best.pt")

cap = cv2.VideoCapture(0)

def draw_countdown(frame, countdown):
    height, width, _ = frame.shape
    cv2.putText(
        frame, f"{countdown}", (width // 2 - 50, height // 2),
        cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5
    )
    return frame

def add_red_line(frame):
    height, width, _ = frame.shape
    mid_x = width // 2
    cv2.line(frame, (mid_x, 0), (mid_x, height), (0, 0, 255), 2)
    return frame

def determine_winner(gesture1, gesture2):
    rules = {
        "pedra": {"tesoura": "ganha", "papel": "perde", "pedra": "empate"},
        "tesoura": {"papel": "ganha", "pedra": "perde", "tesoura": "empate"},
        "papel": {"pedra": "ganha", "tesoura": "perde", "papel": "empate"}
    }
    if gesture1 and gesture2:
        result = rules[gesture1][gesture2]
        if result == "ganha":
            return "Jogador 1"
        elif result == "perde":
            return "Jogador 2"
        else:
            return "Empate"
    return "Gestos não detectados"

def process_hands(frame):
    height, width, _ = frame.shape
    mid_x = width // 2
    results = model.predict(source=frame, imgsz=640, conf=0.95, iou=0.3)  
    
    player1_gesture = None
    player2_gesture = None

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  
        gesture = box.cls[0] 

        if (x1 + x2) // 2 > mid_x:
            player1_gesture = gesture
        else:
            player2_gesture = gesture

    return player1_gesture, player2_gesture, results[0].plot()

start_time = time.time()
last_result = ""  
hands_present = False  
color1 = color2 = (255, 255, 255) 

while True:
    ret, frame = cap.read()
    if not ret:
        break

    elapsed_time = time.time() - start_time
    countdown = 5 - int(elapsed_time) 

    if countdown > 0:
        
        frame = draw_countdown(frame, countdown)
        frame = add_red_line(frame)
    else:
        
        player1, player2, annotated_frame = process_hands(frame)
        frame = annotated_frame
        frame = add_red_line(frame)

        gestures = {0: "pedra", 1: "papel", 2: "tesoura"}  
        player1_gesture = gestures.get(int(player1), None) if player1 is not None else None
        player2_gesture = gestures.get(int(player2), None) if player2 is not None else None

        if player1_gesture and player2_gesture:
            last_result = determine_winner(player1_gesture, player2_gesture)
            hands_present = True
        elif not player1_gesture and not player2_gesture:
            hands_present = False 
            last_result = " "  

        if last_result == "Jogador 1":
            color1 = (0, 255, 0)  
            color2 = (0, 0, 255)  
        elif last_result == "Jogador 2":
            color1 = (0, 0, 255) 
            color2 = (0, 255, 0)  
        elif last_result == "Empate":
            color1 = (0, 255, 255)  
            color2 = (0, 255, 255)  
        else:
            color1 = color2 = (255, 255, 255)  

    height, width, _ = frame.shape
    cv2.putText(frame, "Jogador 2", (width - 300, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color2, 2)
    cv2.putText(frame, "Jogador 1", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color1, 2)

    cv2.imshow("Jokenpô", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
