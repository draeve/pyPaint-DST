
import tkinter
#import omx as omx
from pygame import *
from random import *
from math import *
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
import glob

root = Tk()  # this initializes the Tk engine
root.withdraw()  # by default the Tk root will show a little window. This just hides that window

# preSelected colours for future use
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
calmBlue = (8, 96, 168)
skyBlue = (135, 206, 250)
persianGreen = (0, 166, 147)
teal = (0, 128, 128)
dullMint = (122, 204, 143)
lightSkyBlue = (0, 191, 255)
goodBlue = (0, 0, 51)
dodgerBlue = (30, 144, 255)
paleTurquoise = (175, 238, 238)
beige = (245,245,220)
# ========================================PRE-SETTING VARIABLES
# pre-setting things
fileName = "Untitled" #preSetting filename
#--- tool related preset variables
width = 2
radiusOfCircle = 1
tool = "pencil"
toolUse = True
preHide = None # this is for blitting the complete background
startx, starty = 0, 0  # for lines, rectangles and ellipses
toolPage = 1  # for selecting tool pages

#--- stamp related preset variables
stampUse = False
stampPage = 1
stampBox = 0
stamp = None
pageVarHold = []
for i in range(18):
    pageVarHold.append(0 * i)

#--- music related preset variables 
playlist = [] #will hold music
volu = 0.5 #volume of music
paused = False #music playing
muted = False

#--- colour related preset variables
currentColour = (15, 15, 15)

#--- font related preset variables
font.init()
textContent = ""
chosenFont = None
ubuntuFont = font.Font("fonts/Ubuntu.ttf", 20)
ubuntuFontSmol = font.Font("fonts/Ubuntu.ttf", 15)
timesNewRomanFont = font.Font("fonts/TimesNewRoman.ttf", 20)
comicSansFont = font.Font("fonts/Comic.ttf", 20)

# ================================================================SCREEN INFORMATION
# screen info
init()
inf = display.Info()
w, h = inf.current_w, inf.current_h
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
screen = display.set_mode((1100, 650))

screenX = 1100
screenY = 650
# 1000, 650

display.set_caption("paint project but it's okay this time")  #name of the window at the top ^^

# ============================================================================DIMENSIONS RELATIVE TO SCREEN
# rects n dimensions n stuff

