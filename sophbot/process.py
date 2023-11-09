import nltk
from math import log

with open("sophraw.txt", "r", encoding='utf8') as inputfile:
    lines = inputfile.readlines()
with open("sophraw.txt", "r", encoding='utf8') as inputfile:
    text = inputfile.read()
all_bigrams = []
bigrams_lines = []
for line in lines:
    words = line.split()
    stripped_words = []
    for word in words:
        stripped_word = word.strip(',;.ʼ·:!')
        stripped_words.append(stripped_word)
    stripped_words.insert(0, 'start')
    stripped_words.append('end')
    bigrams = list(nltk.bigrams(stripped_words))
    all_bigrams = all_bigrams + bigrams
    bigrams_lines.append(bigrams)
bigram_dict = {}
for bigram in all_bigrams:
    if bigram not in bigram_dict:
        bigram_dict[bigram] = 1
    else:
        bigram_dict[bigram] += 1
# print(list(sorted(bigram_dict.items(), key=lambda item: item[1], reverse=True))[:3])

words = text.split()
stripped_words = []
for word in words:
    stripped_word = word.strip(',;.ʼ·:!')
    stripped_words.append(stripped_word)
word_dict = {}
for word in stripped_words:
    if word not in word_dict:
        word_dict[word] = 1
    else:
        word_dict[word] += 1

# print(list(sorted(word_dict.items(), key=lambda item: item[1], reverse=True))[:100])

bigram_scores = {}
for line in bigrams_lines:
    bigram_scores[tuple(line)] = 0
    # num = len(line)
    for bigram in line:
        bigram_scores[tuple(line)] += bigram_dict[bigram]


# print(list(sorted(bigram_scores.items(), key=lambda item: item[1], reverse=True))[:10])
# print(list(sorted(bigram_scores.items(), key=lambda item: item[1], reverse=False))[:500])

# Most 'Sophoclean' (hexametric) line (by syntax/style): Philoctetes 1020: "ἀλλʼ οὐ γὰρ οὐδὲν θεοὶ νέμουσιν ἡδύ μοι," (spoken by Philoctetes) - score of 551
# Least 'Sophoclean'(hexametric) line (by syntax/style): Ajax 997: "μόρον διώκων κἀξιχνοσκοπούμενος." (spoken by Teucer) - score of 4
# Least 'Sophoclean'(hexametric) line (by syntax/style): Ajax 820: "σιδηροβρῶτι θηγάνῃ νεηκονής·." (spoken by Ajax) - score of 4
bigram_max = 551
bigram_min = 4


vocab_scores = {}
for line in lines:
    vocab_scores[line] = 0
    words = line.split()
    num = len(words)
    for word in words:
        new_word = word.strip(',;.ʼ·:!')
        vocab_scores[line] += round(word_dict[new_word] / num, 2)

# print(list(sorted(vocab_scores.items(), key=lambda item: item[1], reverse=True))[:10])
# print(list(sorted(vocab_scores.items(), key=lambda item: item[1], reverse=False))[:10])
vocab_max = 513
vocab_min = 1

# Most 'Sophoclean' (hexametric) line (by vocab): Trachiniae 314: "τί δʼ οἶδʼ ἐγώ, τί δʼ ἄν με καὶ κρίνοις; ἴσως" (spoken by Deianira) - score of 3966
# Most 'Sophoclean' (hexametric) line (by vocab, scaled): Antigone 667: "καὶ σμικρὰ καὶ δίκαια καὶ τἀναντία." - (spoken by Creon) scaled score of 513
# Least 'Sophoclean'(hexametric) line (by vocab): Ajax 820: "σιδηροβρῶτι θηγάνῃ νεηκονής·." (spoken by Ajax) - score of 3
# Least 'Sophoclean'(hexametric) line (by vocab, scaled): Ajax 820: "σιδηροβρῶτι θηγάνῃ νεηκονής·." (spoken by Ajax) - scaled score of 1 (among others) 

# conjectures = ['ὅς γ’ οὐ λογίζῃ, πῶς δε πιστεύοιμι σοι;', 'ὥς στέρεος εῖ! τί οὐχὶ πιστεύεις ἐμοί;', 'θέλεις λέγειν με δεῖν πιθέσθαι σοι, Κρέων;', 'τί ποτε πιθοίμην ἂν γε τοῖςδε σοῖς λόγοις;', 'μηδείς δε πιστεύσει γέ σοι, ὀρθῶς φρονῶν.']

with open("conjectures.txt", "r", encoding='utf8') as conjfile:
    conjectures = conjfile.readlines()

