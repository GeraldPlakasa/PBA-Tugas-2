import multiprocessing as mp
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import time
from multiprocessing import Process, Queue
from tkinter import *
from tkinter import ttk
import tkinter as tk
from functools import partial

queue = Queue()
waktu_SP = []
waktu_MP = []

def read_in_chunks(file_object, chunk_size=1024 * 1000):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def stemmer_stemming(t, table_hasil, idx):
    global waktu_SP, waktu_MP
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    filename = (t + '.txt')
    teks = open(filename, "r", encoding="utf-8").read()
    start = time.time()
    teks_stem = stemmer.stem(teks)
    waktu = time.time() - start
    print(f'waktu eksekusi: {convert_seconds(waktu)}')

    try:
      table_hasil.insert(parent='',index='end', iid=idx, text='', 
      values=(filename, str(filename.replace("teks", "").replace(".txt", "") + " MB"),round(waktu),0))
      table_hasil.pack()
    except Exception as e:
      table_hasil.item(idx,text="",values=(filename, str(filename.replace("teks", "").replace(".txt", "") + " MB"),round(waktu),waktu_MP[idx]))
    
    waktu_SP.append(round(waktu))

def stem_mp(stemmer, data, proc_num):
    start = time.time()
    result = stemmer.stem(data)
    waktu = time.time() - start
    print(f'dari process nomor ke-{proc_num}, waktu eksekusi {convert_seconds(waktu)}')
    queue.put((result, proc_num, waktu))
    return result

def stemmer_stemming_mp(t, table_hasil, idx):
    global waktu_SP, waktu_MP
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    filename = (t + '.txt')
    teks = open(filename, "r", encoding="utf-8")
    data_pieces = []
    processes = []

    for piece in read_in_chunks(teks):
        data_pieces.append(piece)

    for idx, piece in enumerate(data_pieces):
        p = Process(target=stem_mp, args=(stemmer, piece, idx))
        p.start()
        processes.append(p)

    result_teks = []
    for i in range(len(processes)):
        result = queue.get()
        result_teks.append(result)

    result_teks = sorted(result_teks, key=lambda x: x[1])
    teks_hasil = ""
    for i in result_teks:
        teks_hasil += i[0]

    times = max(result_teks, key=lambda x: x[2])
    print("")
    print(f'waktu eksekusi: {convert_seconds(times[2])}')

    try:
      table_hasil.insert(parent='',index='end',iid=idx,text='',
      values=(filename, str(filename.replace("teks", "").replace(".txt", "") + " MB"),0,round(times[2])))
      table_hasil.pack()
    except Exception as e:
      table_hasil.item(idx,text="",values=(filename, str(filename.replace("teks", "").replace(".txt", "") + " MB"),waktu_SP[idx],round(times[2])))
    
    waktu_MP.append(round(times[2]))
  
def convert_seconds(seconds):
    days, seconds = divmod(seconds, 24 * 60 * 60)
    hours, seconds = divmod(seconds, 60 * 60)
    minutes, seconds = divmod(seconds, 60)
    return days, hours, minutes, seconds

def btnStemming(table_hasil):

  try:
    table_hasil.delete(0)
    table_hasil.delete(1)
    table_hasil.delete(2)
  except Exception as e:
    print(e)
  
  print("Stemming")
  print("")
  print("File 10MB")
  stemmer_stemming("teks10", table_hasil, 0)

  print("File 15MB")
  stemmer_stemming("teks15", table_hasil, 1)

  print("File 20MB")
  stemmer_stemming("teks20", table_hasil, 2)

  print("_"*100)

def btnStemmingMultiprocessing(table_hasil):

  try:
    table_hasil.delete(0)
    table_hasil.delete(1)
    table_hasil.delete(2)
  except Exception as e:
    print(e)

  print("Stemming Multiprocessing")
  print("")
  print("File 10MB")
  stemmer_stemming_mp("teks10", table_hasil, 0)

  print("File 15MB")
  stemmer_stemming_mp("teks15", table_hasil, 1)

  print("File 20MB")
  stemmer_stemming_mp("teks20", table_hasil, 2)

  print("_"*100)

if __name__ == '__main__':

  struct = Tk()
  struct.geometry("930x420")
  struct.title("Pemrosesan Bahasa Alami")

  box1 = tk.Label(struct)

  box1.pack(
      ipadx=10,
      ipady=10,
      expand=True,
      fill='both',
      side='left'
  )

  box2 = tk.Label(struct)

  box2.pack(
      ipadx=10,
      ipady=10,
      expand=True,
      fill='both',
      side='left'
  )

  label = Label(box1, text="Proses Stemming", bg="gray",
                fg="white", font=("Comic Sans MS", 20, "bold"))
  label.place(relx=.5, rely=.2, anchor='center')
  struct.config(background="gray")
  text = StringVar()

  tabel_frame = Frame(box2)
  tabel_frame.pack()

  table_hasil = ttk.Treeview(tabel_frame)
  table_hasil['columns'] = ('data', 'size', 'time_sp', 'time_mp')

  table_hasil.column("#0", width=0,  stretch=NO)
  table_hasil.column("data",anchor=CENTER, width=100)
  table_hasil.column("size",anchor=CENTER,width=100)
  table_hasil.column("time_sp",anchor=CENTER,width=100)
  table_hasil.column("time_mp",anchor=CENTER,width=100)

  table_hasil.heading("#0",text="",anchor=CENTER)
  table_hasil.heading("data",text="Data",anchor=CENTER)
  table_hasil.heading("size",text="Size (MB)",anchor=CENTER)
  table_hasil.heading("time_sp",text="SP Time (sec)",anchor=CENTER)
  table_hasil.heading("time_mp",text="MP Time (sec)",anchor=CENTER)

  table_hasil.pack()

  button = Button(box1, text="Stemming", font=(
    "Times", 10, "bold"), width=30, bd=2, command=partial(btnStemming, table_hasil))
  button.place(relx=.5, rely=.5, anchor='center')
  button = Button(box1, text="Stemming Multiprocessing", font=(
    "Times", 10, "bold"), width=30, bd=2, command=partial(btnStemmingMultiprocessing, table_hasil))
  button.place(relx=.5, rely=.7, anchor='center')

  struct.mainloop()
