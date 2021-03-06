import pywapi
import pygame
import os
import RPi.GPIO as GPIO
import MainMenu

os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
lcd = pygame.display.set_mode((320, 240))

#Creates Button Map
button_map = {17:(0,0,0)}

#Sets Buttons to Normally Open
GPIO.setmode(GPIO.BCM)
for k in button_map.keys():
    GPIO.setup(k, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Set Location
carbondale = pywapi.get_weather_from_weather_com('66414')
print(carbondale)

#Color Palette
GREY = (54,54,54)
WHITE = (255,255,255)

lcd.fill(GREY)
pygame.display.update()

#Create Fonts
bigFont = pygame.font.Font('Quicksand-Bold.otf', 70)
mediumFont = pygame.font.Font('Quicksand-Bold.otf', 32)
chanceFont = pygame.font.Font(None, 32)
smallFont = pygame.font.Font('Quicksand-Bold.otf', 24)

def DisplayWeather():
    while 1 == 1:
        #Draw Background
        lcd.fill(GREY)
    
        #Set Icon
        if carbondale['current_conditions']['icon'] == 24 :
            iconimg = pygame.image.load('wind.png')
        elif carbondale['current_conditions']['icon'] == 14 :
            iconimg = pygame.image.load('snow.png')
        elif int(carbondale['current_conditions']['icon']) > 24 and int(carbondale['current_conditions']['icon']) < 32 :
            iconimg = pygame.image.load('cloudy.png')
        elif int(carbondale['current_conditions']['icon']) > 31 and int(carbondale['current_conditions']['icon']) < 35 :
            iconimg = pygame.image.load('clear-day.png')
        elif int(carbondale['current_conditions']['icon']) > 35 and int(carbondale['current_conditions']['icon']) < 41 :
            iconimg = pygame.image.load('rain.png')
        else :
            iconimg = pygame.image.load('unknown.png')

        #Draw Icon
        lcd.blit(iconimg, (16,16))

        #Grab Variables
        day = carbondale['forecasts'][0]['date'][4:]
        temperature = str(int((float(carbondale['current_conditions']['temperature'])*1.8)+32))
        dayofweek = carbondale['forecasts'][0]['day_of_week']
        text = carbondale['current_conditions']['text'][:7]
        chanceprecip = carbondale['forecasts'][0]['day']['chance_precip']
        high = str(int((float(carbondale['forecasts'][0]['high'])*1.8)+32))
        low = str(int((float(carbondale['forecasts'][0]['low'])*1.8)+32))

        #Write Temperature
        fontimg = bigFont.render(temperature + "F",1,WHITE)
        lcd.blit(fontimg, (145,38))

        #Write Day
        fontimg = mediumFont.render(dayofweek + " " + day,1,WHITE)
        lcd.blit(fontimg, (135,6))

        #Write Forecast
        fontimg = smallFont.render(text,1,WHITE)
        lcd.blit(fontimg, (23,118))

        #Write Chance of Rain
        fontimg = chanceFont.render("CoR: " + chanceprecip + "%",1,WHITE)
        lcd.blit(fontimg, (15,210))

        #Write High Temp
        fontimg = smallFont.render("Hi: " + high,1,WHITE)
        lcd.blit(fontimg, (141,117))

        #Write Low Temp
        fontimg = smallFont.render("Lo: " + low,1,WHITE)
        lcd.blit(fontimg, (225,117))

        pygame.display.update()

        if GPIO.input(k) == False:
            if k == 17:
                MainMenu.MenuButtons()



