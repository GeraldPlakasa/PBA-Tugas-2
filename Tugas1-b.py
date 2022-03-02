from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import time

def stemmer_stemming(t):
  factory = StemmerFactory()
  stemmer = factory.create_stemmer()

  filename = (t + '.txt')
  teks = open(filename, "r").read()
  teks_stem = stemmer.stem(teks)
  print(teks_stem)
  
def convert_seconds(seconds):
    days, seconds = divmod(seconds, 24 * 60 * 60)
    hours, seconds = divmod(seconds, 60 * 60)
    minutes, seconds = divmod(seconds, 60)
    return days, hours, minutes, seconds
  
stemmer_stemming("text10")
# start = time.time()
# waktu = convert_seconds(time.time() - start)
# print('waktu proses: {:.0f}:{:.0f}:{:.0f}'.format(waktu[1], waktu[2], waktu[3]))

stemmer_stemming("text15")
# start = time.time()
# waktu = convert_seconds(time.time() - start)
# print('waktu proses: {:.0f}:{:.0f}:{:.0f}'.format(waktu[1], waktu[2], waktu[3]))

stemmer_stemming("text20")
# start = time.time()
# waktu = convert_seconds(time.time() - start)
# print('waktu proses: {:.0f}:{:.0f}:{:.0f}'.format(waktu[1], waktu[2], waktu[3]))