#canvas RECTS
canvasRect = Rect((screenX // 36.66), (screenY // 20), (screenX // 1.50), (screenY // 1.50))
subSurCanvas = screen.subsurface(canvasRect)
canvasX = canvasRect[0] + canvasRect[2] # X value for bottom right
canvasY = canvasRect[1] + canvasRect[3] # Y value for bottom right

#open/save RECTS
openRect = Rect((canvasRect[0]), (canvasRect[1] - 25), 50, 20) # above the canvas (loading/opening image/file)
saveRect = Rect((canvasRect[0] + 55), (canvasRect[1] - 25), 50, 20) # above the canvas (saving image/file)

#music RECTS
prevTrack = Rect( (canvasRect[2]//2 - (30*3)-(10*2) - 5), (openRect[1]), 30, 20)
playStop = Rect( (canvasRect[2]//2 - (30*2)-(10*1)) - 5, (openRect[1]), 30, 20)
nextTrack = Rect( (canvasRect[2]//2 - (30*1) - 5), (openRect[1]), 30, 20)
mute = Rect( (canvasRect[2]//2 + (30*3) + (10*2) + 5), (openRect[1]), 30, 20)
quieter = Rect( (canvasRect[2]//2 + (30*2) + (10*1) + 5), (openRect[1]), 30, 20)
louder = Rect( (canvasRect[2]//2 + (30*1) + 5), (openRect[1]), 30, 20)

#stamp RECT
stampRectOuter = Rect((canvasRect[0]), (canvasRect[1] + canvasRect[3] + 10), (canvasRect[2] - 40), (screenY - (canvasRect[1] + canvasRect[3]) - 30))
stampRect = Rect((stampRectOuter[0] + 10), (stampRectOuter[1] + 10), (stampRectOuter[2] - 20), (stampRectOuter[3] - 20))
stampPageSele1 = Rect(stampRectOuter[0] + stampRectOuter[2], stampRect[1], (canvasX - (stampRectOuter[0] + stampRectOuter[2])), ((stampRect[3] - 20) // 3) * 1)
stampPageSele2 = Rect(stampPageSele1[0], stampRect[1] + stampPageSele1[3] + 10, (canvasX - (stampRectOuter[0] + stampRectOuter[2])), (stampRect[3] - 20) // 3)
stampPageSele3 = Rect(stampPageSele1[0], stampRect[1] + (stampPageSele1[3] * 2) + 20, (canvasX - (stampRectOuter[0] + stampRectOuter[2])), (stampRect[3] - 20) // 3)


#tool RECTS
undoRect = Rect((canvasRect[0]) + canvasRect[2] - 105, (canvasRect[1] - 25), 50, 20)
redoRect = Rect((canvasRect[0]) + canvasRect[2] - 50, (canvasRect[1] - 25), 50, 20)
toolPageUp = Rect((canvasX + 20 + (50 * 0)), (canvasRect[1] + (10 * 3) + (50 * 3)), (50 * 3 + 10 * 1) // 2, 20)
toolPageDown = Rect((canvasX + 20 + (50 * 3 + 10 * 2) // 2 + 5), (canvasRect[1] + (10 * 3) + (50 * 3)), (50 * 3 + 10 * 1) // 2, 20)

selectTools = {
    "empty": 1234,

    # since everything is relative to screenX and screen Y (dimensions), there will be an increase of:
    # 10 pixels in between each 50x50 selection box (horizontally is reflected in the (x,0,0,0)
    # increase of 50 per 'column' to offset the previous selection box (x,0,0,0)
    # 10 pixels in between each 50x50 selection box (vertically is reflected in that (0,x,0,0)
    # there is no increase in the size of the 50x50 selection box dimensions

    "A1": Rect((canvasX + 20 + (50 * 0)), (canvasRect[1] + (10 * 0) + (50 * 0)), 50, 50), # index 1
    "A2": Rect((canvasX + 30 + (50 * 1)), (canvasRect[1] + (10 * 0) + (50 * 0)), 50, 50), # index 2
    "A3": Rect((canvasX + 40 + (50 * 2)), (canvasRect[1] + (10 * 0) + (50 * 0)), 50, 50), # index 3
    "B1": Rect((canvasX + 20 + (50 * 0)), (canvasRect[1] + (10 * 1) + (50 * 1)), 50, 50), # index 4
    "B2": Rect((canvasX + 30 + (50 * 1)), (canvasRect[1] + (10 * 1) + (50 * 1)), 50, 50), # index 5
    "B3": Rect((canvasX + 40 + (50 * 2)), (canvasRect[1] + (10 * 1) + (50 * 1)), 50, 50), # index 6
    "C1": Rect((canvasX + 20 + (50 * 0)), (canvasRect[1] + (10 * 2) + (50 * 2)), 50, 50), # index 7
    "C2": Rect((canvasX + 30 + (50 * 1)), (canvasRect[1] + (10 * 2) + (50 * 2)), 50, 50), # index 8
    "C3": Rect((canvasX + 40 + (50 * 2)), (canvasRect[1] + (10 * 2) + (50 * 2)), 50, 50), # index 9

    #widthChooser - drags for width
    "widthChooser": Rect((canvasX + 50 + (50 * 3)), (canvasRect[1]), 50, (screenY // 3.25)),
    "widthChooserTiny": Rect((canvasX + 50 + (50 * 3)), (canvasRect[1] + ((screenY // 2.5 - screenY // 2.5) // 2)), 50, (screenY // 3.25)),

    #colourWhell
    "currentColourRect": Rect((canvasX + 20 + (50 * 0)), (canvasRect[1] + (screenY // 1.77 - 160)), 230, 20),
    "colourWheelRect": Rect((canvasX + 20 + (50 * 0)), (canvasRect[1] + (screenY // 1.77 - 135)), 230, 200),

    "hideDraw": Rect( (canvasX + 50 * 5 + 10), (canvasRect[1]), (screenX - (canvasX + 50 * 5) - 20), 30),
    "backgroundRect": Rect( (canvasX + 50 * 5 + 10), (canvasRect[1] + 40), (screenX - (canvasX + 50 * 5) - 20), (canvasRect[3] - 40)),

    #tool help icons
    "toolHelp": Rect( ( canvasX + 20), (canvasY + 10), (screenX - canvasX - 30), (screenY - canvasY - 40)),
    "toolHelp1": Rect( ( canvasX + 30), (canvasY + 20), (screenX - canvasX - 50), (screenY - canvasY - 150)),
    "toolHelp2": Rect( ( canvasX + 30), (canvasY + 65), (screenX - canvasX - 50), (screenY - canvasY - 150)),
    "toolHelp3": Rect( ( canvasX + 30), (canvasY + 110), (screenX - canvasX - 50), (screenY - canvasY - 150)),
}

# page 1 of tools
pencilRect = selectTools["A1"]
eraserRect = selectTools["A2"]
dottedLine = selectTools["A3"]
lineThing = selectTools["B1"]
rectUnfilled = selectTools["B2"]
rectFilled = selectTools["B3"]
clearCanvas = selectTools["C1"]
ellipseUnfilled = selectTools["C2"]
ellipseFilled = selectTools["C3"]

# page 2 of tools
eyedropperTool = selectTools["A1"]
polygon = selectTools["A2"]
textTimes = selectTools["A3"]
paintBrush = selectTools["B1"]
sprayPaint = selectTools["B2"]
textComic = selectTools["B3"]
calligraphyLeft = selectTools["C1"]
calligraphyRight = selectTools["C2"]
textUbuntu = selectTools["C3"]

# easily accessible lists of page1 and page2 for STAMPS
toolPage1 = [pencilRect, eraserRect, dottedLine, lineThing, rectUnfilled, rectFilled, clearCanvas, ellipseUnfilled, ellipseFilled]
toolPage2 = [eyedropperTool, polygon, textTimes, paintBrush, sprayPaint, textComic, calligraphyLeft, calligraphyRight, textUbuntu]

#-----------------------------------------------------------------------------------------------------------------------------------------------------A SAFE SPOT FOR UNDO/REDO THINGS I GUESS
blank = screen.subsurface(canvasRect).copy()
undoList = [] #holds prev actions
redoList = [] #undo actions held in here UNLESS the user draws on the canvas again
# ---------------------------------------------------------------------------------------------------------------------------------------------------- TOOL PAGES

stampRectX = stampRect[2] // 6  #width of stamp icons
stampRectY = stampRect[3]       #height of stamp icons

selectStamps = {
    "empty": 1234,

    #rectangles in a row
    "A1": Rect((stampRect[0] + (stampRectX) * 0), (stampRect[1]), stampRectX, stampRectY),  # index 1
    "A2": Rect((stampRect[0] + (stampRectX) * 1), (stampRect[1]), stampRectX, stampRectY),  # index 2
    "A3": Rect((stampRect[0] + (stampRectX) * 2), (stampRect[1]), stampRectX, stampRectY),  # index 3
    "A4": Rect((stampRect[0] + (stampRectX) * 3), (stampRect[1]), stampRectX, stampRectY),  # index 4
    "A5": Rect((stampRect[0] + (stampRectX) * 4), (stampRect[1]), stampRectX, stampRectY),  # index 5
    "A6": Rect((stampRect[0] + (stampRectX) * 5), (stampRect[1]), stampRectX, stampRectY),  # index 6
}

# page 1
wilson = selectStamps["A1"]
maxwell = selectStamps["A2"]
webber = selectStamps["A3"]
wendy = selectStamps["A4"]
wickerbottom = selectStamps["A5"]
wx78 = selectStamps["A6"]

# page 2
wes = selectStamps["A1"]
willow = selectStamps["A2"]
winona = selectStamps["A3"]
wolfgang = selectStamps["A4"]
woodie = selectStamps["A5"]
beefalo = selectStamps["A6"]

# page 3
deerclops = selectStamps["A1"]
krampus = selectStamps["A2"]
pig = selectStamps["A3"]
shadowCreature = selectStamps["A4"]
spider = selectStamps["A5"]
tallbird = selectStamps["A6"]

#easily accessible lists for each page
stampPage1 = [wilson, maxwell, webber, wendy, wickerbottom, wx78]
stampPage2 = [wes, willow, winona, wolfgang, woodie, beefalo]
stampPage3 = [deerclops, krampus, pig, shadowCreature, spider, tallbird]
# ============================================================================================LOADING IMAGES ONTO SCREEN
# LOADING PICTURES

backgrounds = [] #list of backgrounds pulled from the folder
for back in glob.glob("backgrounds/*.*"):
    back = transform.scale(image.load(back), (screenX, screenY))
    backgrounds.append(back)

background = choice(backgrounds) #random background
currentBack = backgrounds.index(background) #holds the index of the current background for future selection
screen.blit(background, (0, 0)) #blits the current chosen background to the screen

#----------------------------AUDIO
for mp3 in glob.glob("audio/backM/*"):
    playlist.append(mp3) #takes the songs from the audio folder

init() #initializes music mixer
trackIn = playlist.index(choice(playlist)) #the index of the current track
mixer.music.load(playlist[trackIn]) #loads the track in
mixer.music.play() #plays the track

# ---------------------------TOOLS BEING LOADED IN
#page 1 of tools
pencil = transform.scale(image.load("tools/A1pencil.png"), (50, 50))
eraser = transform.scale(image.load("tools/A2eraser.png"), (50, 50))
bucket = transform.scale(image.load("tools/A3bucket.jpg"), (50, 50))
dottedL = transform.scale(image.load("tools/A3dotted.png"), (50,50))
linePic = transform.scale(image.load("tools/B1lineThing.png"), (50,50))
rectangleUnfilled = transform.scale(image.load("tools/B2unfilledRect.png"), (50,50))
rectangleFilled = transform.scale(image.load("tools/B3filledRect.png"), (50, 50))
clearCanvasPic = transform.scale(image.load("tools/C1clearCanvas.png"), (50, 50))
unfilledEll = transform.scale(image.load("tools/C2unfilledEllipse.png"), (50,50))
filledEll = transform.scale(image.load("tools/C3filledEllipse.png"), (50, 50))
#page 2 of tools
eyedropper = transform.scale(image.load("tools/D1eyedropper.png"), (50, 50))
polygonPic = transform.scale(image.load("tools/D2polygon.png"), (50,50))
timesNewPic = transform.scale(image.load("tools/D3times.png"), (50,50))
paintBrushPic = transform.scale(image.load("tools/E1PAINTB.png"), (50,50))
sprayPic = transform.scale(image.load("tools/E2spray.png"), (50,50))
comicPic = transform.scale(image.load("tools/E3comic.png"), (50,50))
calliL = transform.scale(image.load("tools/F1calliL.png"), (50,50))
calliR = transform.scale(image.load("tools/F2calliR.png"), (50,50))
ubunPic = transform.scale(image.load("tools/F3ubun.png"), (50,50))
#pageUp and pageDown
toolpUp = transform.scale(image.load("tools/toolup.png"), (toolPageUp[2:]))
toolpDown = transform.scale(image.load("tools/tooldown.png"), (toolPageDown[2:]))
# -----------------------------------------------STAMPS BEING LOADED IN
stampIcons = [[], [], []]  # icons // PAGE1, PAGE2, PAGE3

stamps = [
    [],  # 0 -wilson
    [],  # 1 -maxwell
    [],  # 2 -webber
    [],  # 3 -wendy
    [],  # 4 -wickerbottom
    [],  # 5 -wx78

    [],  # 6 -wes
    [],  # 7-willow
    [],  # 8 -winona
    [],  # 9 -wolfgang
    [],  # 10 -woodie
    [],  # 11 -beefalo

    [],  # 12 -deerclops
    [],  # 13 -krampus
    [],  # 14 -pig
    [],  # 15 -shadowCreature
    [],  # 16 -spider
    []  # 17 -tallbird

]

for ic in sorted(glob.glob("stamps/icons//A*.*")):  # ICONS - PAGE 1
    ic = transform.scale(image.load(ic), (stampRectX, stampRectY))
    stampIcons[0].append(ic)

for ic in sorted(glob.glob("stamps/icons//B*.*")):  # ICONS - PAGE 2
    ic = transform.scale((image.load(ic)), (stampRectX, stampRectY))
    stampIcons[1].append(ic)

for ic in sorted(glob.glob("stamps/icons//C*.*")):  # ICONS - PAGE 3
    ic = transform.scale((image.load(ic)), (stampRectX, stampRectY))
    stampIcons[2].append(ic)

#-------------------
# PAGE 1 STARTS HERE
# stampPage1 = [wilson, maxwell, webber, wendy, wickerbottom, wx78]

for wils in glob.glob("stamps/wilson/*.png"):  # WILSON
    wils = transform.scale((image.load(wils)), (stampRectX, stampRectY))
    stamps[0].append(wils)

for maxw in glob.glob("stamps/maxwell/*.png"):  # MAXWELL
    maxw = transform.scale((image.load(maxw)), (stampRectX, stampRectY))
    stamps[1].append(maxw)

for webb in glob.glob("stamps/webber/*.png"):  # WEBBER
    webb = transform.scale((image.load(webb)), (stampRectX, stampRectY))
    stamps[2].append(webb)

for wend in glob.glob("stamps/wendy/*.png"):  # WENDY
    wend = transform.scale((image.load(wend)), (stampRectX, stampRectY))
    stamps[3].append(wend)

for wicker in glob.glob("stamps/wickerbottom/*.png"):  # WICKERBOTTOM
    wicker = transform.scale((image.load(wicker)), (stampRectX, stampRectY))
    stamps[4].append(wicker)

for wx in glob.glob("stamps/wx78/*.png"):  # WX78
    wx = transform.scale((image.load(wx)), (stampRectX, stampRectY))
    stamps[5].append(wx)

#-------------------
# PAGE 2 STARTS HERE
# stampPage2 = [wes, willow, winona, wolfgang, woodie, beefalo]

for we in glob.glob("stamps/wes/*.png"):  # WES
    we = transform.scale((image.load(we)), (stampRectX, stampRectY))
    stamps[6].append(we)

for will in glob.glob("stamps/willow/*.png"):  # WILLOW
    will = transform.scale((image.load(will)), (stampRectX, stampRectY))
    stamps[7].append(will)

for win in glob.glob("stamps/winona/*.png"):  # WINONA
    win = transform.scale((image.load(win)), (stampRectX, stampRectY))
    stamps[8].append(win)

for wolf in glob.glob("stamps/wolfgang/*.png"):  # WOLFGANG
    wolf = transform.scale((image.load(wolf)), (stampRectX, stampRectY))
    stamps[9].append(wolf)

for wood in glob.glob("stamps/woodie/*.png"):  # WOODIE
    wood = transform.scale((image.load(wood)), (stampRectX, stampRectY))
    stamps[10].append(wood)

for beef in glob.glob("stamps/mobs//be*.*"):  # BEEFALO
    beef = transform.scale((image.load(beef)), (stampRectX, stampRectY))
    stamps[11].append(beef)

#--------------
# PAGE 3 STARTS
# stampPage3 = [deerclops, krampus, pig, shadowCreature, spider, tallbird]

for deer in glob.glob("stamps/mobs//de*.*"):  # DEERCLOPS
    deer = transform.scale((image.load(deer)), (stampRectX, stampRectY))
    stamps[12].append(deer)

for kramp in glob.glob("stamps/mobs//k*.*"):  # KRAMPUS
    kramp = transform.scale((image.load(kramp)), (stampRectX, stampRectY))
    stamps[13].append(kramp)

for pi in glob.glob("stamps/mobs/pig*.*"):  # PIG
    pi = transform.scale((image.load(pi)), (stampRectX, stampRectY))
    stamps[14].append(pi)

for shadow in glob.glob("stamps/mobs//sh*.*"):  # SHADOW CREATURE
    shadow = transform.scale((image.load(shadow)), (stampRectX, stampRectY))
    stamps[15].append(shadow)

for spi in glob.glob("stamps/mobs//sp*.*"):  # SPIDERS
    spi = transform.scale((image.load(spi)), (stampRectX, stampRectY))
    stamps[16].append(spi)

for bird in glob.glob("stamps/mobs/tall*.*"):  # TALLBIRD
    bird = transform.scale((image.load(bird)), (stampRectX, stampRectY))
    stamps[17].append(bird)

#icons for selecting which page of stamps
stampp1 = transform.scale(image.load("tools/stamp1.png"), stampPageSele1[2:])
stampp2 = transform.scale(image.load("tools/stamp2.png"), stampPageSele2[2:])
stampp3 = transform.scale(image.load("tools/stamp3.png"), stampPageSele3[2:])

# ------------------------------LOADING IN OTHER MISC ITEMS

colourPalette = image.load("tools/linearColourPalette.jpg")  # colour wheel
colourPaletteResized = transform.scale(colourPalette, (230, 200))
screen.blit(colourPaletteResized, (selectTools["colourWheelRect"][:2]))

loadPic = transform.scale(image.load("tools/load.png"), (openRect[2:])) #LOAD 
savePic = transform.scale(image.load("tools/save.png"), (saveRect[2:])) #SAVE

undoPic = transform.scale(image.load("tools/undo.png"), (undoRect[2:])) #UNDO
redoPic = transform.scale(image.load("tools/redo.png"), (redoRect[2:])) #REDO

#--- music icons being loaded in
prev = transform.scale(image.load("tools/previous.png"), (prevTrack[2:]))
pause = transform.scale(image.load("tools/playPause.png"), (playStop[2:]))
nextPic = transform.scale(image.load("tools/next.png"), (nextTrack[2:]))
mutePic = transform.scale(image.load("tools/mute.png"), (mute[2:]))
quietPic = transform.scale(image.load("tools/quiet.png"), (quieter[2:]))
loudPic = transform.scale(image.load("tools/loud.png"), (louder[2:]))

#list of items above the canvas for easy access and for-loop blitting
topBar = [loadPic, savePic, undoPic, redoPic, prev, pause, nextPic, mutePic, quietPic, loudPic]
topBarLoc = [openRect, saveRect, undoRect, redoRect, prevTrack, playStop, nextTrack, mute, quieter, louder]

count = 0
for p in topBarLoc:
    draw.rect(screen, white, p, 0)
    screen.blit(topBar[count], p[:2])
    count += 1

screen.blit(toolpUp, toolPageUp[:2])    #blitting tool UP
screen.blit(toolpDown, toolPageDown[:2])#blitting tool DOWN

draw.rect(screen, white, stampPageSele1, 0) #just clearing the back - WHITE
draw.rect(screen, white, stampPageSele2, 0)
draw.rect(screen, white, stampPageSele3, 0)
screen.blit(stampp1, stampPageSele1[:2])    #blitting the image onto the rectangle area
screen.blit(stampp2, stampPageSele2[:2])
screen.blit(stampp3, stampPageSele3[:2])

#drawing the canvas in
draw.rect(screen, white, canvasRect, 0)  # filled CANVAS
draw.rect(screen, black, canvasRect, 1)  # CANVAS outline

# =================================================================================================================RUNNING
running = True
while running:
    click = False
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()
    for evt in event.get():
        if evt.type == QUIT:
            running = False
            
        if evt.type == MOUSEBUTTONUP:
            screenSc = screen.copy()
            if evt.button == 1:
                click = True
                if canvasRect.collidepoint(mx,my): #this will be used for the UNDO function
                    receipts = screen.subsurface(canvasRect).copy()
                    #receipts is the variable for the screenshots taken everyime the mouse button is realeased
                    undoList.append(receipts)
                    if len(redoList) >= 0:
                        redoList = [] #clears the redoList because it won't be applicable anymore

        #this was stolen from HenryTwo's github (with sorta permission? if high fives count I guess)
        if evt.type == USEREVENT: #If the music ends
            playlist.insert(0, playlist.pop()) #Take the last item in playlist and move to front
            mixer.music.load(playlist[-1]) #Load new muic
            mixer.music.play() #play it
        
        if click:
            #OPENING/LOADING IN PICTURES
            if openRect.collidepoint(mx, my) and mb[0] == 1:
                reFileName = tkinter.filedialog.askopenfilename(filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"),('Windows Bitmap','*.bmp')])
                if reFileName:
                    loadfile = transform.scale(image.load(reFileName), (canvasRect[2:]))
                    screen.blit(loadfile, canvasRect)
                    print(loadfile)

            #SAVING THIS PICTURES
            elif saveRect.collidepoint(mx, my) and mb[0] == 1:
                saFileName = tkinter.filedialog.asksaveasfilename(defaultextension = ".jpg")
                if saFileName:
                    image.save(subSurCanvas, saFileName)
                    print(saFileName)

            #UNDO
            if undoRect.collidepoint(mx,my):    #borrowed undo/redo for an undetermined amount of time from Rumaisa
                if len(undoList) == 0:
                    draw.rect(screen, teal, undoRect, 2)
                elif len(undoList) == 1:
                    continue
                else:
                    redoList.append(undoList[-1])
                    undoList.remove(undoList[-1])
                    screen.blit(undoList[-1], canvasRect[:2])

            #REDO
            elif redoRect.collidepoint(mx,my):
                if len(redoList) == 0:
                    draw.rect(screen, teal, redoRect, 2)
                elif len(redoList) == 1:
                    continue
                else:
                    #screen.blit(redoList[-1], canvasRect[:2])
                    undoList.append(redoList[-1])
                    redoList.remove(redoList[-1])
                    screen.blit(undoList[-1], (canvasRect[:2]))                       

        #FOR THE TEXT FUNCTIONS
        if evt.type == KEYDOWN: #if a key on the keyboard is pressed down

            if tool == "textTimes" or tool == "textComic" or tool == "textUbuntu": #making sure that 'drawing' text is true
                keyValue = evt.unicode #getting the key/letter/character
                if len(textContent) <= 100: #making sure it's less than 50 characters
                    textContent += keyValue
                    if key.get_pressed()[K_BACKSPACE]:
                        textContent = textContent[0:-2]
                screen.blit(entireScreen, (0,0))
                if tool == "textTimes":
                    chosenFont = timesNewRomanFont
                    txtPic = chosenFont.render((textContent), True, (currentColour))
                    screen.blit(txtPic,(mx-txtPic.get_width()//2, my-txtPic.get_height()//2))
                if tool == "textComic":
                    chosenFont = comicSansFont
                    txtPic = chosenFont.render((textContent), True, (currentColour))
                    screen.blit(txtPic,(mx-txtPic.get_width()//2, my-txtPic.get_height()//2))
                if tool == "textUbuntu":
                    chosenFont = ubuntuFont
                    txtPic = chosenFont.render((textContent), True, (currentColour))
                    screen.blit(txtPic,(mx-txtPic.get_width()//2, my-txtPic.get_height()//2))

        
        if evt.type == MOUSEBUTTONDOWN:
            if evt.button == 1:
                entireScreen = screen.copy()
                startx, starty = evt.pos


            # SCROLLING UP
            if evt.button == 4:

                #changing the background
                if selectTools["backgroundRect"].collidepoint(mx, my):
                    currentBack = (currentBack + 1) % len(backgrounds)
                    screen.set_clip(selectTools["backgroundRect"])
                    backgr = transform.scale(backgrounds[currentBack], (selectTools["backgroundRect"][2] * 5, selectTools["backgroundRect"][3]))
                    screen.blit(backgr, selectTools["backgroundRect"][:2])
                screen.set_clip(None)

                #flipping through variations
                if stampRect.collidepoint(mx, my):
                    stampBox = int((mx - stampRect[0]) // stampRectX)  # to figure out which 'section' it's in

                    if stampPage == 1:
                        # no need to increase stampBox regarding the index, because it's the first page
                        if len(stamps[stampBox]) == 1:
                            pageVarHold[stampBox] = 0
                        else:
                            pageVarHold[stampBox] = (pageVarHold[stampBox] + 1) % len(stamps[stampBox]) #making sure it's staying within the limits
                        stamp = stamps[stampBox][pageVarHold[stampBox]]  # the actual picture index within the stamp list

                    if stampPage == 2:
                        stampBox += 6
                        if len(stamps[stampBox]) == 1:
                            pageVarHold[stampBox] = 0
                        else:
                            pageVarHold[stampBox] = (pageVarHold[stampBox] + 1) % len(stamps[stampBox])
                            # i want this to find the index of the variation at the index of the character list INSIDE THE LIST OF CHARACTERS
                        stamp = stamps[stampBox][pageVarHold[stampBox]]

                    if stampPage == 3:
                        stampBox += 12
                        if len(stamps[stampBox]) == 1:
                            pageVarHold[stampBox] = 0
                        else:
                            pageVarHold[stampBox] = (pageVarHold[stampBox] + 1) % len(stamps[stampBox])
                        stamp = stamps[stampBox][pageVarHold[stampBox]]

            # SCROLLING DOWN
            if evt.button == 5:
               #going through backgrounds 
                if selectTools["backgroundRect"].collidepoint(mx, my):
                    currentBack = (currentBack - 1) % len(backgrounds)
                    screen.set_clip(selectTools["backgroundRect"])
                    backgr = transform.scale(backgrounds[currentBack], (selectTools["backgroundRect"][2] * 5, selectTools["backgroundRect"][3]))
                    screen.blit(backgr, selectTools["backgroundRect"][:2])
                screen.set_clip(None)

                #flipping through variations
                if stampRect.collidepoint(mx, my):
                    stampBox = int((mx - stampRect[0]) // stampRectX)  # to figure out which 'section' it's in
                    stampBoxOG = stampBox  # this includes the 0

                    if stampPage == 1:
                        if len(stamps[stampBox]) == 1:
                            pageVarHold[stampBox] = 0
                        else:
                            pageVarHold[stampBox] = (pageVarHold[stampBox] - 1) % len(stamps[stampBox])
                        stamp = stamps[stampBox][pageVarHold[stampBox]]

                    if stampPage == 2:
                        stampBox += 6
                        if len(stamps[stampBox]) == 1:
                            pageVarHold[stampBox] = 0
                        else:
                            pageVarHold[stampBox] = (pageVarHold[stampBox] - 1) % len(stamps[stampBox])
                        stamp = stamps[stampBox][pageVarHold[stampBox]]

                    if stampPage == 3:
                        stampBox += 12
                        if len(stamps[stampBox]) == 1:
                            pageVarHold[stampBox] = 0
                        else:
                            pageVarHold[stampBox] = (pageVarHold[stampBox] - 1) % len(stamps[stampBox])
                        stamp = stamps[stampBox][pageVarHold[stampBox]]

    # =================================================================================================================================DRAWING THINGS WHILE RUNNING
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()

    if toolPage == 1: #blitting in tools in PAGE 1
            screen.blit(pencil, (pencilRect[:2]))
            screen.blit(eraser, (eraserRect[:2]))
            screen.blit(dottedL, (dottedLine[:2]))
            screen.blit(linePic, (lineThing[:2]))
            screen.blit(rectangleUnfilled, (rectUnfilled[:2]))
            screen.blit(rectangleFilled, (rectFilled[:2]))
            screen.blit(clearCanvasPic, (clearCanvas[:2]))
            screen.blit(unfilledEll, (ellipseUnfilled[:2]))
            screen.blit(filledEll, (ellipseFilled[:2]))

    if toolPage == 2: #blitting tools in PAGE 2
            screen.blit(eyedropper, (eyedropperTool[:2]))
            screen.blit(polygonPic, (polygon[:2]))
            screen.blit(timesNewPic, (textTimes[:2]))
            screen.blit(paintBrushPic, (paintBrush[:2]))
            screen.blit(sprayPic, (sprayPaint[:2]))
            screen.blit(comicPic, (textComic [:2]))
            screen.blit(calliL, (calligraphyLeft[:2]))
            screen.blit(calliR, (calligraphyRight[:2]))
            screen.blit(ubunPic, (textUbuntu[:2]))

    #blitting the choices + variations
    if stampPage == 1:
        count1 = 0
        for st1 in stampPage1:
            draw.rect(screen, white, st1, 0)
            if stamp is not None:
                screen.blit(stamps[count1][pageVarHold[count1]], st1)
                count1 += 1
            else:
                screen.blit((stampIcons[0][count1]), st1)
                count1 += 1

    if stampPage == 2:
        count1 = 6
        for st2 in stampPage2:
            draw.rect(screen, white, st2, 0)
            if stamp is not None:
                screen.blit(stamps[count1][pageVarHold[count1]], st2)
                count1 += 1
            else:
                screen.blit((stampIcons[1][count1]), st2)
                count1 += 1

    if stampPage == 3:
        count1 = 12
        for st3 in stampPage3:
            draw.rect(screen, white, st3, 0)
            if stamp is not None:
                screen.blit(stamps[count1][pageVarHold[count1]], st3)
                count1 += 1
            else:
                screen.blit((stampIcons[2][count1]), st3)
                count1 += 1

    # the original background (outside of selection, behind everything)
    screen.set_clip(selectTools["backgroundRect"])
    backgr = transform.scale(backgrounds[currentBack], (selectTools["backgroundRect"][2] * 4, selectTools["backgroundRect"][3]))
    screen.blit(backgr, selectTools["backgroundRect"][:2])
    screen.set_clip(None)

#----------FILLING IN THE EMPTY RECTANGLES FOR TOOLS/STAMPS/ETC.
    draw.rect(screen, white, stampPageSele1, 2) #beside the stamps - page selection 1
    draw.rect(screen, white, stampPageSele2, 2) #beside the stamps - page selection 2
    draw.rect(screen, white, stampPageSele3, 2) #beside the stamps - page selection 3
    draw.rect(screen, black, stampPageSele1, 2) #beside the stamps - page selection 1
    draw.rect(screen, black, stampPageSele2, 2) #beside the stamps - page selection 2
    draw.rect(screen, black, stampPageSele3, 2) #beside the stamps - page selection 3
    draw.rect(screen, dullMint, canvasRect, 5)  # CANVAS outline
    draw.rect(screen, black, openRect, 2)  # LOAD/OPEN file black outline
    draw.rect(screen, black, saveRect, 2)  # SAVE file black outline
    draw.rect(screen, black, toolPageUp, 2) #tool page up (right)
    draw.rect(screen, black, toolPageDown, 2) # tool page down (left)
    draw.rect(screen, black, undoRect, 2) #undo Rect
    draw.rect(screen, black, redoRect, 2) #redo rect
    draw.rect(screen, black, selectTools["widthChooserTiny"], 3)  # internal WIDTH CHOOSER box outline
    draw.rect(screen, white, selectTools["widthChooserTiny"], 0)  # internal WIDTH CHOOSER box white filling
    draw.rect(screen, black, selectTools["widthChooser"], 3)  # actual WIDTH CHOOSER box outline
    draw.rect(screen, white, selectTools["widthChooser"], 0)  # actual WIDTH CHOOSER box outline
    draw.rect(screen, white, selectTools["hideDraw"], 3) #tool to show the actual background for extra aesthetic!!!
    draw.rect(screen, white, selectTools["backgroundRect"], 3) #to show selection of backgrounds (able to be canvas or background)
    draw.rect(screen, white, selectTools["toolHelp"], 0) #for the help thing for tools gg
    #draw.rect(screen, red, selectTools["toolHelp1"], 2) #first row for tool/stamp help
    #draw.rect(screen, green, selectTools["toolHelp2"], 2) #second row for tool/stamp help
    #draw.rect(screen, black, selectTools["toolHelp3"], 2) #third row for tool/stamp help
    draw.rect(screen, black, prevTrack, 2)
    draw.rect(screen, black, playStop, 2)
    draw.rect(screen, black, nextTrack, 2)
    draw.rect(screen, black, mute, 2)
    draw.rect(screen, black, quieter, 2)
    draw.rect(screen, black, louder, 2)

    # these variables are somewhat relative to the actual screenX and screenY dimensions, and are placed before and after the width choosers for context
    widthChooserCenterTop = (selectTools["widthChooserTiny"][0] + selectTools["widthChooserTiny"][2] // 2), ( selectTools["widthChooser"][1])
    widthChooserCenterBottom = (selectTools["widthChooserTiny"][0] + selectTools["widthChooserTiny"][2] // 2), (selectTools["widthChooser"][1] + selectTools["widthChooser"][3])
    draw.line(screen, black, widthChooserCenterTop, widthChooserCenterBottom, 1)  # line at the center of the WIDTH CHOOSER
    draw.rect(screen, currentColour, selectTools["currentColourRect"], 0)  # box that shows the CURRENT COLOUR
    screen.blit(colourPaletteResized, (selectTools["colourWheelRect"][:2]))

    screenSc = screen.copy()
    # =============================================================================================================================COLLIDE POINT SELECTIONS
    # everything below (until the next break) concern collidepoints and tool selection for:

    #OPENING OR LOADING AN IMAGE-------------------------------------------------------------------------------------
    if openRect.collidepoint(mx, my):
        draw.rect(screen, persianGreen, openRect, 2)
        draw.rect(screen, white, selectTools["toolHelp"], 0)
        screen.blit(ubuntuFont.render(("Want to bring a beaut'"), True, black), selectTools["toolHelp1"])
        screen.blit(ubuntuFont.render(("onto this canvas? Go ahead!"), True, black), selectTools["toolHelp2"])
        if mb[0] == 1:
            draw.rect(screen, teal, openRect, 2)

    #SAVING AN IMAGE-------------------------------------------------------------------------------------
    if saveRect.collidepoint(mx, my):
        draw.rect(screen, persianGreen, saveRect, 2)
        draw.rect(screen, white, selectTools["toolHelp"], 0)
        screen.blit(ubuntuFont.render(("Like your masterpiece?"), True, black), selectTools["toolHelp1"])
        screen.blit(ubuntuFont.render(("Click to save!"), True, black), selectTools["toolHelp2"])
        if mb[0] == 1:
            draw.rect(screen, teal, saveRect, 2)

    #UNDO-------------------------------------------------------------------------------------
    if undoRect.collidepoint(mx,my):
        draw.rect(screen, persianGreen, undoRect, 2)
        draw.rect(screen, white, selectTools["toolHelp"], 0)
        screen.blit(ubuntuFont.render(("Don't like what you just"), True, black), selectTools["toolHelp1"])
        screen.blit(ubuntuFont.render(("did? Click to undo!"), True, black), selectTools["toolHelp2"])
        if mb[0] == 1:
            draw.rect(screen, teal, undoRect, 2)
    #REDO-------------------------------------------------------------------------------------
    if redoRect.collidepoint(mx,my):
        draw.rect(screen, persianGreen, redoRect, 2)
        draw.rect(screen, white, selectTools["toolHelp"], 0)
        screen.blit(ubuntuFont.render(("Thought it looked better before?"), True, black), selectTools["toolHelp1"])
        screen.blit(ubuntuFont.render(("Click to redo!"), True, black), selectTools["toolHelp2"])
        if mb[0] == 1:
            draw.rect(screen, teal, redoRect, 2)

    #MUSIC RELATED COLLIDEPOINTS-------------------------------------------------------------------------------------
    if prevTrack.collidepoint(mx,my):
        draw.rect(screen, persianGreen, prevTrack, 2)
        draw.rect(screen, white, selectTools["toolHelp"], 0)
        screen.blit(ubuntuFont.render(("Was the last song better?"), True, black), selectTools["toolHelp1"])
        screen.blit(ubuntuFont.render(("Click to go back a track!"), True, black), selectTools["toolHelp2"])
        if mb[0] == 1:
            draw.rect(screen, teal, prevTrack, 2)
            playlist[trackIn] = (playlist[trackIn] - 1) %len(playlist)
            mixer.music.load(playlist[trackIn]) #Load new muic
            mixer.music.play()

    if playStop.collidepoint(mx,my):
        draw.rect(screen, persianGreen, playStop, 2)
        draw.rect(screen, white, selectTools["toolHelp"], 0)
        screen.blit(ubuntuFont.render(("Want the music to stop/start?"), True, black), selectTools["toolHelp1"])
        screen.blit(ubuntuFont.render(("Click to do so!"), True, black), selectTools["toolHelp2"])
        if mb[0] == 1:
            draw.rect(screen, teal, playStop, 2)
            if paused == False:
                mixer.music.pause()
            elif paused == True:
                mixer.music.unpause()

    if nextTrack.collidepoint(mx,my):
        draw.rect(screen, persianGreen, nextTrack, 2)
        draw.rect(screen, white, selectTools["toolHelp"], 0)
        screen.blit(ubuntuFont.render(("Don't like this song?"), True, black), selectTools["toolHelp1"])
        screen.blit(ubuntuFont.render(("Click to listen to the next one!"), True, black), selectTools["toolHelp2"])
        if mb[0] == 1:
            draw.rect(screen, teal, nextTrack, 2)
            playlist[trackIn] = (playlist[trackIn] + 1) %len(playlist)
            mixer.music.load(playlist[trackIn + 1]) #Load new muic
            mixer.music.play()

    if mute.collidepoint(mx,my):
        draw.rect(screen, persianGreen, mute, 2)
        draw.rect(screen, white, selectTools["toolHelp"], 0)
        screen.blit(ubuntuFont.render(("Want to focus with/without the music?"), True, black), selectTools["toolHelp1"])
        screen.blit(ubuntuFont.render(("Click to do so!"), True, black), selectTools["toolHelp2"])
        if mb[0] == 1:
            draw.rect(screen, teal, mute, 2)
            if muted == True:
                muted = False
                mixer.music.set_volume(0.5) #UNmuted
            if muted == False:
                muted = True
                mixer.music.set_volume(0) #muted

    if quieter.collidepoint(mx,my):
        draw.rect(screen, white, selectTools["toolHelp"], 0)
        draw.rect(screen, persianGreen, quieter, 2)
        screen.blit(ubuntuFont.render(("Want the music to be quieter?"), True, black), selectTools["toolHelp1"])
        screen.blit(ubuntuFont.render(("Click to do so!"), True, black), selectTools["toolHelp2"])
        if mb[0] == 1:
            draw.rect(screen, teal, quieter, 2)
            init()
            if volu - 0.1 != 0:
                volu = (volu - 0.1)
            else:
                volu = 0
            mixer.music.set_volume(volu) #quieter

    if louder.collidepoint(mx,my):
        draw.rect(screen, white, selectTools["toolHelp"], 0)
        draw.rect(screen, persianGreen, louder, 2)
        screen.blit(ubuntuFont.render(("Want the music to be louder?"), True, black), selectTools["toolHelp1"])
        screen.blit(ubuntuFont.render(("Click to do so!"), True, black), selectTools["toolHelp2"])
        if mb[0] == 1:
            draw.rect(screen, teal, louder, 2)
            init()
            if volu + 0.1 != 1:
                volu = (volu + 0.1)
            else:
                volu = 1
            mixer.music.set_volume(volu) #louder

    #FINDING THE STAMPBOX IF THEY HAVEN'T SCROLLED THROUGH YET
    if stampRect.collidepoint(mx, my) and mb[0] == 1:
        stampUse = True
        toolUse = False
        stampBox = int((mx - stampRect[0]) // stampRectX)
        if stampPage == 2:
            stampBox += 6
        if stampPage == 3:
            stampBox += 12
        stamp = stamps[stampBox][pageVarHold[stampBox]]

    #WRITING THE HELP/ABOUT ICONS FOR //STAMP PAGE 1
    #PAGE 1 - wilson, maxwell, webber, wendy, wickerbottom, wx78
    if stampRect.collidepoint(mx,my):
        stampBox = int((mx - stampRect[0]) // stampRectX)
        if stampPage == 1:
            if stampBox == 0:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing WILSON"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("He grows a magnificent beard, but you'll "), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("have to scroll to see his other personas"), True, black), selectTools["toolHelp3"])
            elif stampBox == 1:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing MAXWELL"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("He's quite dapper, but frail too... "), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("You might as well scroll though his mind.."), True, black), selectTools["toolHelp3"])
            elif stampBox == 2:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing WEBBER"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("He a friend among spiders, with a silky beard."), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("For his, er, portraits, just scroll-"), True, black), selectTools["toolHelp3"])
            elif stampBox == 3:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing WENDY"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("She's haunted by her twin sister Abigail,"), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("who MIGHT show up if you scroll enough..."), True, black), selectTools["toolHelp3"])
            elif stampBox == 4:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing WICKERBOTTOM"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("Knows much stuff, is librarian. Can't sleep.."), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("She would tell you to scroll qUIETLY..."), True, black), selectTools["toolHelp3"])
            elif stampBox == 5:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing WX78"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("He may be a robot, but even robots die-"), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("Rusty dusty and crusty, but still scrolling"), True, black), selectTools["toolHelp3"])

        #WRITING THE HELP/ABOUT ICONS FOR //STAMP PAGE 2
        #PAGE 2 - wes, willow, winona, wolfgang, woodie, beefalo
        if stampPage == 2:
            stampBox += 6
            if stampBox == 6:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing WES"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("He has trouble staying alive, so scrolling to"), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("the rhythm of 'Staying Alive' might help him-"), True, black), selectTools["toolHelp3"])
            elif stampBox == 7:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing WILLOW"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("Pretty sure she's a pyromaniac, but that's ok-"), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("QUICK!!! PUT OUT THE FIRE BY SCROLLING!! GO!!"), True, black), selectTools["toolHelp3"])
            elif stampBox == 8:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing WINONA"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("Skilled in the trades, and even brings her own tools!"), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("To see her skilled skilliness, scroll through!"), True, black), selectTools["toolHelp3"]) 
            elif stampBox == 9:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing WOLFGANG"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("Like everyone else, he's better with a full belly,"), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("but is scared of scrolling in the dark..."), True, black), selectTools["toolHelp3"]) 
            elif stampBox == 10:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing WOODIE"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("Has a very useful axe, and a terrible secret.."), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("Scroll to find out!"), True, black), selectTools["toolHelp3"]) 
            elif stampBox == 11:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing BEEFALO"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("A calm bunch, except when they're not-"), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("Meaning whenever they're not scrolling"), True, black), selectTools["toolHelp3"]) 

        #WRITING THE HELP/ABOUT ICONS FOR //STAMP PAGE 3
        #PAGE 3 - deerclops, krampus, pig, shadowCreature, spider, tallbird
        if stampPage == 3:
            stampBox += 12
            if stampBox == 12:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing DEERCLOPS"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("They're just- no. No one like it when they"), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("show up. Not even if they scroll. Which they can't."), True, black), selectTools["toolHelp3"]) 
            elif stampBox == 13:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing KRAMPUS"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("Since he likes stealing things when people"), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("are naughty, I stole his ability to scroll. Take that-"), True, black), selectTools["toolHelp3"]) 
            elif stampBox == 14:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing PIGS"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("There's more than one type of pig, apparently..."), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("Basically you, but you can scroll. Boom. Roast-."), True, black), selectTools["toolHelp3"]) 
            elif stampBox == 15:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing SHADOW CREATURES"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("They're a cool gang that shows up when"), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("you're insane, so just keep scrolling..."), True, black), selectTools["toolHelp3"]) 
            elif stampBox == 16:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing SPIDER"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("Here are Webber's friends, they missed the"), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render((" party, but at least they showed up to scroll!"), True, black), selectTools["toolHelp3"])
            elif stampBox == 17:
                draw.rect(screen, white, selectTools["toolHelp"], 0)
                screen.blit(ubuntuFontSmol.render(("Introducing TALLBIRD"), True, black), selectTools["toolHelp1"])
                screen.blit(ubuntuFontSmol.render(("Yeah, this is a really tallbird..."), True, black), selectTools["toolHelp2"])
                screen.blit(ubuntuFontSmol.render(("or is it? Scroll to see...."), True, black), selectTools["toolHelp3"]) 

    #HELP ICONS for hovering over PAGE 1 ICON // stamps
    if stampPageSele1.collidepoint(mx, my):
        draw.rect(screen, persianGreen, stampPageSele1, 2)
        draw.rect(screen, white, selectTools["toolHelp"], 0)
        screen.blit(ubuntuFontSmol.render(("PAGE 1 OF STAMPS - "), True, black), selectTools["toolHelp1"])
        screen.blit(ubuntuFontSmol.render(("Wilson, Maxwell, Webber, "), True, black), selectTools["toolHelp2"])
        screen.blit(ubuntuFontSmol.render(("Wendy, Wickerbottom, WX78"), True, black), selectTools["toolHelp3"]) 
        if mb[0] == 1:
            draw.rect(screen, teal, stampPageSele1, 2)
            stampPage = 1

    #HELP ICONS for hovering over PAGE 2 ICON // stamps
    if stampPageSele2.collidepoint(mx, my):
        draw.rect(screen, persianGreen, stampPageSele2, 2)
        screen.blit(ubuntuFontSmol.render(("PAGE 2 OF STAMPS - "), True, black), selectTools["toolHelp1"])
        screen.blit(ubuntuFontSmol.render(("Wes, Willow, Winona, "), True, black), selectTools["toolHelp2"])
        screen.blit(ubuntuFontSmol.render(("Wolfgang, Woodie, Beefalo"), True, black), selectTools["toolHelp3"])
        if mb[0] == 1:
            draw.rect(screen, teal, stampPageSele2, 2)
            stampPage = 2

    #HELP ICONS for hovering over PAGE 3 ICON // stamps
    if stampPageSele3.collidepoint(mx, my):
        draw.rect(screen, persianGreen, stampPageSele3, 2)
        screen.blit(ubuntuFontSmol.render(("PAGE 3 OF STAMPS - "), True, black), selectTools["toolHelp1"])
        screen.blit(ubuntuFontSmol.render(("Deerclops, Krampus, Pigs "), True, black), selectTools["toolHelp2"])
        screen.blit(ubuntuFontSmol.render(("Shadow Creatures, Spider, Tallbird"), True, black), selectTools["toolHelp3"])
        if mb[0] == 1:
            draw.rect(screen, teal, stampPageSele3, 2)
            stampPage = 3        

    #HELP ICONS for PAGE 1 // tools
    if toolPage == 1:
        for t in toolPage1:
            if t.collidepoint(mx, my):
                draw.rect(screen, persianGreen, t, 3)
                if t == pencilRect:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("This is a pencil.."), True, black), selectTools["toolHelp1"])
                    screen.blit(ubuntuFont.render(("Have fun drawing I guess..."), True, black), selectTools["toolHelp2"])
                    if mb[0] == 1:
                        toolUse = True
                        stampUse = False
                        tool = "pencil"
                elif t == eraserRect:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("When in doubt..."), True, black), selectTools["toolHelp1"])
                    screen.blit(ubuntuFont.render(("ERASE!!"), True, black), selectTools["toolHelp2"])
                    if mb[0] == 1:
                        toolUse = True
                        stampUse = False
                        tool = "eraser"
                elif t == dottedLine:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("suPPOSED to be a dotted line"), True, black), selectTools["toolHelp1"])
                    screen.blit(ubuntuFont.render(("Have fun?"), True, black), selectTools["toolHelp2"])
                    if mb[0] == 1:
                        toolUse = True
                        stampUse = False
                        tool = "dottedL"
                elif t == lineThing:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("Draw a line!!!!"), True, black), selectTools["toolHelp1"])
                    if mb[0] == 1:
                        toolUse = True
                        stampUse = False
                        tool = "lineThing"
                elif t == rectUnfilled:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("This is a rectangle.."), True, black), selectTools["toolHelp1"])
                    screen.blit(ubuntuFont.render(("an outline, that is..."), True, black), selectTools["toolHelp2"])
                    if mb[0] == 1:
                        toolUse = True
                        stampUse = False
                        tool = "rectUnfilled"
                elif t == rectFilled:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("This is a rectangle..."), True, black), selectTools["toolHelp1"])
                    screen.blit(ubuntuFont.render(("But it's filled this time!!"), True, black), selectTools["toolHelp2"])
                    if mb[0] == 1:
                        toolUse = True
                        stampUse = False
                        tool = "rectFilled"
                elif t == clearCanvas:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("Want to clear the canvas?"), True, black), selectTools["toolHelp1"])
                    screen.blit(ubuntuFont.render(("Click to go ahead!!"), True, black), selectTools["toolHelp2"])
                    if mb[0] == 1:
                        draw.rect(screen, white, canvasRect, 0)
                elif t == ellipseUnfilled:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("This is a circle thing.."), True, black), selectTools["toolHelp1"])
                    screen.blit(ubuntuFont.render(("Just draw it..."), True, black), selectTools["toolHelp2"])
                    if mb[0] == 1:
                        toolUse = True
                        stampUse = False
                        tool = "ellipseUnfilled"
                elif t == ellipseFilled:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("This is a filled circle thing.."), True, black), selectTools["toolHelp1"])
                    screen.blit(ubuntuFont.render(("Have fun again!!!"), True, black), selectTools["toolHelp2"])
                    if mb[0] == 1:
                        toolUse = True
                        stampUse = False
                        tool = "ellipseFilled"
                else:
                    tool = "pencil"
                draw.rect(screen, teal, t, 3)

    #toolPage2 = [eyedropperTool, polygon, textTimes,
    #paintBrush, sprayPaint, textComic,
    #calligraphyRight, calligraphyLeft, textUbuntu]

    #HELP ICONS for PAGE 2 // tools
    if toolPage == 2:
        for t in toolPage2:
            if t.collidepoint(mx, my):
                draw.rect(screen, persianGreen, t, 3)
                if t == eyedropperTool:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("Choose a colour on canvas!!!"), True, black), selectTools["toolHelp1"])
                    if mb[0] == 1:
                        toolUse = True
                        stampUse = False
                        tool = "eyedropper"
                elif t == polygon:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("This is a polygon thing.."), True, black), selectTools["toolHelp1"])
                    if mb[0] == 1:
                        toolUse = True
                        stampUse = False
                        tool = "polygon"
                elif t == textTimes:                    
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("Type in the canvas!"), True, black), selectTools["toolHelp1"])
                    screen.blit(ubuntuFont.render(("TIMES NEW ROMAN"), True, black), selectTools["toolHelp2"])
                    if mb[0] == 1:                        
                        toolUse = True
                        stampUse = False
                        tool = "textTimes"
                elif t == paintBrush:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("Paintbrush!!"), True, black), selectTools["toolHelp1"])
                    screen.blit(ubuntuFont.render(("You can change the width too"), True, black), selectTools["toolHelp2"])
                    if mb[0] == 1:
                        toolUse = True
                        stampUse = False
                        tool = "paintBrush"
                elif t == sprayPaint:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("This is a bottle spray paint!"), True, black), selectTools["toolHelp1"])
                    screen.blit(ubuntuFont.render(("Don't get high off the fumes!"), True, black), selectTools["toolHelp2"])
                    if mb[0] == 1:                        
                        toolUse = True
                        stampUse = False
                        tool = "sprayPaint"
                elif t == textComic:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("Type in the canvas!"), True, black), selectTools["toolHelp1"])
                    screen.blit(ubuntuFont.render(("COMIC SANS"), True, black), selectTools["toolHelp2"])
                    if mb[0] == 1:                        
                        toolUse = True
                        stampUse = False
                        tool = "textComic"
                elif t == calligraphyLeft:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("This is a calligraphy pen,"), True, black), selectTools["toolHelp1"])
                    screen.blit(ubuntuFont.render(("Set leaning towards the left"), True, black), selectTools["toolHelp2"])
                    if mb[0] == 1:                        
                        toolUse = True
                        stampUse = False
                        tool = "calligraphyLeft"
                elif t == calligraphyRight:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("This is another calligraphy pen.."), True, black), selectTools["toolHelp1"])
                    screen.blit(ubuntuFont.render(("Set leaning towards the right"), True, black), selectTools["toolHelp2"])
                    if mb[0] == 1:                        
                        toolUse = True
                        stampUse = False
                        tool = "calligraphyRight"
                elif t == textUbuntu:
                    draw.rect(screen, white, selectTools["toolHelp"], 0)
                    screen.blit(ubuntuFont.render(("Type in the canvas"), True, black), selectTools["toolHelp1"])
                    screen.blit(ubuntuFont.render(("UBUNTU"), True, black), selectTools["toolHelp2"])
                    if mb[0] == 1:                        
                        toolUse = True
                        stampUse = False
                        tool = "textUbuntu"
                else:
                    tool = "pencil"
                draw.rect(screen, teal, t, 3)

    #clearing the canvas - individual cus why not
    if clearCanvas.collidepoint(mx,my) and toolPage == 1:
        draw.rect(screen, persianGreen, clearCanvas, 2)
        if mb[0] == 1:
            draw.rect(screen, teal, clearCanvas, 2)
            draw.rect(screen, white, canvasRect, 0)
            draw.rect(screen, dullMint, canvasRect, 3)

    #changing the tool PAGE
    if toolPageUp.collidepoint(mx, my):
        draw.rect(screen, persianGreen, toolPageUp, 2)
        if mb[0] == 1:
            toolPage = 1
            draw.rect(screen, teal, toolPageUp, 2)
            for tool in toolPage1:
                draw.rect(screen, white, tool, 0)
                draw.rect(screen, goodBlue, tool, 3)

    #changing the tool PAGE
    if toolPageDown.collidepoint(mx, my):
        draw.rect(screen, persianGreen, toolPageDown, 2)
        if mb[0] == 1:
            toolPage = 2
            draw.rect(screen, teal, toolPageDown, 2)
            for tool in toolPage2:
                draw.rect(screen, white, tool, 0)

    #colour selection
    if selectTools["colourWheelRect"].collidepoint(mx, my):
        screen.set_clip(selectTools["colourWheelRect"])
        draw.rect(screen, white, selectTools["toolHelp"], 0)
        screen.blit(ubuntuFont.render(("Choose a colour! Any colour!"), True, black), selectTools["toolHelp1"])
        screen.blit(colourPaletteResized, (selectTools["colourWheelRect"][:2]))
        draw.circle(screen, white, (mx, my), 7, 1)
        if mb[0] == 1:
            currentColour = screen.get_at((mx, my))
            draw.circle(screen, currentColour, (mx, my), 7, 1)
        screen.set_clip(None)

    #choosing the size/width for tools // HELP ICON
    if selectTools["widthChooser"].collidepoint(mx, my):
        draw.rect(screen, persianGreen, selectTools["widthChooser"], 2)        
        draw.rect(screen, white, selectTools["toolHelp"], 0)
        screen.blit(ubuntuFont.render(("Drag to change the width"), True, black), selectTools["toolHelp1"])
        if mb[0] == 1:
            screen.set_clip((selectTools["widthChooser"]))
            if selectTools["widthChooserTiny"].collidepoint(mx, my):
                if mb[0] == 1:
                    screen.blit(entireScreen, (0, 0))
                    radiusOfCircle = int(
                        (my - selectTools["widthChooser"][1]) // 10)  # display for width chooser -> for the radius!!
                    width = int((my - selectTools["widthChooser"][
                        1]) // 5)  # the actual width of stuff for LINES AND STUFF, IF YOU'RE DOING CIRCLE, USE ^
                    draw.circle(screen, currentColour, (widthChooserCenterTop[0], my), radiusOfCircle, 0)
            screen.set_clip(None)

    #hiding everything to be able to see the background // HELP ICON
    if selectTools["hideDraw"].collidepoint(mx, my):
        draw.rect(screen, persianGreen, selectTools["hideDraw"], 2)       
        draw.rect(screen, white, selectTools["toolHelp"], 0)
        screen.blit(ubuntuFont.render(("Click to view/set the current"), True, black), selectTools["toolHelp1"])
        screen.blit(ubuntuFont.render(("background!!"), True, black), selectTools["toolHelp2"])
        if mb[0] == 1:
            draw.rect(screen, teal, selectTools["hideDraw"], 2)
            screen.blit(backgrounds[currentBack], (0, 0))
            hideScreen = True
        else:
            draw.rect(screen, persianGreen, selectTools["hideDraw"], 2)
            preHide = False

    #choosing backgrounds // HELP ICON
    if selectTools["backgroundRect"].collidepoint(mx,my):
        draw.rect(screen, persianGreen, selectTools["backgroundRect"], 2)
        draw.rect(screen, white, selectTools["toolHelp"], 0)
        screen.blit(ubuntuFont.render(("Scroll to see other backgrounds,"), True, black), selectTools["toolHelp1"])
        screen.blit(ubuntuFont.render(("and click to apply to canvas!"), True, black), selectTools["toolHelp2"])
        if mb[0] == 1:
            draw.rect(screen, teal, selectTools["backgroundRect"], 2)
            backgroundPic = transform.scale(backgrounds[currentBack], (canvasRect[2], canvasRect[3]))
            screen.blit(backgroundPic, canvasRect)



    # ===========================================================================================================================================DRAWING ON CANVAS
    # everything here and beyond (until the next line break) concerns the canvas,
    # and the if statements for the given tools, including actions to be done if it is a certain tool

    #actually drawing on the canvas
    if canvasRect.collidepoint(mx, my):
        screen.set_clip(canvasRect)
        if mb[0] == 1:
            if toolUse is True and stampUse is False:

                if tool == "pencil":  # works
                    dist = max(1, int(hypot(mx - omx, my - omy)))
                    sx = (mx - omx) / dist
                    sy = (my - omy) / dist
                    for i in range(dist):
                        dx = int(omx + i * sx)
                        dy = int(omy + i * sy)
                        draw.circle(screen, currentColour, (dx, dy), 2, 0)

                if tool == "eraser":  # works
                    dist = max(1, int(hypot(mx - omx, my - omy)))
                    sx = (mx - omx) / dist
                    sy = (my - omy) / dist
                    for i in range(dist):
                        dx = int(omx + i * sx)
                        dy = int(omy + i * sy)
                        draw.circle(screen, white, (dx, dy), width, 0)

                #if tool == "fillBucket":
                    """ #highkey stolen from Henry Tu's github thing, im sorry but i was desperate
                    # List of pixels that need to be checked
                    colourQueue = [(mx, my)]
                    
                    # Gets the starting colour to make sure only certain pixels are filled
                    startCol = screen.get_at((colourQueue[0]))

                    # Ensures the colour clicked is not the fill colour
                    if startCol != currentColour:
                        # Runs through the list of coordinates
                        if len(colourQueue) > 0:

                            # Checks if the current pixel is the target colour
                            if screen.get_at((colourQueue[0])) == startCol:
                                # Sets the pixel the fill colour
                                screen.set_at(((colourQueue[0])), currentColour)
                                
                                # Checks to make sure the pixel to the left of current pixel is valid
                                if colourQueue[0][1] - 1 >= 0:
                                    # Adds pixel to queue
                                    colourQueue.append((colourQueue[0][0], colourQueue[0][1] - 1))

                                if colourQueue[0][1] + 1 < canvasRect[3]: #to the right
                                    colourQueue.append((colourQueue[0][0], colourQueue[0][1] + 1))

                                if colourQueue[0][0] - 1 >= 0: #above
                                    colourQueue.append((colourQueue[0][0] - 1, colourQueue[0][1]))

                                if colourQueue[0][0] + 1 < canvasRect[2]: #below
                                    colourQueue.append((colourQueue[0][0] + 1, colourQueue[0][1]))

                        # Removes coordinate from the queue
                        del colourQueue[0]
                        """
                if tool == "dottedLine":
                    screen.blit(entireScreen, (0,0))
                    dx = mx-sx
                    dy = my - sy
                    dist = sqrt(dx**2 + dy**2)
                    for d in range(10, int(dist), 10):
                        dotX = int(dx*d /dixt + sx)
                        dotY = int(dy*d /dist + sy)
                        draw.circle(screen, currentColour, (dox,dotY), width)

                if tool == "lineThing":  # works
                    screen.blit(entireScreen, (0, 0))
                    draw.line(screen, currentColour, (startx, starty), (mx, my), width)

                if tool == "rectUnfilled":  # works, but should fill in the corners with larger widths?
                    screen.blit(entireScreen, (0, 0))
                    draw.rect(screen, currentColour, (startx, starty, mx - startx, my - starty), width)

                if tool == "rectFilled":  # works
                    screen.blit(entireScreen, (0, 0))
                    draw.rect(screen, currentColour, (startx, starty, mx - startx, my - starty), 0)

                if tool == "ellipseUnfilled":  # works
                    screen.blit(entireScreen, (0, 0))
                    ellipseRadiusRect = Rect(startx, starty, mx - startx, my - starty)
                    ellipseRadiusRect.normalize()
                    try:
                        draw.ellipse(screen, currentColour, (ellipseRadiusRect), width)
                    except:
                        draw.ellipse(screen, currentColour, ellipseRadiusRect)

                if tool == "ellipseFilled":  # works
                    screen.blit(entireScreen, (0, 0))
                    ellipseRadiusRect = Rect(startx, starty, mx - startx, my - starty)
                    ellipseRadiusRect.normalize()
                    draw.ellipse(screen, currentColour, (ellipseRadiusRect), 0)

                #PAGE 2 BEGINS HERE!!
                
                if tool == "eyedropper":
                    currentColour = screen.get_at((mx, my))

                if tool == "polygon": #wtf was i high
                    #screen.blit(entireScreen, (0,0))
                    polygonCoor = []
                    if len(polygonCoor) == 0:
                        polygonCoor.append((mx,my))
                    elif len(polygonCoor) > 1:
                        polygonCoor.append((mx,my))
                        draw.lines(screen, currentColour, polygonCoor[-1], 2)
                        for p in range(len(polygonCoor) - 1):
                            draw.line(screen, currentColour, polygonList[p], polygonList[p + 1], 2)

                if tool == "textTimes":
                    textContent = ""
                    chosenFont = timesNewRomanFont
                    txtPic = timesNewRomanFont.render((textContent), True, (currentColour))
                    screen.blit(txtPic,(mx-txtPic.get_width()//2, my-txtPic.get_height()//2))

                if tool == "paintBrush":  # sorta works
                    dist = max(1, int(hypot(mx - omx, my - omy)))
                    sx = (mx - omx) / dist
                    sy = (my - omy) / dist
                    for i in range(dist):
                        dx = int(omx + i * sx)
                        dy = int(omy + i * sy)
                        draw.circle(screen, currentColour, (dx, dy), radiusOfCircle,
                                    0)  # when developed alphaCurrentColour, change it

                if tool == "sprayPaint":  # works
                    for i in range(75):
                        sx = randint(-width, width)
                        sy = randint(-width, width)
                        if hypot(sx, sy) <= width:
                            draw.circle(screen, currentColour, (mx + sx, my + sy), 0)

                if tool == "textComic":
                    textContent = ""
                    chosenFont = comicSansFont
                    txtPic = comicSansFont.render((textContent), True, (currentColour))
                    screen.blit(txtPic,(mx-txtPic.get_width()//2, my-txtPic.get_height()//2))

                if tool == "calligraphyLeft":  # works
                    dist = max(1, int(hypot(mx - omx, my - omy)))
                    sx = (mx - omx) / dist
                    sy = (my - omy) / dist
                    for i in range(dist):
                        dx = int(omx + i * sx)
                        dy = int(omy + i * sy)
                        draw.line(screen, currentColour, (dx + 5, dy + 5), (dx - 5, dy - 5), 3)

                if tool == "calligraphyRight":  # works
                    dist = max(1, int(hypot(mx - omx, my - omy)))
                    sx = (mx - omx) / dist
                    sy = (my - omy) / dist
                    for i in range(dist):
                        dx = int(omx + i * sx)
                        dy = int(omy + i * sy)
                        draw.line(screen, currentColour, (dx - 5, dy + 5), (dx + 5, dy - 5),3)

                if tool == "textUbuntu":
                    textContent = ""
                    chosenFont = ubuntuFont
                    txtPic = ubuntuFont.render((textContent), True, (currentColour))
                    screen.blit(txtPic,(mx-txtPic.get_width()//2, my-txtPic.get_height()//2))                 

            if stampUse is True and toolUse is False:
                if stamp is None:
                    if stampPage == 1:
                        stamp = stampIcons[0][stampBox]
                    if stampPage == 2:
                        stamp = stampIcons[1][stampBox]
                    if stampPage == 3:
                        stamp = stampIcons[2][stampBox]
                else:
                    screen.blit(entireScreen, (0, 0))
                    screen.blit( (transform.scale(stamp, (stampRectX, stampRectY))), (mx - stampRectX // 2, my - stampRectY // 2))
    #================================================================================================================================== end of paint functions
        screen.set_clip(None)
    omx, omy = mx, my
    
    display.flip()
quit()
