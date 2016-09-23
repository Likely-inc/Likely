from sklearn import linear_model
import imageClassifier
import sklearn.feature_extraction
from datetime import datetime



def train(list_of_dicts, new_photo_dict):
    training_vects = []
    labels = []
    for i in range (len(list_of_dicts)):
        this_time = list_of_dicts[i]['created_time']
        format_time = datetime.fromtimestamp(float(this_time)).strftime("%A %H")
        dow = "DOW_" + format_time.split()[0]
        curdict = {list_of_dicts[i]["filter"]: 1, list_of_dicts[i]["location"]: 1, dow: 1}
        for hour, w in [(-1,0.25), (0, 0.5), (1, 0.25)]:
            curdict["hod_" + str((int(format_time.split()[0])+hour) % 24)] = w
        googles = imageClassifier.getImageFeatures(list_of_dicts[i]["image_link"])
        for key in googles.keys():
            for label in googles[key]:
                if label in ["blueMean", "redMean"]:
                    curdict[label] = googles[key][label]
                else:
                    curdict[label] = 1
        training_vects.append(curdict)
        labels.append(list_of_dicts[i]["likes"])

    # vectorizer = sklearn.feature_extraction.DictVectorizer()
    # vectorizer.fit_transform(list_of_dicts)

    print_oneline(training_vects)

    # vectorizer = sklearn.feature_extraction.DictVectorizer()
    # vectorizer.fit_transform(training_vects)
    #
    # data = vectorizer.fit(training_vects)

    # predictor = linear_model.RidgeCV()
    # predictor.fit(data, labels)


    # return predict(predictor, new_vec)
    return 37


def print_oneline(training_vecs):
    print("[training_vec] start")
    for vec in training_vecs:
        print(vec)
    print("[training_vec] start")
    print(training_vecs)


def predict(predictor, new_vector):
    return predictor.predict(new_vector)[0]
