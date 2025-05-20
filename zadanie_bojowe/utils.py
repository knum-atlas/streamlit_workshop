import pandas as pd
import numpy as np
import timeit

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_curve,
    auc,
)


def round_p(n):
    return f"{round(n * 100, 2)}%"


def load_data(path_to_file="./data.csv"):
    df = pd.read_csv(path_to_file)
    y = df["Cured"]
    X = df.drop(columns=["Cured"])
    return X, y


def prepare_data(X, y):
    return train_test_split(X, y, test_size=0.33, random_state=42)


def train_model(hyperparams, X_train, X_test, y_train, y_test):
    import time
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        confusion_matrix, roc_curve, auc
    )

    start = time.time()
    model = RandomForestClassifier(**hyperparams)
    model.fit(X_train, y_train)

    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    y_test_prob = model.predict_proba(X_test)[:, 1]

    train_score = accuracy_score(y_train, y_train_pred)
    test_score = accuracy_score(y_test, y_test_pred)
    precision = precision_score(y_test, y_test_pred)
    recall = recall_score(y_test, y_test_pred)
    f1 = f1_score(y_test, y_test_pred)
    confusion = confusion_matrix(y_test, y_test_pred)

    fpr, tpr, _ = roc_curve(y_test, y_test_prob)
    roc_auc = auc(fpr, tpr)

    end = time.time()
    run_time = end - start

    return (
        train_score,
        test_score,
        precision,
        recall,
        f1,
        confusion,
        run_time,
        fpr,
        tpr,
        roc_auc,
        model
    )


def produce_confusion(cm):
    import altair as alt

    data = pd.DataFrame(
        {
            "Actual": np.array(["Positive", "Negative", "Positive", "Negative"]),
            "Predicted": np.array(["Positive", "Negative", "Negative", "Positive"]),
            "Count": np.array([cm[0, 0], cm[1, 1], cm[1, 0], cm[0, 1]]),
            "Color": np.array(["#66BB6A", "#66BB6A", "#EF5350", "#EF5350"]),
        }
    )

    heatmap = (
        alt.Chart(data)
        .mark_rect()
        .encode(
            x="Actual:N",
            y="Predicted:N",
            color=alt.Color("Color:N", scale=None, legend=None),
            tooltip=["Actual:N", "Predicted:N", "Count:Q"],
        )
        .properties(title="Confusion Matrix", width=300, height=350)
    )

    text = (
        alt.Chart(data)
        .mark_text(fontSize=16, fontWeight="bold")
        .encode(
            x="Actual:N",
            y="Predicted:N",
            text="Count:Q",
            color=alt.condition(
                alt.datum.Color == "#EF5350", alt.value("white"), alt.value("black")
            ),
        )
    )

    return (heatmap + text).configure_title(fontSize=18, fontWeight="bold", anchor="middle")
