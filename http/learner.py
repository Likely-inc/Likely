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
            curdict["hod_" + str((int(format_time.split()[1])+hour) % 24)] = w
        googles = imageClassifier.getImageFeatures(list_of_dicts[i]["image_link"], False)
        for key in googles.keys():
            if type(googles[key]) is float or type(googles[key]) is int:
                curdict[key] = googles[key]
            else:
                for label in googles[key]:
                    if label in ["blueMean", "redMean"]:
                        curdict[label] = googles[key][label]
                    elif label in ["joyLikelihood", "sorrowLikelihood", "angerLikelihood", "surpriseLikelihood"]:
                        curdict[label + googles[key][label]] = 1
                    else:
                        curdict[label] = 1
        training_vects.append(curdict)
        labels.append(list_of_dicts[i]["likes"])

    # vectorizer = sklearn.feature_extraction.DictVectorizer()
    # vectorizer.fit_transform(list_of_dicts)

    print_oneline(training_vects)

    vectorizer = sklearn.feature_extraction.DictVectorizer()
    vectorizer.fit_transform(training_vects)

    print("now with the new picture")
    new_vec = {}
    print(new_photo_dict[0])
    googles = imageClassifier.getImageFeatures(new_photo_dict[0], local=True)
    for key in googles.keys():
        if type(googles[key]) is float or type(googles[key]) is int:
            new_vec[key] = googles[key]
        else:
            for label in googles[key]:
                if label in ["blueMean", "redMean"]:
                    new_vec[label] = googles[key][label]
                elif label in ["joyLikelihood", "sorrowLikelihood", "angerLikelihood", "surpriseLikelihood"]:
                    new_vec[label + googles[key][label]] = 1
                else:
                    new_vec[label] = 1
    print("done with the new picture")

    print("fitting data")
    data = vectorizer.transform(training_vects)
    print("fittine new photo")
    print ([new_vec])
    to_predict = vectorizer.transform([new_vec])

    predictor = linear_model.RidgeCV()
    print("trainnn")
    predictor.fit(X=data, y=labels)
    print("predict")
    return predictor.predict(X=new_vec)


def print_oneline(training_vecs):
    print("[training_vec] start")
    for vec in training_vecs:
        print(vec)
    print("[training_vec] start")
    print(training_vecs)


def predict(predictor, new_vector):
    return predictor.predict(new_vector)[0]