conj_vocab_scores = {}
for conjecture in conjectures:
    conj_vocab_scores[conjecture] = 0
    words = conjecture.split()
    num = len(words)
    for word in words:
        new_word = word.strip(',;.ʼ·:!')
        if new_word in word_dict:
            conj_vocab_scores[conjecture] += word_dict[new_word] / num
    conj_vocab_scores[conjecture] = round((conj_vocab_scores[conjecture] - vocab_min) / (vocab_max - vocab_min), 4)
# print(conj_vocab_scores)

bigrams_conjectures = []
conj_bigram_scores = {}
for conjecture in conjectures:
    words = conjecture.split()
    stripped_words = []
    for word in words:
        stripped_word = word.strip(',;.ʼ·:!')
        stripped_words.append(stripped_word)
    stripped_words.insert(0, 'start')
    stripped_words.append('end')
    bigrams = list(nltk.bigrams(stripped_words))

    conj_bigram_scores[conjecture] = 0
    for bigram in bigrams:
        if bigram in bigram_dict:
            conj_bigram_scores[conjecture] += bigram_dict[bigram]
    conj_bigram_scores[conjecture] = round((conj_bigram_scores[conjecture] - bigram_min) / (bigram_max - bigram_min), 4)
    
"""
    bigrams_conjectures.append(bigrams)

conj_bigram_scores = {}
for conjecture in bigrams_conjectures:
    conj_bigram_scores[tuple(conjecture)] = 0
    for bigram in conjecture:
        if bigram in bigram_dict:
            conj_bigram_scores[tuple(conjecture)] += bigram_dict[bigram]
    conj_bigram_scores[tuple(conjecture)] = (log(conj_bigram_scores[tuple(conjecture)]) - log(bigram_min)) / (log(bigram_max) - log(bigram_min))
"""
# print(conj_bigram_scores)

stopwords_raw = ['μή', 'ἑαυτοῦ', 'ἄν', 'ἀλλʼ', 'ἀλλά', 'ἄλλος', 'ἀπό', 'ἄρα',
             'αὐτός', 'δʼ', 'δέ', 'δή', 'διά', 'δαί', 'δαίς', 'ἔτι', 'ἐγώ',
             'ἐκ', 'ἐμός', 'ἐν', 'ἐπί', 'εἰ', 'εἰμί', 'εἴμι', 'εἰς', 'γάρ', 'γε', 'γʼ',
             'γα', 'ἡ', 'ἤ', 'καί', 'κατά', 'μʼ', 'μέν', 'μετά', 'μή', 'ὁ', 'ὅδε',
             'ὅς', 'ὅστις', 'ὅτι', 'οὕτως', 'οὗτος', 'οὔτε', 'οὖν', 'οὐδείς',
             'οἱ', 'οὐ', 'οὐδέ', 'οὐκ', 'περί', 'πρός', 'σύ', 'σʼ', 'σύν', 'τά', 'τʼ', 'τε',
             'τήν', 'τῆς', 'τῇ', 'τι', 'τί', 'τις', 'τίς', 'τό', 'τοί',
             'τοιοῦτος', 'τόν', 'τούς', 'τοῦ', 'τῶν', 'τῷ', 'ὑμός', 'ὑπέρ',
             'ὑπό', 'ὡς', 'ὦ', 'ὥστε', 'ἐάν', 'παρά', 'σός']

stopwords = []
for stopword in stopwords_raw:
    stopword = stopword.strip("',;.ʼ·:!")
    bare_word = ""
    for letter in stopword:
        if letter in 'ἈἉἊἋἌἍἎἏᾺἀἁἂἃἄἅἆἇὰᾶάᾼᾈᾉᾊᾋᾌᾍᾎᾏᾳᾀᾁᾂᾃᾄᾅᾆᾇᾲᾷ':
            bare_word = bare_word + 'α'
        elif letter in 'ἘἙἚἛἜἝῈἐἑἒἓἔἕὲέ':
            bare_word = bare_word + 'ε'
        elif letter in 'ἨἩἪἫἬἭἮἯῊἠἡἢἣἤἥἦἧὴῆήῌᾘᾙᾚᾛᾝᾞᾟῃᾐᾑᾒᾓᾔᾕᾖᾗῂῇῄ':
            bare_word = bare_word + 'η'
        elif letter in 'ἸἹἺἻἼἽἾἿῚἰἱἲἳἴἵἶἷὶῖί':
            bare_word = bare_word + 'ι'
        elif letter in 'ὈὉὊὋὌὍῸὀὁὂὃὄὅὸό':
           bare_word = bare_word + 'ο'
        elif letter in 'ὙὛὝὟῪὐὑὒὓὔὕὖὗὺῦῧῢΰύ':
           bare_word = bare_word + 'υ'
        elif letter in 'ὨὩὪὫὬὭὮὯῺὠὡὢὣὤὥὦὧὼῶώῼᾨᾩᾪᾫᾬᾭᾮᾯῳᾠᾡᾢᾣᾤᾥᾦᾧῲῷῴ':
           bare_word = bare_word + 'ω'
        else:
          bare_word = bare_word + letter
    stopwords.append(bare_word)

