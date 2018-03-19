from flask_wizard import response

def find_course(session):
    redis_db = session["cache"]
    key="question"
    event={"message":"course has to be found"}
    redis_db.hmset(key, event)
    redis_db.expire(key, 259200)
    response.send(session,"lol")

def find_profession(session):
    response.send(session,"looool")

def trend(session):
    return {"message":"trendify","type":"text"}