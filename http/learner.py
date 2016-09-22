from sklearn import linear_model
# import imageClassifier
from datetime import datetime



def train(list_of_dicts, new_photo_dict):
    training_vects = []
    for i in range (len(list_of_dicts)):
        this_time = list_of_dicts[i]['created_time']
        dow = "DOW_" + datetime.fromtimestamp(this_time).strftime("%A")
        curdict = {list_of_dicts[i]["filter"]: 1, list_of_dicts[i]["location"]: 1, dow: 1}
        training_vects.append(curdict)
    print(training_vects)
    # return predict(predictor, new_vec)


def predict(predictor, new_vector):
    return predictor.predict(new_vector)[0]
