import boto3.session
import joblib
import boto3
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

BUCKET_NAME = "uploading-model-s3"
S3_FILE_NAME = "iris-model"


def testFunction():
    X,y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"accuracy={acc:.4f}")

    joblib.dump(model, "model.pkl")

    try_upload_pickle_tos3()


def try_upload_pickle_tos3():
    try:
        s3_client = boto3.client("s3")
        session = boto3.session.Session()
        current_region = session.region_name

        s3_client.create_bucket(Bucket=BUCKET_NAME)
    except Exception as err:
        print("Error in creating s3 bucket {err}")

    try:
        s3_client.upload_file("model.pkl", BUCKET_NAME, S3_FILE_NAME)
    except Exception as ex:
        print("Err when uploading file to s3 {ex}")





if __name__ == "__main__":
    testFunction()


   