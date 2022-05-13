# Library Import
import tkinter as tk
import random
import time
import datetime
from english_words import english_words_lower_alpha_set as kamus

# logic and function
def help():
    choice  = var1.get()
    if choice == 3:
        # Hard
        help_text = "Bantuan: Awal huruf akan dimulai secara random dari kata sebelumnya"
    elif choice == 2:
        # Medium
        help_text = "Bantuan: Awal huruf akan dimulai dari huruf tengah kata sebelumnya"
    else:
        # Easy
        help_text = "Bantuan: Awal huruf akan dimulai dari huruf akhir kata sebelumnya"
    help_plc.configure(text=help_text)

def update_result(text):
    result.configure(text=text)

def new_game():
    global prev_ans, jml_kata, ls_kata, is_playing, addsec, poin, start_huruf

    #Button Config
    guess_button.config(state='normal')
    play_button.configure(state='disabled')
    R1.configure(state='disabled')
    R2.configure(state='disabled')
    R3.configure(state='disabled')
    skor.configure(text='0')
    help()

    #Inisialisasi
    is_playing = True
    addsec = 0
    jml_kata = 0
    poin = 0
    ls_kata = []

    #Ambil 1 kata random dari kamus
    ls_first = random.sample(kamus, 1)
    prev_ans = ls_first[0]

    # Setting Diff Pertama Kali
    choice  = var1.get()
    start_huruf = dif_ref(prev_ans)

    update_result(text="Dimulai dari kata: '" + prev_ans + "' Kata selanjutnya berawalan dari huruf: '" + prev_ans[start_huruf] + "'")


def dif_ref(kata):
    # Setting Diff
    choice  = var1.get()
    if choice == 3:
        # Hard
        start_huruf = random.randint(0, len(kata)-1)
    elif choice == 2:
        # Medium
        start_huruf = len(kata) // 2
    else:
        # Easy
        start_huruf = -1
    return start_huruf

def play_game():
    global prev_ans, jml_kata, ls_kata, is_playing, addsec, poin, start_huruf


    #Ambil jawaban dari formulir
    answer = str(entry_form.get()).lower()

    if ((answer not in kamus) or (answer[0] != prev_ans[start_huruf])): # Jika kata tidak ada di kamus atau Tidak sesuai ketentuan Shiritori
        is_playing = False
        result = endGame()
        timer.configure(text='0')
        help_plc.configure(text=" ")
    elif (answer in ls_kata): # Jika kata yang dimasukkan sudah pernah dijawab
        result = "Anda sudah menjawab dengan kata tersebut\nKata selanjutnya berawalan dari huruf: '" + prev_ans[start_huruf] + "'"
    else: # Jika Benar
        start_huruf = dif_ref(answer)
        result = "Kata '" + answer + "' benar. Kata selanjutnya berawalan dari huruf: '" + answer[start_huruf] + "'"
        ls_kata.insert(0, answer)
        jml_kata += 1
        addsec = 5

        # Scoring
        if (int(timer.cget("text")) > 15):
            poin += 7
        elif (int(timer.cget("text")) > 5):
            poin += 5
        else:
            poin += 3
        timer.configure(text=addsec + int(timer.cget("text")))
        skor.configure(text=poin)

        prev_ans = answer

    #Munculkan status jawaban ke layar
    update_result(result)

    entry_form.delete(0, 'end')

# Fungsi Gameover
def endGame():
    result = "Permainan berakhir. Anda berhasil menyusun " + str(jml_kata) + " kata"
    result += "\n" + "Klik Mulai untuk memulai permainan baru"

    #Reset tombol
    guess_button.configure(state='disabled')
    play_button.configure(state='normal')
    R1.configure(state='normal')
    R2.configure(state='normal')
    R3.configure(state='normal')

    return result

# Fungsi Timer
def countdown(count=15):
    global jml_kata, is_playing, addsec

    timer.configure(text=count)

    if addsec > 0:
        count = count + addsec
        timer.configure(text=count)
    if count > 0 and is_playing:
        window.after(1000, countdown, count-1)
    else:
        timer.configure(text='0')
        result = endGame()
        update_result(result)

    addsec = 0


# Render window ke layar
window = tk.Tk()

window.geometry("625x400")
window.config(bg="#065569")
window.resizable(width=False,height=False)
window.title('Shiritori/Word-Chain')
word_entry = tk.StringVar()

# Elemen Visual
title = tk.Label(window,text="Shiritori/Word-Chain",font=("Arial",24),fg="#fffcbd",bg="#065569")
help_plc = tk.Label(window, text="", font=("Arial", 11, "normal"),fg = "White", bg="#065569", justify=tk.LEFT)
timer_plc = tk.Label(window, text="Timer:", font=("Arial", 12, "normal", "bold"),fg = "White", bg="#065569", justify=tk.LEFT)
timer = tk.Label(window, text="15", font=("Arial", 12, "normal", "bold"),fg = "White", bg="#065569", justify=tk.LEFT)
skor_plc = tk.Label(window, text="Skor:", font=("Arial", 12, "normal", "bold"),fg = "White", bg="#065569", justify=tk.LEFT)
skor = tk.Label(window, text="0", font=("Arial", 12, "normal", "bold"),fg = "White", bg="#065569", justify=tk.LEFT)
entry_form = tk.Entry(window,font=("Arial",11),textvariable=word_entry)
result = tk.Label(window, text="Klik Mulai Untuk Bermain", font=("Arial", 12, "normal", "italic"),fg = "White", bg="#065569", justify=tk.LEFT)
play_button = tk.Button(window, text="Mulai", font=("Arial", 14, "bold"), fg = "Black", bg="#29c70a", command=lambda:[new_game(),countdown(15)])
guess_button = tk.Button(window,text="Submit",font=("Arial",13), state='disabled', fg="#13d675",bg="Black", command=play_game)
exit_button = tk.Button(window,text="Keluar",font=("Arial",14), fg="White", bg="#b82741", command=exit)

# Diff
var1 = tk.IntVar()
R1 = tk.Radiobutton(window, text="Easy", font=("Arial",11), value=1, variable=var1)
R2 = tk.Radiobutton(window, text="Medium", font=("Arial",11), value=2, variable=var1)
R3 = tk.Radiobutton(window, text="Hard", font=("Arial",11), value=3, variable=var1)
var1.set(1)

# Placement
title.place(x=170, y=50)
help_plc.place(x=320, y=120, anchor="center")
timer_plc.place(x=35, y=50)
timer.place(x=100, y=50)
skor_plc.place(x=35, y=75)
skor.place(x=100, y=75)
entry_form.place(x=200, y=150)
result.place(x=320, y=210, anchor="center")
play_button.place(x=200, y=320)
guess_button.place(x=370, y=147)
exit_button.place(x=330,y=320)

R1.place(x=35, y=230)
R2.place(x=35, y=255)
R3.place(x=35, y=280)

# Mulai window looping
window.mainloop()
