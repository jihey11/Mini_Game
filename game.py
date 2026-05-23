#git add .
#git commit -m "커밋 작성"
#git push -u origin main




import tkinter
import random


fnt1 = ("Times New Roman", 24)
fnt2 = ("Times New Roman", 50)
index = 0
timer = 0
score = 0
bg_pos = 0
px = 240
py = 540
PLUS_MAX = 3
METEO_MAX = 25
BULLET_MAX = 1
bactive = [False] * BULLET_MAX
bx = [0] * BULLET_MAX
by = [0] * BULLET_MAX
lx = [0] * PLUS_MAX
ly = [0] * PLUS_MAX
mx = [0] * METEO_MAX
my = [0] * METEO_MAX

key = ""
koff = False

def Key_down(e):
    global key, koff
    key = e.keysym
    koff = False

def Key_up(e):
    global koff
    koff = True

def hit_cheak(x1, y1, x2, y2):
    if((x1 - x2) ** 2 + (y1 - y2) ** 2 < 36 ** 2):
        return True
    return False

def init_bullet():
    for i in range(BULLET_MAX):
        if bactive[i] == False:
            bx[i] = px
            by[i] = py
            bactive[i] = True
            break

def init_puls():
    for i in range(PLUS_MAX):
        lx[i] = random.randint(0,480) + 10
        ly[i] = random.randint(-640, 0) + 10

def init_enemy():
    for i in range(METEO_MAX):
        mx[i] = random.randint(0,480)
        my[i] = random.randint(-640, 0)

def move_bullet():
    global index
    for i in range(BULLET_MAX):
        if bactive[i] == True:
            by[i] += -20
            if by[i] < -10:
                bactive[i] = False
            else:
                cv.create_image(bx[i], by[i], image=img_bullet, tag="SCREEN")
        
def move_enemy():
    global index, timer, score
    for i in range(METEO_MAX):
        my[i] = my[i] + 6 + i / 5
        if my[i] > 660:
            mx[i] = random.randint(0,480)
            my[i] = random.randint(-640, 0)
        if index == 1 and hit_cheak(px, py, mx[i], my[i]) == True:
            index = 2
            timer = 0
        for j in range(BULLET_MAX):
            if bactive[j] and hit_cheak(bx[j], by[j], mx[i], my[i]):
                score += 10
                mx[i] = random.randint(0,480)
                my[i] = random.randint(-640, 0)
                bactive[j] = False
                break
        cv.create_image(mx[i], my[i], image = img_enemy, tag="SCREEN")

def move_plus():
    global index, score
    for i in range(PLUS_MAX):
        ly[i] = ly[i] + 6 + i
        if ly[i] > 660:
            lx[i] = random.randint(0,480) + 10
            ly[i] = random.randint(-640, 0) + 10
        if index == 1 and hit_cheak(px, py, lx[i], ly[i]) == True:
            score += 50
            lx[i] = random.randint(0,480) + 10
            ly[i] = random.randint(-640, 0) + 10
        for j in range(BULLET_MAX):
            if bactive[j] and hit_cheak(bx[j], by[j], lx[i], ly[i]):
                score +=1
                lx[i] = random.randint(0,480)
                ly[i] = random.randint(-640, 0)
                bactive[j] = False
                break    
        cv.create_image(lx[i], ly[i], image = img_plus, tag="SCREEN")

def move_player():
    global px, py
    if key == "Left" and px > 30:
        px -= 10
    if key == "Right" and px < 450:
        px += 10
    if key == "Up" and py > 30:
        py -= 10
    if key == "Down" and py < 610:
        py += 10

    cv.create_image(px, py, image=img_player[timer % 2], tag="SCREEN")
        

def main():
    global key, koff, index, timer, score, bg_pos, px, py
    timer += 1
    bg_pos = (bg_pos + 1) % 640
    cv.delete("SCREEN")

    cv.create_image(240,  bg_pos - 320, image = img_bg, tag="SCREEN")
    cv.create_image(240,  bg_pos + 320, image = img_bg, tag="SCREEN")


    if index == 0:
        cv.create_text(240, 240, text="METEOR", fill="gold", font=fnt2, tag="SCREEN")
        cv.create_text(240, 480, text="Press [SPACE] Key", fill="lime", font=fnt1, tag="SCREEN")
        if key == "space":
            score = 0
            px = 240
            init_enemy()
            init_puls()
            index = 1
    
    if index == 1:
        score += 1
        move_player()
        move_enemy()
        move_plus()
        move_bullet()
        if key == "f":
            init_bullet()

    if index == 2 :
        cv.create_text(240, timer * 4, text="GAME OVER", fill="red", font=fnt1, tag="SCREEN")
        if timer == 60:
            index = 0
            timer = 0

    cv.create_text(240, 30, text="SCORE " + str(score), fill="white", font=fnt1, tag="SCREEN")
    
    if koff == True:
        key = ""
        koff = False

    root.after(50, main)




root = tkinter.Tk()
root.title("GAME")
root.bind("<KeyPress>", Key_down)
root.bind("<KeyRelease>", Key_up)
cv = tkinter.Canvas(width=480, height=640)
cv.pack()
img_player = [
    tkinter.PhotoImage(file="img/starship0.png"),
    tkinter.PhotoImage(file="img/starship1.png")
]
img_enemy = tkinter.PhotoImage(file="img/meteo.png")
img_bg = tkinter.PhotoImage(file="img/cosmo.png")
img_plus = tkinter.PhotoImage(file="img/plus.png")
img_bullet = tkinter.PhotoImage(file="img/xx.png")
main()
root.mainloop()