with open("stopwords-el.txt", "r", encoding='utf8') as midwordfile:
    midwords_raw = midwordfile.readlines()         

midwords = []
for midword in midwords_raw:
    midword = midword.strip()
    midword = midword.strip("',;.ʼ·:!")
    bare_word = ""
    for letter in midword:
        if letter in 'ἈἉἊἋἌἍἎἏᾺἀἁἂἃἄἅἆἇὰᾶάᾼᾈᾉᾊᾋᾌᾍᾎᾏᾳᾀᾁᾂᾃᾄᾅᾆᾇᾲᾷ':
            bare_word = bare_word + 'α'
        elif letter in 'ἘἙἚἛἜἝῈἐἑἒἓἔἕὲέ':
            bare_word = bare_word + 'ε'
        elif letter in 'ἨἩἪἫἬἭἮἯῊἠἡἢἣἤἥἦἧὴῆήῌᾘᾙᾚᾛᾝᾞᾟῃᾐᾑᾒᾓᾔᾕᾖᾗῂῇῄ':
            bare_word = bare_word + 'η'
        elif letter in 'ἸἹἺἻἼἽἾἿῚἰἱἲἳἴἵἶἷὶῖί':
            bare_word = bare_word + 'ι'
        elif letter in 'ὈὉὊὋὌὍῸὀὁὂὃὄὅὸό':
           bare_word = bare_word + 'ο'
        elif letter in 'ὙὛὝὟῪὐὑὒὓὔὕὖὗὺῦῧῢΰύ':
           bare_word = bare_word + 'υ'
        elif letter in 'ὨὩὪὫὬὭὮὯῺὠὡὢὣὤὥὦὧὼῶώῼᾨᾩᾪᾫᾬᾭᾮᾯῳᾠᾡᾢᾣᾤᾥᾦᾧῲῷῴ':
           bare_word = bare_word + 'ω'
        else:
          bare_word = bare_word + letter
    midwords.append(bare_word)

# print(stopwords)
# print(midwords)

cur_max = 0
cur_min = 99
max_line = ""
min_line = ""
for line in lines:
    line_score = 0
    words = line.split()
    bare_words = []
    for word in words:
        bare_word = ""
        stripped_word = word.strip(',;.ʼ·:!')
        for letter in stripped_word:
            if letter in 'ἈἉἊἋἌἍἎἏᾺἀἁἂἃἄἅἆἇὰᾶάᾼᾈᾉᾊᾋᾌᾍᾎᾏᾳᾀᾁᾂᾃᾄᾅᾆᾇᾲᾷ':
                bare_word = bare_word + 'α'
            elif letter in 'ἘἙἚἛἜἝῈἐἑἒἓἔἕὲέ':
                bare_word = bare_word + 'ε'
            elif letter in 'ἨἩἪἫἬἭἮἯῊἠἡἢἣἤἥἦἧὴῆήῌᾘᾙᾚᾛᾝᾞᾟῃᾐᾑᾒᾓᾔᾕᾖᾗῂῇῄ':
                bare_word = bare_word + 'η'
            elif letter in 'ἸἹἺἻἼἽἾἿῚἰἱἲἳἴἵἶἷὶῖί':
                bare_word = bare_word + 'ι'
            elif letter in 'ὈὉὊὋὌὍῸὀὁὂὃὄὅὸό':
                bare_word = bare_word + 'ο'
            elif letter in 'ὙὛὝὟῪὐὑὒὓὔὕὖὗὺῦῧῢΰύ':
                bare_word = bare_word + 'υ'
            elif letter in 'ὨὩὪὫὬὭὮὯῺὠὡὢὣὤὥὦὧὼῶώῼᾨᾩᾪᾫᾬᾭᾮᾯῳᾠᾡᾢᾣᾤᾥᾦᾧῲῷῴ':
                bare_word = bare_word + 'ω'
            else:
                bare_word = bare_word + letter
        bare_words.append(bare_word)
    # print(bare_words)
    for bare_word in bare_words:
        if bare_word in stopwords:
            line_score += 1
        elif bare_word in midwords:
            line_score += 2
        else:
            line_score += 3
    if line_score > cur_max:
        cur_max = line_score
        max_line = line
        # print(max_line, cur_max)
    if line_score < cur_min:
        cur_min = line_score
        min_line = line
        # print(min_line, cur_min)
    # if line_score == 24:
        # print (line, line_score)
    # if line_score == 7:
        # print (line, line_score)

