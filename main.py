import pygame
import sys
import json

class Item:
    def __init__(self, text, png, basePrice, baseCpsEach):
        self.text = text
        self.png = pygame.image.load(png)
        self.png = pygame.transform.scale(self.png, (64, 64))
        self.count = 0
        self.basePrice = basePrice
        self.cpsEach = baseCpsEach

    def total_cps(self):
        return (self.cpsEach/10) * self.count

    def price(self):
        return self.basePrice * 1.15**self.count
    
    def click(self):
        price = self.price()
        global money
        if money >= price:
            self.count += 1
            money -= price

def saveGame():
    data = {
        'money': money,
        'items': [{'text': item.text, 'count': item.count} for item in items]
    }
    with open('savegame.json', 'w') as f:
        json.dump(data, f)

def loadGame():
    global money, items
    try:
        with open('savegame.json', 'r') as f:
            data = json.load(f)
            money = data['money']
            for itemData in data['items']:
                for item in items:
                    if item.text == itemData['text']:
                        item.count = itemData['count']
    except FileNotFoundError:
        pass

screenX = 720
screenY = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
blue = pygame.Color(0, 200, 200)

pygame.init()

screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption('Cookie Clicker')

fps = pygame.time.Clock()

cookieImage = pygame.image.load("cookie.png")
cookieImage = pygame.transform.scale(cookieImage, (192, 192))

cookiePos = [((screenX/2)-(192/2)), ((screenY/2)-(192/2))]

money = 0
CPS = 0.0

iItem = 0

def makeItems(textList, pngList, basePriceList, cpsList):
    items = []
    for i in range(len(textList)):
        text = textList[i]
        png = pngList[i]
        basePrice = basePriceList[i]
        baseCps = cpsList[i]
        item = Item(text, png, basePrice, baseCps)
        items.append(item)
    return items

def getCookie():
    global money
    money += 1

items = makeItems(["Half Cookie", "Vanille Cookie"], ["halfcookie.png", "vcookie.png"], [100, 1000], [0.1, 1])

def calculateCps():
    global CPS
    cps = 0.0
    for item in items:
        cps += item.total_cps()
    CPS = cps

def updateCookies():
    global money
    money += CPS

def showMoney(choice, color, font, size):
    moneyFont = pygame.font.SysFont(font, size)

    moneySurface = moneyFont.render("Money : " + str(int(money)) + " | " + "Cps: " + str(CPS*10), True, color)

    moneyRect = moneySurface.get_rect(center=(screenX/2, (screenY/2)-((screenY/2)/2)))

    screen.blit(moneySurface, moneyRect)

loadGame()

while True:
    screen.fill(blue)
    screen.blit(cookieImage, (cookiePos[0], cookiePos[1]))
    cookieRect = pygame.Rect(cookiePos[0], cookiePos[1], cookieImage.get_width(), cookieImage.get_height())

    for i, item in enumerate(items):
        screen.blit(item.png, (0, (0 + (64 * i))))

        Font = pygame.font.SysFont("time new roman", 20)
        nameSurface = Font.render("Name : " + str(item.text), True, white)
        priceSurface = Font.render("Price : " + str(int(item.basePrice*1.15**item.count)), True, white)
        countSurface = Font.render("Count : " + str(item.count), True, white)
        priceRect = priceSurface.get_rect(topleft = (70, (25 + (64 * i))))
        countRect = countSurface.get_rect(topleft = (70, (45 + (64 * i))))
        nameRect = nameSurface.get_rect(topleft = (70, (5 + (64 * i))))
        screen.blit(priceSurface, priceRect)
        screen.blit(countSurface, countRect)
        screen.blit(nameSurface, nameRect)

        itemRect = pygame.Rect(0, (0 + (64 * i)), item.png.get_width(), item.png.get_height())
        if itemRect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                item.click()
                break
            
    calculateCps()
    updateCookies()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            saveGame()
            pygame.quit()
            sys.exit()
        if(event.type == pygame.MOUSEBUTTONDOWN):
            mousePos = event.pos
            mouseButton = event.button
            if mouseButton == 1:
                if cookieRect.collidepoint(mousePos):
                    getCookie()

    showMoney(1, white, "time new roman", 20)

    pygame.display.update()
    fps.tick(30)