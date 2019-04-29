from django.views import generic
from .models import Music, Emotion, Access
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from .forms import UserForm, MusicForm


from time import time
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
#from sklearn.metrics import classification_report
#from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from keras.preprocessing import image
#import pickle
import cv2
import numpy as np
import logging
from sklearn.model_selection import train_test_split
#from . import dataset_fetch as df
#from . import cascade as casc
from PIL import Image

def Index(request):
    all_emotions = Emotion.objects.all()
    if not request.user.is_authenticated():
        log = False
        return render(request, 'music/index.html', {'all_emotions':all_emotions, 'log':log})
    else:
        log = True
        return render(request, 'music/index.html',{'all_emotions':all_emotions, 'log':log})

def MySong(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        my_music = Music.objects.filter(user=user)
        return render(request, 'music/my_song.html', {'my_music': my_music, 'user': user})

def delete_song(request, song_id):
    music = Music.objects.get(pk=song_id)
    music.delete()
    return render(request, 'music/my_song.html', {'music': music})

def SongCreate(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = MusicForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            music = form.save(commit=False)
            music.user = request.user
            music.song_upload = request.FILES['song_upload']
            music.save()
            return render(request, 'music/index.html', {'music': music})
        context = {
            "form": form,
        }
        return render(request, 'music/music_form.html', context)

class SongDelete(DeleteView):
    model = Music
    success_url = reverse_lazy('my-song')

class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    #display blank form
    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template_name,{'form':form})
    #process form data
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #clean or normalize data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user.set_password(password)
            user.save()
            #login
            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('music/index.html')

        return render(request, self.template_name, {'form': form})

def LoginUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #music = Music.objects.filter(user=request.user)
                user = request.user
                return render(request, 'music/index.html', {'user': user})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)

def detail(request, emotion_id):
        emotion = get_object_or_404(Emotion, pk=emotion_id)
        all_music = emotion.music_set.filter(access=4)
        if not request.user.is_authenticated():
            log = False
            return render(request, 'music/detail.html', {'emotion': emotion, 'all_music': all_music, 'log': log})
        else:
            log = True
            user = request.user
            my_music = emotion.music_set.filter(user=user)
            return render(request, 'music/detail.html', {'emotion': emotion, 'all_music': all_music, 'log':log, 'my_music':my_music})



def detect(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        # -----------------------------
        # opencv initialization

        face_cascade = cv2.CascadeClassifier('/home/dell/project/musicweb/music/dl/haarcascade_frontalface_default.xml')

        cap = cv2.VideoCapture(1)
        # -----------------------------
        # face expression recognizer initialization
        from keras.models import model_from_json
        model = model_from_json(open("/home/dell/project/musicweb/music/dl/models.json", "r").read())
        model.load_weights('/home/dell/project/musicweb/music/dl/models.h5')  # load weights

        # -----------------------------

        emotions = ('Angry', ' ', ' ', 'Happy', 'Sad', 'Surprise', 'Neutral')
        emo = None
        while (True):
            ret, img = cap.read()

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # draw rectangle to main image

                detected_face = img[int(y):int(y + h), int(x):int(x + w)]  # crop detected face
                detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY)  # transform to gray scale
                detected_face = cv2.resize(detected_face, (48, 48))  # resize to 48x48

                img_pixels = image.img_to_array(detected_face)
                img_pixels = np.expand_dims(img_pixels, axis=0)

                img_pixels /= 255  # pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]

                predictions = model.predict(img_pixels)  # store probabilities of 7 expressions

                # find max indexed array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral
                max_index = np.argmax(predictions[0])
                emotion = emotions[max_index]
                emo = emotion
                # write emotion text above rectangle
                cv2.putText(img, emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            # print(emotion)
            # process on detected face end
            # -------------------------
            cv2.imshow('Emotion', img)
            if emo!=None:
                cv2.waitKey(1000)
                cap.release()
                cv2.destroyAllWindows()
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
                break
        # kill open cv things
        user = request.user
        my_emotion = Emotion.objects.filter(emotion=emo)
        music_emotion = Music.objects.filter(emotion=my_emotion, access=4)
        my_music = Music.objects.filter(emotion=my_emotion, access=5, user=user)
        return render(request, 'music/emotion_music.html', {'emotion': my_emotion, 'my_music': my_music,'music_emotion':music_emotion, 'user':user})

