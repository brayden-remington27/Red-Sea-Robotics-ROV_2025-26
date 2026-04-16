import cv2
import pygame
import numpy as np
from edge_impulse_linux.image import ImageImpulseRunner

MODEL_PATH = "ROV Code/resources/crabdetection.eim"

# --- Init Edge Impulse ---
runner = ImageImpulseRunner(MODEL_PATH)
model_info = runner.init()
print("Model loaded:", model_info['project']['name'])

# --- Init Camera ---
cap = cv2.VideoCapture(0)

# --- Init Pygame ---
pygame.init()
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 24)

running = True

try:
    while running:
        # Handle exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ret, frame = cap.read()
        if not ret:
            break

        # Resize for model input
        resized = cv2.resize(frame, (model_info['model_parameters']['image_input_width'],
                                     model_info['model_parameters']['image_input_height']))

        # Run inference
        features, cropped = runner.get_features_from_image(resized)
        res = runner.classify(features)

        count_A = 0
        count_B = 0
        count_C = 0
        
        if "bounding_boxes" in res["result"]:
            for bb in res["result"]["bounding_boxes"]:
                label = bb["label"]

                if label == "rock_crab":
                    count_A += 1
                elif label == "jonah_crab":
                    count_B += 1
                elif label == "european_green_crab":
                    count_C += 1

                # Draw bounding boxes
                x = int(bb["x"] * WIDTH / resized.shape[1])
                y = int(bb["y"] * HEIGHT / resized.shape[0])
                w = int(bb["width"] * WIDTH / resized.shape[1])
                h = int(bb["height"] * HEIGHT / resized.shape[0])

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(frame, label, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

        # Convert to pygame surface
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = np.rot90(frame_rgb)
        surface = pygame.surfarray.make_surface(frame_rgb)

        screen.blit(surface, (0, 0))

        # Draw counts
        text_A = font.render(f"A: {count_A}", True, (255, 0, 0))
        text_B = font.render(f"B: {count_B}", True, (0, 255, 0))
        text_C = font.render(f"B: {count_C}", True, (0, 0, 255))

        screen.blit(text_A, (10, 10))
        screen.blit(text_B, (10, 40))
        screen.blit(text_C, (10, 70))

        pygame.display.flip()

finally:
    cap.release()
    runner.stop()
    pygame.quit()