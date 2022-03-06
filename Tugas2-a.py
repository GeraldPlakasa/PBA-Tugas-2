import os
from tkinter import *
import pickle
import codecs
import nltk
# nltk.download('punkt')

struct = Tk()
struct.geometry("254x250")
struct.title("Pemrosesan Bahasa Alami")
label = Label(struct, text="Algoritma Punkt", bg="gray",
              fg="white", font=("Comic Sans MS", 20, "bold"))
label.place(relx=.5, rely=.2, anchor='center')
struct.config(background="gray")
text = StringVar()


def btnPunkt():
    print('─' * 100)
    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
    f = codecs.open("1000.txt", "r", "utf8").read()
    tokenizer.train(f)
    out = open("indonesian.pickle", "wb")
    pickle.dump(tokenizer, out)
    out.close()
    seg_kalimat = nltk.data.load('indonesian.pickle')
    teks = seg_kalimat.tokenize(f)

    # menghapus nilai kosong pada list
    teks = list(filter(None, teks))

    # membuat file hasil / jika sudah ada di replace
    try:
        f2 = open("hasil_punkt.txt", "x")
        f2.close()
    except Exception as e:
        os.remove("hasil_punkt.txt")
        f2 = open("hasil_punkt.txt", "x")
        f2.close()

    for punktz in teks:
        # rename multiple \n to space
        punktz = punktz.replace('\n', ' ')
        # hapus mutiple space
        punktz = re.sub(' +', ' ', punktz)
        print(punktz.strip())
        try:
            f3 = open("hasil_punkt.txt", "a")
            f3.write(punktz.strip()+"\n\n")
            f3.close()
        except Exception as e:
            print(e)


button = Button(struct, text="Punkt", font=(
    "Times", 10, "bold"), width=20, bd=2, command=btnPunkt)
button.place(relx=.5, rely=.5, anchor='center')

struct.mainloop()
