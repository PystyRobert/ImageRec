import pygame
from pyautogui import *
import pyautogui
import time
import keyboard

HEIGHT = 500
WIDTH = 800

# Title , Icon and Screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Image Recognition")
icon = pygame.image.load("target.png")
pygame.display.set_icon(icon)

# Load images
start_img = pygame.image.load("start_btn.png").convert_alpha()
exit_img = pygame.image.load("exit_btn.png").convert_alpha()
color_img = pygame.image.load("color_btn.png").convert_alpha()
image_img = pygame.image.load("image_btn.png").convert_alpha()


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.aim = False

    def draw(self):
        pos = pygame.mouse.get_pos()
        action = False

        # Check mouseover and click
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


# Specify where the buttons should be drawn
# 1st 2 values are the x and y coordinates
# 2nd takes the image loaded which should be drawn
# 3rd resize the image on screen based on percentage given ( 0.7 = 70% / 0.65 = 65% )
start_button = Button(15, 200, start_img, 0.65)
exit_button = Button(625, 200, exit_img, 0.65)
image_button = Button(215, 200, image_img, 0.65)
color_button = Button(420, 200, color_img, 0.65)

# Application loop
run = True
while run:

    # Set the color for background, can be changed with images
    screen.fill((202, 228, 241))

    # Take a screenshot and save image in the designated folder
    if start_button.draw():
        # 1st 2 values are the offset for the cursor [(0, 0) => top left of the screen]
        # 2nd 2 values are the x and y coordinates of the screen
        iml = pyautogui.screenshot(region=(0, 0, 1000, 700))
        iml.save(r"E:\Desktop\PythonProjects2022\Image recognition Python\anyimage.png")

    # Search for image on screen
    if image_button.draw():
        # 1st condition is the image saved in the folder that has to find on screen
        # 2nd condition is the grayscale if False the image has to be colored / if True the image can be black and white
        # 3rd condition is the percentage of accuracy for the image ( 0.7 = 70% / 0.65 = 65% )
        # Example of accuracy : If there is an image with 2 red balls and 1 green ball ,
        # if the percentage is low it can find an image with 2 red balls and 1 orange ball
        if pyautogui.locateOnScreen("savedimage.png", grayscale=False, confidence=0.7) is not None:
            print("I can see the image")
            time.sleep(1)
        else:
            print("I can not see the image")
            time.sleep(1)

    # Search and click on the specified color on screen
    if color_button.draw():
        time.sleep(2)
        Button.aim = True
        while Button.aim:

            # Press space to end the loop
            if keyboard.is_pressed("space"):
                Button.aim = False

            # Select the region on the screen for checking
            # 1st 2 values are the offset from where the cursor start [(0, 0) => top left of the screen]
            # 2nd 2 values are the screen coordinates (x, y)
            pic = pyautogui.screenshot(region=(680, 350, 600, 400))
            width, height = pic.size

            # Refresh and check every 5 pixels for the condition below
            for x in range(0, width, 5):
                for y in range(0, height, 5):
                    r, g, b = pic.getpixel((x, y))
                    if b == 195:
                        click(x + 680, y + 350)
                        time.sleep(0.05)
                        break

    # Exit the application
    if exit_button.draw():
        run = False

    # Check keyboard inputs and events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Button.aim = False

    pygame.display.update()

pygame.quit()
