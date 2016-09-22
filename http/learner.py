from sklearn import linear_model


def train(vectors, likes, new_vec):
    predictor = linear_model.RidgeCV(alphas=[0.1, 1, 10])
    predictor.fit(vectors, likes)
    return predict(predictor, new_vec)


def predict(predictor, new_vector):
    return predictor.predict(new_vector)[0]
