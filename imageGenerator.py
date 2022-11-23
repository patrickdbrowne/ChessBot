import cv2
import numpy as np
import pyautogui as pg

screenshot = pg.screenshot()
screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
l = pg.locateOnScreen("test.png", confidence=0.8)


cv2.rectangle(
    screenshot,
    (l.left, l.top),
    (l.left+l.width, l.top+l.height),
    (0, 0, 255),
    4
)

cv2.imshow("sc", screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()