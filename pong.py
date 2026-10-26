import cv2
import numpy as np

cap = cv2.VideoCapture(0)
LOWER_SKIN = np.array([0, 30, 60], dtype=np.uint8)     
UPPER_SKIN = np.array([20, 80, 255], dtype=np.uint8)  

ball_x, ball_y = 320, 240
ball_vx, ball_vy = 6, 5
BALL_R = 15
cooldown = 0

MAX_LIVES = 3
lives = MAX_LIVES

def reset_ball(w, h):
    
    return w // 2, h // 2, 6, int(np.random.choice([-5, 5]))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    ZONA_TANGAN = w // 2

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_SKIN, UPPER_SKIN)

    mask_zona = mask.copy()
    mask_zona[:, ZONA_TANGAN:] = 0

    
    if lives > 0:
        ball_x += ball_vx
        ball_y += ball_vy


    if ball_x - BALL_R <= 0 or ball_x + BALL_R >= w:
        ball_vx = -ball_vx
    if ball_y - BALL_R <= 0 or ball_y + BALL_R >= h:
        ball_vy = -ball_vy
    ball_x = max(BALL_R, min(w - BALL_R, ball_x))
    ball_y = max(BALL_R, min(h - BALL_R, ball_y))

    if ball_x - BALL_R <= 0:
            lives -= 1
            ball_x, ball_y, ball_vx, ball_vy = reset_ball(w, h)
    
    x1, y1 = int(ball_x) - BALL_R, int(ball_y) - BALL_R
    x2, y2 = int(ball_x) + BALL_R, int(ball_y) + BALL_R
    area = mask_zona[y1:y2, x1:x2]
    ys, xs = np.nonzero(area)  

    if cooldown == 0 and len(xs) > 30:   

        dx = ball_x - (x1 + xs.mean())
        dy = ball_y - (y1 + ys.mean())
        dist = np.hypot(dx, dy)
        speed = np.hypot(ball_vx, ball_vy)
        if dist > 0:
            ball_vx = dx / dist * speed
            ball_vy = dy / dist * speed
        else:
            ball_vx, ball_vy = -ball_vx, -ball_vy
        cooldown = 10
    if cooldown > 0:
        cooldown -= 1

    
    cv2.line(frame, (ZONA_TANGAN, 0), (ZONA_TANGAN, h), (255, 255, 0), 2)
    cv2.circle(frame, (int(ball_x), int(ball_y)), BALL_R, (0, 0, 255), -1)
    cv2.putText(frame, f"Lives: {lives}", (w - 160, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    if lives <= 0:
        cv2.putText(frame, "Game Over", (w // 2 - 120, h // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        cv2.putText(frame, "Tekan 'r' untuk restart", (w // 2 - 150, h // 2 + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.imshow("Hand Pong - Frame", frame)
    cv2.imshow("Hand Pong - Skin Mask", mask_zona)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('r'):                           
        lives = MAX_LIVES
        ball_x, ball_y, ball_vx, ball_vy = reset_ball(w, h)
cap.release()
cv2.destroyAllWindows()