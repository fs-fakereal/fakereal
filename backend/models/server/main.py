
import time
from user import authenticate, User

from database import Base, get_connection
from fastapi import FastAPI
#from image import Image
from sqlalchemy.orm import sessionmaker


app = FastAPI()

@app.get('/')
def main():
    return { 'message': 'hi' }

@app.post('/predict')
def predict(data):
    pass

if __name__ == '__main__':
    try:
        engine = get_connection()

        # drops selected table
        Base.metadata.drop_all(bind=engine, tables=[User.__table__])

        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        s = Session()

        #image = Image(str(unix_timestamp), "0", f"localhost:8080/{unix_timestamp}")
        unix_timestamp = time.time()
        acc = User(str(unix_timestamp), "Lm", "Js", "cow@bunga.com", "coolio")

        s.add(acc)
        s.commit()
        res = s.query(User).all()
        for i in res:
            print(i)

        ps = input("password: ")

        if authenticate(s, str(unix_timestamp), ps):
            print("Password is correct")
        else:
            print("Password is incorrect")


        print("Connection success!")
    except Exception as e:
        print("Connect failed...", e)

    s.close()
