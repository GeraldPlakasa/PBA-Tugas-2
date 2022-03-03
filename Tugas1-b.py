import multiprocessing as mp
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import time
from multiprocessing import Process, Queue

queue = Queue()

def read_in_chunks(file_object, chunk_size=1024 * 10):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def stemmer_stemming(t):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    filename = (t + '.txt')
    teks = open(filename, "r", encoding="utf-8").read()
    start = time.time()
    teks_stem = stemmer.stem(teks)
    waktu = convert_seconds(time.time() - start)
    print(f'waktu proses: {waktu}')

def stem_multiprocessing(stemmer, data, proc_num):
    start = time.time()
    result = stemmer.stem(data)
    waktu = convert_seconds(time.time() - start)
    print(f'dari process nomor ke-{proc_num}, waktu eksekusi {waktu}')
    queue.put((result, proc_num))
    return result

def stemmer_stemming_multiprocessing(t):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    filename = (t + '.txt')
    teks = open(filename, "r", encoding="utf-8")
    data_pieces = []
    processes = []

    for piece in read_in_chunks(teks):
        data_pieces.append(piece)

    for idx, piece in enumerate(data_pieces):
        p = Process(target=stem_multiprocessing, args=(stemmer, piece, idx))
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

    f = open("hasil.txt", "w")
    f.write(teks_hasil)
    f.close()
  
def convert_seconds(seconds):
    days, seconds = divmod(seconds, 24 * 60 * 60)
    hours, seconds = divmod(seconds, 60 * 60)
    minutes, seconds = divmod(seconds, 60)
    return days, hours, minutes, seconds

if __name__ == '__main__':

    print("Stemming")
    print("")
    print("File 10MB")
    stemmer_stemming("teks10")

    print("File 15MB")
    stemmer_stemming("teks15")

    print("File 20MB")
    stemmer_stemming("teks20")

    print("_"*100)

    print("Stemming Multiprocessing")
    print("")
    print("File 10MB")
    stemmer_stemming_multiprocessing("teks10")

    print("File 15MB")
    stemmer_stemming_multiprocessing("teks15")

    print("File 20MB")
    stemmer_stemming_multiprocessing("teks20")