# Most 'significant' (hexametric) line: Philoctetes 989: "Ζεύς ἐσθʼ, ἵνʼ εἰδῇς, Ζεύς, ὁ τῆσδε γῆς κρατῶν," (spoken by Odysseus) - score of 24
# Least 'significant' (hexametric) line: Oedipus at Colonus 1269: "παρασταθήτω· τῶν γὰρ ἡμαρτημένων" (spoken by Polynices) - score of 8
signif_min = 8
signif_max = 24

conj_signif_scores = {}
for conjecture in conjectures:
    conj_signif_scores[conjecture] = 0
    words = conjecture.split()
    bare_words = []
    for word in words:
        bare_word = ""
        stripped_word = word.strip(',;.ʼ·:!')
        for letter in stripped_word:
            if letter in 'ἈἉἊἋἌἍἎἏᾺἀἁἂἃἄἅἆἇὰᾶάᾼᾈᾉᾊᾋᾌᾍᾎᾏᾳᾀᾁᾂᾃᾄᾅᾆᾇᾲᾷ':
                bare_word = bare_word + 'α'
            elif letter in 'ἘἙἚἛἜἝῈἐἑἒἓἔἕὲέ':
                bare_word = bare_word + 'ε'
            elif letter in 'ἨἩἪἫἬἭἮἯῊἠἡἢἣἤἥἦἧὴῆήῌᾘᾙᾚᾛᾝᾞᾟῃᾐᾑᾒᾓᾔᾕᾖᾗῂῇῄ':
                bare_word = bare_word + 'η'
            elif letter in 'ἸἹἺἻἼἽἾἿῚἰἱἲἳἴἵἶἷὶῖί':
                bare_word = bare_word + 'ι'
            elif letter in 'ὈὉὊὋὌὍῸὀὁὂὃὄὅὸό':
                bare_word = bare_word + 'ο'
            elif letter in 'ὙὛὝὟῪὐὑὒὓὔὕὖὗὺῦῧῢΰύ':
                bare_word = bare_word + 'υ'
            elif letter in 'ὨὩὪὫὬὭὮὯῺὠὡὢὣὤὥὦὧὼῶώῼᾨᾩᾪᾫᾬᾭᾮᾯῳᾠᾡᾢᾣᾤᾥᾦᾧῲῷῴ':
                bare_word = bare_word + 'ω'
            else:
                bare_word = bare_word + letter
        bare_words.append(bare_word)
    for bare_word in bare_words:
        if bare_word in stopwords:
            conj_signif_scores[conjecture] += 1
        elif bare_word in midwords:
            conj_signif_scores[conjecture] += 2
        else:
            conj_signif_scores[conjecture] += 3
    conj_signif_scores[conjecture] = round((conj_signif_scores[conjecture] - signif_min) / (signif_max - signif_min), 4)
# print(conj_signif_scores)

# print(sum(conj_vocab_scores.values())/5)

with open("sophlemmas.txt", "r", encoding='utf8') as lemmafile:
    lemmas_raw = lemmafile.read()

lemmas = lemmas_raw.split()
lemma_dict = {}
prev = ""
for lemma in lemmas:
    cur = lemma
    if cur not in lemma_dict:
        lemma_dict[cur] = 1
    else:
        if cur != prev:
            lemma_dict[cur] += 1
    prev = cur

with open("conjlemmas.txt", "r", encoding='utf8') as conjlemmafile:
    conj_lemmas_raw = conjlemmafile.readlines()

conj_lemma_scores = {}
for conjecture in conj_lemmas_raw:
    conj_lemma_scores[conjecture] = 0
    conj_lemmas = conjecture.split()
    num = 0
    for lemma in conj_lemmas:
        if lemma not in stopwords_raw:
            num += 1
            if lemma in lemma_dict:
                print(lemma, lemma_dict[lemma])
                conj_lemma_scores[conjecture] += lemma_dict[lemma]
    if num == 0:
        num = 1
    conj_lemma_scores[conjecture] = conj_lemma_scores[conjecture] / (200 * num)
print(conj_lemma_scores)       