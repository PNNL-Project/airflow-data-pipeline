import csv

from joblib import load
from Util import fileUtil, commonUtil


def make_predictions(clf, row, label):
    """
    make prediction
    """
    pred_matrix = clf.predict_proba([row])
    tmp = pred_matrix[0].tolist()

    idx = tmp.index(max(tmp))
    return label[idx]

def prediction_flow(csv_filepath, prediction_filepath, model_filepath, labels, YESTERDAY):
    """
    Prediction flows reads the file, removes columns not allowed in ml model,
    makes predictions, appends predictions to original dataframe, filters out necessary columns

    args:
        csv_filepath str Filepath of the aggregated csv
        model_filepath str Filepath of the joblib file
        labels list List of strings for the label, order matters
        remove_columns list List of strings for columns that need to be removed before placing in model
        retain_columns list List of strings for columns that need to be kept overall before storing in DB

    """
    # create list for predictions
    predictions = []

    # Load our pre-trained model
    model_filepath = commonUtil.getPath(model_filepath)
    clf = load(model_filepath)

    # read the data_temperature, header included
    csv_filepath = commonUtil.getPath(csv_filepath)
    df_model_input = fileUtil.retainTimeColumnsInCSV(csv_filepath)

    # make a list of prediction labels
    for row in df_model_input.values:
        prediction = make_predictions(clf, row, labels)
        predictions.append(prediction)

    prediction_filepath = commonUtil.getPath(prediction_filepath)
    vals = commonUtil.d(['Date','Label','Frequency'])
    fileUtil.saveDataToCSV(prediction_filepath, vals)

    res = []
    for label in labels:
        tmp = [YESTERDAY,label]
        tmp.append(predictions.count(label))
        res.append(tmp)
    fileUtil.addLinesToCSV(prediction_filepath,res)