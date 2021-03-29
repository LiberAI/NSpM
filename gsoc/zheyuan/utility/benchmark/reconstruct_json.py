def construct_json(dataset_id,infos, questions, sparqls, answers):
    qald_test_answers_dict = {}
    qald_test_answers_dict["dataset"] = {'id':dataset_id}
    qald_test_answers_dict['questions'] = []
    print(len(answers))
    for index,info in enumerate(infos):

        question_dict = info

        id = info["id"]
        question = questions[id]
        question_dict["question"] = [{
            "language" : "en",
            "string" : question
        }]
        question_dict["query"] = {"sparql" : sparqls[index]}
        question_dict["answers"] = answers[index]
        print(answers[index])
        qald_test_answers_dict['questions'].append(question_dict)
    return qald_test_answers_dict

