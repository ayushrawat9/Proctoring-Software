import logging
from email import message

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect
from accounts.models import UserProfile
import numpy as np
import base64, cv2
from deepface import DeepFace
from .segmentation import get_segmented_image


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        user_image = request.POST["image_hidden"]
        verifying_authority = request.POST["verifying_authority"]

        # user_image = np.frombuffer(base64.b64decode(user_image), np.uint8)
        # user_image = get_segmented_image(user_image)
        # retval, buffer = cv2.imencode('.jpg', user_image)
        # user_image = base64.b64encode(buffer)

        role = request.POST['role']

        if pass1 != pass2:
            message.error(request, "Password didn't match")

        user = UserProfile(username=username, email=email, password=pass1, user_image=user_image, first_name=first_name,
                           last_name=last_name, role=role,verifying_authority = verifying_authority)
        user.set_password(pass1)
        user.save()
        messages.success(request, "Your account has been successfully created")
        return redirect('signin')
    return render(request, 'accounts/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']
        user_image = request.POST["image_hidden"]

        if not UserProfile.objects.filter(username=username).values("password"):
            messages.error(request, "User not found!")
            return render(request, "accounts/signin.html")

        user = UserProfile.objects.filter(username=username)[0]
        if not user.verified:
            messages.error(request, "User Not Verified Please Contact Administrator")
            return render(request, "accounts/signin.html")

        logging.info(f"Username:  {user.username}")
        imgdata1 = user.user_image
        imgdata2 = user_image
        np_arr_1 = np.frombuffer(base64.b64decode(imgdata1), np.uint8)
        np_arr_2 = np.frombuffer(base64.b64decode(imgdata2), np.uint8)
        # np_arr_2 = get_segmented_image(np_arr_2)
        image1 = cv2.imdecode(np_arr_1, cv2.COLOR_BGR2GRAY)
        image2 = cv2.imdecode(np_arr_2, cv2.COLOR_BGR2GRAY)
        models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
        model_name = models[-1]
        img_result = DeepFace.verify(image1, image2, model_name=model_name, enforce_detection=False)
        logging.debug(f"Image verifiled  = {img_result}")
        if not img_result["verified"]:
            messages.error(request, "Bad Image Credentials")
            return render(request, "accounts/signin.html")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Authentication Error Check Password !")
            return render(request, "accounts/signin.html")

    return render(request, "accounts/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return HttpResponseRedirect('/')


def home(request):
    if (not request.user.is_authenticated) or request.user.is_anonymous:
        return render(request, 'home.html')

    user = request.user
    logging.debug(f"{user.role=} ")
    context = {"user": user}
    return render(request, 'home.html', context=context)


def my_custom_page_not_found_view(request,error):
    return render(request, '404.html')


def my_custom_error_view(request):
    return render(request, '500.html')