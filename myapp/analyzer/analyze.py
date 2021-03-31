from datetime import datetime, timezone
import glob
import numpy as np
import pandas as pd
import pytz
from sklearn.covariance import EllipticEnvelope
from typing import Dict, List
from io import StringIO


# Action constants
LEFT_ACTION = "Left"
JOINED_ACTION = "Joined"
JOINED_BEFORE_ACTION = "Joined before"


# Columns
PARTICIPANT = "participant"
ACTION = "action"
TIMESTAMP = "timestamp"


def get_data_filenames(data_dir="./data/*.csv") -> List[str]:
    return glob.glob(data_dir)


def read_meeting_from_csv(filename_or_buffer) -> pd.DataFrame:
    return pd.read_csv(filename_or_buffer, sep="\t", encoding="utf-16 le",
                       header=0, names=[PARTICIPANT, ACTION, TIMESTAMP],
                       parse_dates=[TIMESTAMP])


def get_participants(df: pd.DataFrame) -> np.array:
    return df[PARTICIPANT].to_numpy()


def get_timestamps(df: pd.DataFrame) -> np.array:
    return df[TIMESTAMP].to_numpy()


def get_left(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get *Left* participants. Temporary disconnections are disregarder by keeping
    only the last *Left* entry for each participant.

    :return: A df with participants who have left.
    """
    return df.loc[df[ACTION] == LEFT_ACTION].sort_values(TIMESTAMP).groupby(PARTICIPANT).tail(1)


def get_joined(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get *Joined* or *Joined before* participants. Subsequent reconnections are
    disregarder by keeping only the first join entry for each participant.

    :return: A df with participants who have joined.
    """
    return df.loc[(df[ACTION] == JOINED_ACTION) | (df[ACTION] == JOINED_BEFORE_ACTION)].sort_values(TIMESTAMP).groupby(PARTICIPANT).head(1)


def get_X(df: pd.DataFrame) -> List[List[int]]:
    """
    Preprocess a dataframe and extract trainable data.

    :return: A 2D numpy array with timestamps.
    """
    def to_timestamp(x): return x.timestamp()
    return df[TIMESTAMP].map(to_timestamp).to_numpy().reshape(-1, 1)


def get_outliers(participants: np.array, predictions: np.array) -> np.array:
    """
    Retrieve participant names for whose detected as outliers, i.e.,
    their prediction is `-1`.

    :return: A list with participant names detected as outliers.
    """
    x = zip(participants, predictions)   # associate each user with it's prediction
    # keep outliers only (prediction == -1)
    x = filter(lambda x: x[1] == -1, x)
    x = map(lambda x: x[0], x)           # back to participant names
    return np.array(list(x))


def detect_outliers(X: np.array) -> Dict:
    """
    Detects outliers.

    :return: A dict with `location`, `covariance` and `predictions`
             for `X` or `None`.
    """
    try:
        cov = EllipticEnvelope(random_state=0).fit(X)

        preds = cov.predict(X)

        [location] = cov.location_
        [[covariance]] = cov.covariance_

        return {"location": datetime.utcfromtimestamp(location), "covariance": covariance, "predictions": preds}

    except ValueError:
        # In this case data do not vary and covariance matrix is 0, cannot determine outliers
        return None


def get_anomalies(ref_df, get_data):

    df = get_data(ref_df)
    X = get_X(df)

    anomalies = detect_outliers(X)

    if anomalies:
        # Join partecipant names with predictions
        outliers = get_outliers(
            get_participants(df), anomalies["predictions"])

        # Get outlier participant details
        outliers_df = df.loc[df[PARTICIPANT].isin(outliers)]

        # Retrieve timestamps and participants from outliers df
        timestamps = get_timestamps(outliers_df)
        participants = get_participants(outliers_df)

        # Convert to np.datetime64 the estimated robust location datetime
        location = np.datetime64(anomalies['location'])

        def get_relative(location, timestamps):
            def to_minutes(td): return td // np.timedelta64(1, 'm')

            def to_seconds(td): return (
                td % np.timedelta64(1, 'm')) // np.timedelta64(1, 's')
            tds = (timestamps - location)
            return np.array([(to_minutes(td), to_seconds(td)) for td in tds])

        # Get the difference between estimated robust location and timestamps from outliers
        relatives = get_relative(location, timestamps)

        # Get a str representation for each outlier: `PARTICIPANT (TIME_DELTA)`
        outliers_processed = list(map(
            lambda x: {"participant": x[0], "delta": f"{x[1][0]:02}:{x[1][1]:02}"}, zip(participants, relatives)))

        # Get statistics
        return {
            "estimated_robust_location": anomalies['location'].strftime('%d/%m/%Y %H:%M:%S'),
            "outliers": outliers_processed
        }


def get_anomalies_list(dfs, get_data):
    return [get_anomalies(df, get_data) for df in dfs]
