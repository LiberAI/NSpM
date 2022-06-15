

def precision(target, predicted):
    target = set(target)
    predicted = set(predicted)
    common = (target).intersection(predicted)
    if len(common) == 0:
        return 0
    else:
        return len(common)/len(predicted)

def recall(target, predicted):
    target = set(target)
    predicted = set(predicted)
    common = (target).intersection(predicted)
    if len(common) == 0:
        return 0
    else:
        return len(common)/len(target)

def f1score(target, predicted):
    p = precision(target, predicted)
    r = recall(target, predicted)
    if (p+r) == 0:
        return 0
    else:
        return (2 * p * r) / (p + r) 
