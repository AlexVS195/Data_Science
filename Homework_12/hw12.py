# -*- coding: utf-8 -*-
"""Hw12.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PvYeGtxlI_Zi4VQ0MzV0D7XyUpayrLHv
"""

import nltk
import spacy
import string
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from heapq import nlargest

# Завантаження необхідних ресурсів для nltk
nltk.download('punkt')
nltk.download('stopwords')

# Завантаження мови для SpaCy
nlp = spacy.load('en_core_web_sm')

# Текст для обробки
text = "The Orbiter Discovery, OV-103, is considered eligible for listing in the National Register of Historic Places (NRHP) in the context of the U.S. Space Shuttle Program (1969-2011) under Criterion A in the areas of Space Exploration and Transportation and under Criterion C in the area of Engineering. Because it has achieved significance within the past fifty years, Criteria Consideration G applies. Under Criterion A, Discovery is significant as the oldest of the three extant orbiter vehicles constructed for the Space Shuttle Program (SSP), the longest running American space program to date; she was the third of five orbiters built by NASA. Unlike the Mercury, Gemini, and Apollo programs, the SSP’s emphasis was on cost effectiveness and reusability, and eventually the construction of a space station. Including her maiden voyage (launched August 30, 1984), Discovery flew to space thirty-nine times, more than any of the other four orbiters; she was also the first orbiter to fly twenty missions. She had the honor of being chosen as the Return to Flight vehicle after both the Challenger and Columbia accidents. Discovery was the first shuttle to fly with the redesigned SRBs, a result of the Challenger accident, and the first shuttle to fly with the Phase II and Block I SSME. Discovery also carried the Hubble Space Telescope to orbit and performed two of the five servicing missions to the observatory. She flew the first and last dedicated Department of Defense (DoD) missions, as well as the first unclassified defense-related mission. In addition, Discovery was vital to the construction of the International Space Station (ISS); she flew thirteen of the thirty-seven total missions flown to the station by a U.S. Space Shuttle. She was the first orbiter to dock to the ISS, and the first to perform an exchange of a resident crew. Under Criterion C, Discovery is significant as a feat of engineering. According to Wayne Hale, a flight director from Johnson Space Center, the Space Shuttle orbiter represents a “huge technological leap from expendable rockets and capsules to a reusable, winged, hypersonic, cargo-carrying spacecraft.” Although her base structure followed a conventional aircraft design, she used advanced materials that both minimized her weight for cargo-carrying purposes and featured low thermal expansion ratios, which provided a stable base for her Thermal Protection System (TPS) materials. The Space Shuttle orbiter also featured the first reusable TPS; all previous spaceflight vehicles had a single-use, ablative heat shield. Other notable engineering achievements of the orbiter included the first reusable orbital propulsion system, and the first two-fault-tolerant Integrated Avionics System. As Hale stated, the Space Shuttle remains “the largest, fastest, winged hypersonic aircraft in history,” having regularly flown at twenty-five times the speed of sound."

# Токенізація
doc = nlp(text)
tokens = [token.text for token in doc]

# Токенізація за допомогою nltk
word_tokens = word_tokenize(text)
sentence_tokens = sent_tokenize(text)
stop_words = set(stopwords.words('english'))

# Імпортуємо знаки пунктуації з модуля string
punctuation = string.punctuation + '\n'

# Видалення стоп-слів та пунктуації
filtered_tokens = [word for word in word_tokens if word.lower() not in stop_words and word.isalnum()]

# Підрахунок частоти слів
word_frequencies = {}
for word in doc:
    if word.text.lower() not in stop_words and word.is_alpha:
        if word.text.lower() not in word_frequencies.keys():
            word_frequencies[word.text.lower()] = 1
        else:
            word_frequencies[word.text.lower()] += 1

# Визначення ваги речень
max_frequency = max(word_frequencies.values())
for word in word_frequencies.keys():
    word_frequencies[word] = word_frequencies[word] / max_frequency

# Оцінка речень
sentence_scores = {}
for sent in sentence_tokens:
    for word in word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

# Вибір найважливіших речень
select_length = int(len(sentence_tokens) * 0.3)  # Вибираємо 30% найважливіших речень
summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)

# Формування резюме
final_summary = ' '.join(summary)
paragraph_length = 1
summary_paragraphs = [' '.join(summary[i:i + paragraph_length]) for i in range(0, len(summary), paragraph_length)]
for paragraph in summary_paragraphs:
    print(paragraph)

# Візуалізація частоти слів
word_freq_list = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)[:20]
words, freqs = zip(*word_freq_list)

plt.figure(figsize=(10, 5))
plt.bar(words, freqs, color='blue')
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.title('Top 20 Word Frequencies in the Text')
plt.xticks(rotation=45)
plt.show()