import syntax_aware
import utility


# Reading Data from text file
file_en = "gsoc/siddhant/DataAug/data-en.txt"
file_sp = "gsoc/siddhant/DataAug/data-sp.txt"
text_en = utility.return_data(file_en)
text_sp = utility.return_data(file_sp)


# Sampling a subset
setsize = 50
shuffled_en, shuffled_sp = utility.randomset(text_en, text_sp, setsize)
#shuffled_en, shuffled_sp = text_en[0:200], text_sp[0:200]


en_sp = []
for i in range(len(shuffled_en)):
    en_sp.append(syntax_aware.getData(shuffled_en[i], shuffled_sp[i]))


en_prob = []
for i in range(len(shuffled_en)):
    en_prob.append(syntax_aware.parsingTree(en_sp[i], 0.1))


dropped_data = []
for i in range(len(en_prob)):
    inde1, inde2 = syntax_aware.top2(en_prob[i])
    dropped_data.append(syntax_aware.dropout(en_sp[i][0], inde1, inde2))

en_sp_dropout = []
for i in range(len(dropped_data)):
    en_sp_dropout.append(syntax_aware.getData(
        dropped_data[i], shuffled_sp[i]))


f = open("gsoc/siddhant/DataAug/dropped_data-en.txt", "w+")
for i in range(len(en_sp_dropout)):
    f.write(en_sp_dropout[i][0]+"\n")

f.close()

f = open("gsoc/siddhant/DataAug/dropped_data-sp.txt", "w+")
for i in range(len(en_sp_dropout)):
    f.write(en_sp_dropout[i][1]+"\n")

f.close()




replaced_data = []
for i in range(len(en_prob)):
    inde1, inde2 = syntax_aware.top2(en_prob[i])
    replaced_data.append(syntax_aware.replacement(en_sp[i][0], inde1, inde2))

en_sp_replacement = []
for i in range(len(replaced_data)):
    en_sp_replacement.append(syntax_aware.getData(
        replaced_data[i], shuffled_sp[i]))


f = open("gsoc/siddhant/DataAug/replaced_data-en.txt", "w+")
for i in range(len(en_sp_replacement)):
    f.write(en_sp_replacement[i][0]+"\n")

f.close()

f = open("gsoc/siddhant/DataAug/replaced_data-sp.txt", "w+")
for i in range(len(en_sp_replacement)):
    f.write(en_sp_replacement[i][1]+"\n")

f.close()

