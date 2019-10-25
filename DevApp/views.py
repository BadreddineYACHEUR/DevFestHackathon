import pyrebase
from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

config = {
    'apiKey': "AIzaSyCEa9hno2HVbGGe_ioYXWP2Gest6wYuz6A",
    'authDomain': "devfest-cdb61.firebaseapp.com",
    'databaseURL': "https://devfest-cdb61.firebaseio.com",
    'projectId': "devfest-cdb61",
    'storageBucket': "devfest-cdb61.appspot.com",
    'messagingSenderId': "594553715761",
    'appId': "1:594553715761:web:b6332be4bc6a43a36a2910",
    'measurementId': "G-W60MDQRSMP"
}

fireBase = pyrebase.initialize_app(config)

auth = fireBase.auth()
db = fireBase.database()


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def sign_in(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get("password")
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            print(user)
            message = "User Authenticated"
            return Response({
                'message': message,
                'user': user['idToken']
            })
        except Exception as e:
            message = "invalid cerediantials"
            return Response({
                'message': message,
                'exeption': type(e)
            })


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def sign_out(request):
    auth.logout(request)


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def sign_up(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get("password")
        age = request.data.get("age")
        gender = request.data.get("gender")

        try:
            user = auth.create_user_with_email_and_password(email, password)
            print(user)
            data = {
                "email": email,
                "password": password,
                "age": age,
                "gender": gender
            }

            db.child('users').child(user['localId']).set(data)
            message = "User Created"

            return Response({
                'message': message,
            })
        except Exception as e:
            message = "invalid cerediantials"
            return Response({
                'message': message,
                'exeption': type(e)
            })

