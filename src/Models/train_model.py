"""
src/models/train_model.py

Trains the GeoRiskAI forecasting model.
Predicts NEXT YEAR geopolitical conflict risk.
"""

import pandas as pd
import os
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    accuracy_score,
)


# =========================
# FILE PATHS
# =========================

INPUT_PATH = os.path.join(
    "data",
    "processed",
    "features.csv"
)

MODEL_PATH = os.path.join(
    "models",
    "trained",
    "georisk_rf.pkl"
)

PREDICTIONS_PATH = os.path.join(
    "data",
    "processed",
    "predictions.csv"
)


# =========================
# LOAD DATA
# =========================

def load_data() -> pd.DataFrame:

    print("\nLoading feature dataset...")

    df = pd.read_csv(INPUT_PATH)

    print(
        f"Dataset loaded: "
        f"{df.shape[0]:,} rows"
    )

    return df


# =========================
# PREPARE FEATURES
# =========================

def prepare_data(df):

    feature_cols = [
        "prev_conflict",
        "rolling_conflict_3yr",
        "rolling_deaths_3yr",
        "prev_year_deaths",
        "event_change",
        "conflict_streak",
    ]

    X = df[feature_cols]

    # FUTURE TARGET
    y = df["Future_Conflict"]

    return X, y, feature_cols


# =========================
# TRAIN MODEL
# =========================

def train_model(X, y):

    print("\nTraining Random Forest forecasting model...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=8,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print(
        f"\nModel Accuracy: {accuracy:.2%}"
    )

    print("\nClassification Report:\n")

    print(
        classification_report(
            y_test,
            predictions
        )
    )

    return model


# =========================
# GENERATE PREDICTIONS
# =========================

def generate_predictions(
    model,
    df,
    feature_cols
):

    print("\nGenerating future conflict predictions...")

    X_all = df[feature_cols]

    df["Conflict_Probability"] = (
        model.predict_proba(X_all)[:, 1]
    )

    # =====================================
    # RISK CLASSIFICATION
    # =====================================

    def classify_risk(prob):

        if prob >= 0.75:
            return "Critical"

        elif prob >= 0.50:
            return "High"

        elif prob >= 0.25:
            return "Medium"

        else:
            return "Low"

    df["Risk_Level"] = (
        df["Conflict_Probability"]
        .apply(classify_risk)
    )

    return df


# =========================
# SAVE MODEL
# =========================

def save_model(model):

    os.makedirs(
        os.path.dirname(MODEL_PATH),
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_PATH
    )

    print(
        f"\nModel saved to:"
    )

    print(MODEL_PATH)


# =========================
# SAVE PREDICTIONS
# =========================

def save_predictions(df):

    os.makedirs(
        os.path.dirname(PREDICTIONS_PATH),
        exist_ok=True
    )

    df.to_csv(
        PREDICTIONS_PATH,
        index=False
    )

    print(
        f"\nPredictions saved to:"
    )

    print(PREDICTIONS_PATH)


# =========================
# FEATURE IMPORTANCE
# =========================

def show_feature_importance(
    model,
    feature_cols
):

    importance_df = pd.DataFrame({
        "Feature": feature_cols,
        "Importance": model.feature_importances_
    })

    importance_df = (
        importance_df
        .sort_values(
            "Importance",
            ascending=False
        )
    )

    print("\nFeature Importance:\n")

    print(
        importance_df.to_string(index=False)
    )


# =========================
# MAIN PIPELINE
# =========================

def run():

    df = load_data()

    X, y, feature_cols = prepare_data(df)

    model = train_model(X, y)

    show_feature_importance(
        model,
        feature_cols
    )

    df = generate_predictions(
        model,
        df,
        feature_cols
    )

    save_model(model)

    save_predictions(df)

    return df


# =========================
# EXECUTE
# =========================

if __name__ == "__main__":

    df = run()

    print("\nPrediction sample:\n")

    print(
        df[[
            "Country",
            "Year",
            "Conflict_Probability",
            "Risk_Level",
            "Future_Conflict"
        ]]
        .head(25)
        .to_string(index=False)
    )