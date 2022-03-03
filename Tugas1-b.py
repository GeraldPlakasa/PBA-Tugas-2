from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import time

def stemmer_stemming(t):
  factory = StemmerFactory()
  stemmer = factory.create_stemmer()

  filename = (t + '.txt')
  teks = open(filename, "r", encoding="utf-8").read()
  start = time.time()
  teks_stem = stemmer.stem(teks)
  waktu = convert_seconds(time.time() - start)
  print(f'waktu proses: {waktu}')
  
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
