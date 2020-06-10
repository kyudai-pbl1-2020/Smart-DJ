import pickle
import numpy as np

def pred(data):

    gbm = pickle.load(open('./trained_model.pkl', 'rb'))
    preds = gbm.predict(data)
    preds_max = np.argmax(preds, axis=1) 

    return preds_max  
