# !pip install git+https://github.com/sauravjoshi23/Questgen.ai
# !pip install sense2vec==1.0.3

# !pip install git+https://github.com/boudinfl/pke.git

# !python -m nltk.downloader universal_tagset
# !python -m spacy download en

# !wget https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz
# !tar -xvf  s2v_reddit_2015_md.tar.gz
# !ls s2v_old

import nltk
# nltk.download('stopwords')

def question_generator(qg, property1 = False, property2 = False):

    sentence = ""
    if property1 == property2:
        sentence = "the " + property1 + " of ABC is Q" # ABC and Q are just placeholders
    else:
        sentence = "the " + property1 + " of " + property2 + " of ABC is Q"

    payload = {
                "input_text": sentence
            }
    output = qg.predict_mcq(payload)
    # few inputs don't have an output
    send = ""
    try:
        send = output['questions'][-1]['question_statement']
    except:
        send = ""
    
    return send
