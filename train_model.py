
import pandas as pd, joblib, os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

df=pd.read_csv("data/history.csv")
y=1-df["success"]
X=df[["building_type","time_of_day","parcel_count","past_fail_rate","customer_note_len"]]

pre=ColumnTransformer([
("cat",OneHotEncoder(handle_unknown="ignore"),["building_type","time_of_day"]),
("num","passthrough",["parcel_count","past_fail_rate","customer_note_len"])
])

pipe=Pipeline([("pre",pre),("model",LogisticRegression(max_iter=200))])

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
pipe.fit(X_train,y_train)

os.makedirs("models",exist_ok=True)
joblib.dump(pipe,"models/failure_model.pkl")
print("Model trained")
