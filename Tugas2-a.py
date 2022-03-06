import nltk.tokenize.punkt
import nltk.data
import pickle
from timeit import default_timer as timer

cleaning_file = f'1500.txt'


def punkt(file):
    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
    tokenizer.train(file)
    with open('indonesian.pickle', "wb") as out:  # membuat file pickle
        pickle.dump(tokenizer, out)
        out.close()
    sentence_segment = nltk.data.load('indonesian.pickle')
    text_sentence = sentence_segment.tokenize(file)

    file_after_segmentation = f'file_punkt.txt'
    with open(file_after_segmentation, 'w') as f:
        for sentence in text_sentence:
            f.write(sentence.strip())
            f.write('\n')
    print(f'Result: success! file_punkt.txt. saved')


# Main Program
start = timer()
with open(cleaning_file, 'r') as r:
    openFile = r.read()
punkt(openFile)
end = timer()
print(f"\nprocess finished {end-start} seconds")
