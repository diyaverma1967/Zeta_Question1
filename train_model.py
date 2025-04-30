import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report
import joblib

from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier

import warnings
warnings.filterwarnings("ignore")

def ge_syne_dispute_data(n=1000, seed=42):
    np.random.seed(seed)
    data = {
        "transaction_amount": np.round(np.random.exponential(100, n), 2),
        "customer_age": np.random.randint(18, 80, n),
        "customer_tenure": np.random.randint(1, 20, n),
        "account_type": np.random.choice(["savings", "checking", "credit"], n),
        "dispute_reason": np.random.choice(["fraud", "duplicate", "unauthorized", "service_error"], n),
        "channel": np.random.choice(["online", "branch", "phone"], n),
        "customer_flagged": np.random.choice([0, 1], n, p=[0.9, 0.1]),
        "previous_disputes": np.random.poisson(1.2, n),
        "dispute_time": np.random.choice(["day", "night"], n),
    }
    df = pd.DataFrame(data)
    df["high_risk"] = (
        (df["transaction_amount"] > 500) |
        (df["customer_flagged"] == 1) |
        ((df["dispute_reason"] == "fraud") & (df["previous_disputes"] > 2))
    ).astype(int)
    return df

df = ge_syne_dispute_data()
X = df.drop("high_risk", axis=1)
y = df["high_risk"]

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

num_cols = ["transaction_amount", "customer_age", "customer_tenure", "previous_disputes"]
cat_cols = ["account_type", "dispute_reason", "channel", "dispute_time"]

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
])

model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric="logloss"
)

pipeline = ImbPipeline([
    ("pre", preprocessor),
    ("bal", SMOTE(random_state=42)),
    ("clf", model)
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

joblib.dump(pipeline, "dispute_model.pkl")
print(" Model saved to dispute_model.pkl")

