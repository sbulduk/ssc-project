from flask import Blueprint, jsonify,request,make_response
from functools import wraps
import jwt
import datetime

apiUser=Blueprint("apiUser",__name__,url_prefix="/api/users")
secretKey="sscProjectPrivateKey"
algorithmCrypto="HS256"

def TokenRequired(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=request.args.get("token")
        if not token:
            return jsonify({"success":False,"content":"Token is missing!"}),403
        try:
            data=jwt.decode(token,secretKey,algorithms=algorithmCrypto)
            print(f"{data}")
        except Exception as e:
            print(f"Error Details: {str(e)}")
            return jsonify({"success":False,"content":"Token is invalid!","token":token}),403
        return f(*args,**kwargs)
    return decorated

@apiUser.route("/login",methods=["GET"])
def Login():
    auth=request.authorization
    if auth and auth.password=="pass":
        token=jwt.encode({"user":auth.username,"exp":datetime.datetime.now()+datetime.timedelta(minutes=30)},secretKey)
        return jsonify({"success":True,"token":token})
    return make_response("Could not verify",401,{"WWW-Authenticate":"Basic realm=\"Login Required\""})

@apiUser.route("/account/<int:id>",methods=["GET"])
def GetUserById(id):
    return jsonify({"success":True,"message":f"Selected user: {id}"})

@apiUser.route("/protected")
@TokenRequired
def Protected():
    return jsonify({"success":True,"message":f"You have a valid token. That's how you get this result.\nHere is your token: \"tokken\""})

@apiUser.route("/unprotected")
def Unprotected():
    return jsonify({"success":False,"message":"Unprotected which means anyone can view this page!"})