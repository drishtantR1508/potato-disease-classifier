import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from django.shortcuts import render
from .forms import UploadImageForm
from django.core.files.storage import FileSystemStorage
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

MODEL = load_model("../models/cpu_training.h5")
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]
# front end using django templating language
def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.cleaned_data['image']
        im = Image.open(upload)
        image = np.array(im)

        img_batch = np.expand_dims(image, 0)
    
        predictions = MODEL.predict(img_batch)
        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        confidence = np.max(predictions[0])

        print(predicted_class,confidence)

        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        # form = UploadImageForm()
        return render(request, 'uploaded_image.html', {'file_url': file_url,"predicted_class":predicted_class,"confidence":confidence})
    else:
        form = UploadImageForm()

    return render(request, 'upload_image.html', {'form': form})

#API
class PredictAPIView(APIView):
    def post(self,request):
        upload = request.FILES['image']
        im = Image.open(upload)
        image = np.array(im)
        img_batch = np.expand_dims(image, 0)
        predictions = MODEL.predict(img_batch)
        predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        confidence = np.max(predictions[0])

        response = Response()
        response.data = {
                'predicted_class':predicted_class,
                'confidence' : confidence            
                }
        return response