#-*- coding:utf-8 -*-
import pyautogui

class AutoGui():
    
    def screensize():
        return pyautogui.size()

    def position():
        return pyautogui.position()

    def moveto(x,y,duration=0.1):
        pyautogui.moveTo(x,y,duration=0.1)

    def click():
        pyautogui.click()
    
    def clickxy(x,y):
        pyautogui.click(x,y)
    
    def doubleclick():
        pyautogui.doubleClick()

    def rightclick():
        pyautogui.rightClick()
    
    def dragto(x,y,duration=0.5):
        pyautogui.dragTo(x,y,duration)

    def mousedown():
        pyautogui.mouseDown()

    def mouseup():
        pyautogui.mouseUp()
    
    def typein(*args):
        print(args)
        pyautogui.typewrite(args)
    
    def keydown(key):
        pyautogui.keyDown(key)

    def keyup(key):
        pyautogui.keyUp(key)

    def press(key):
        pyautogui.press(key)

    def hotkey(*args):
        pyautogui.hotkey(args) 

    def screenshot(picname):
        return pyautogui.screenshot(picname)

    def alert(text='',title='',button='OK'):
        return pyautogui.alert(text,title,button)

    def confirm(text='',title='',buttons=['OK','Cancel']):
        return pyautogui.confirm(text,title,buttons)

    def prompt(text='',title='',default=''):
        return pyautogui.prompt(text,title,default)

    
