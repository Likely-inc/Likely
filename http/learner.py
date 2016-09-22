from sklearn import linear_model
import imageClassifier
import sklearn.feature_extraction
from datetime import datetime



def train(list_of_dicts, new_photo_dict):
    training_vects = []
    for i in range (len(list_of_dicts)):
        this_time = list_of_dicts[i]['created_time']
        dow = "DOW_" + datetime.fromtimestamp(float(this_time)).strftime("%A")
        curdict = {list_of_dicts[i]["filter"]: 1, list_of_dicts[i]["location"]: 1, dow: 1}
        googles = imageClassifier.getImageFeatures(list_of_dicts[i]["image_link"])
        # print(googles)
        for key in googles.keys():
            for label in key:
                curdict[label] = 1
        training_vects.append([curdict])

    # vectorizer = sklearn.feature_extraction.DictVectorizer()
    # vectorizer.fit_transform(list_of_dicts)

    print(training_vects)
    # return predict(predictor, new_vec)
    return 37

def predict(predictor, new_vector):
    return predictor.predict(new_vector)[0]
