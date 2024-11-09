# PlacesCNN to predict the scene category, attribute, and class activation map in a single pass
# by Bolei Zhou, sep 2, 2017
# updated, making it compatible to pytorch 1.x in a hacky way

import torch
from torch.autograd import Variable as V
import torchvision.models as models
from torchvision import transforms as trn
from torch.nn import functional as F
import os
import numpy as np
import cv2
from PIL import Image
import IndoorOutdoorClassifier.wideresnet as wideresnet
#import json
#import wideresnet

features_blobs = []

varsha = []
 # hacky way to deal with the Pytorch 1.0 update
def recursion_change_bn(module):
    if isinstance(module, torch.nn.BatchNorm2d):
        module.track_running_stats = 1
    else:
        for i, (name, module1) in enumerate(module._modules.items()):
            module1 = recursion_change_bn(module1)
    return module

def load_labels():
    # prepare all the labels
    # scene category relevant
    file_name_category = 'IndoorOutdoorClassifier/categories_places365.txt'
    classes = list()
    with open(file_name_category) as class_file:
        for line in class_file:
            classes.append(line.strip().split(' ')[0][3:])
    classes = tuple(classes)

    # indoor and outdoor relevant
    file_name_IO = 'IndoorOutdoorClassifier/IO_places365.txt'
    with open(file_name_IO) as f:
        lines = f.readlines()
        labels_IO = []
        for line in lines:
            items = line.rstrip().split()
            labels_IO.append(int(items[-1]) -1) # 0 is indoor, 1 is outdoor
    labels_IO = np.array(labels_IO)

    # scene attribute relevant
    file_name_attribute = 'IndoorOutdoorClassifier/labels_sunattribute.txt'
    with open(file_name_attribute) as f:
        lines = f.readlines()
        labels_attribute = [item.rstrip() for item in lines]
    file_name_W = 'IndoorOutdoorClassifier/W_sceneattribute_wideresnet18.npy'
    W_attribute = np.load(file_name_W)

    return classes, labels_IO, labels_attribute, W_attribute

def hook_feature(module, input, output):
    features_blobs.append(np.squeeze(output.data.cpu().numpy()))

def returnCAM(feature_conv, weight_softmax, class_idx):
    # generate the class activation maps upsample to 256x256
    size_upsample = (256, 256)
    nc, h, w = feature_conv.shape
    output_cam = []
    for idx in class_idx:
        cam = weight_softmax[class_idx].dot(feature_conv.reshape((nc, h*w)))
        cam = cam.reshape(h, w)
        cam = cam - np.min(cam)
        cam_img = cam / np.max(cam)
        cam_img = np.uint8(255 * cam_img)
        output_cam.append(cv2.resize(cam_img, size_upsample))
    return output_cam

def returnTF():
# load the image transformer
    tf = trn.Compose([
        trn.Resize((224,224)),
        trn.ToTensor(),
        trn.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    return tf


def load_model():
    # this model has a last conv feature map as 14x14

    model_file = 'IndoorOutdoorClassifier/wideresnet18_places365.pth.tar'
    
    #import IndoorOutdoorClassifier.wideresnet as wideresnet
    #import wideresnet
    model = wideresnet.resnet18(num_classes=365)
    checkpoint = torch.load(model_file, map_location=lambda storage, loc: storage)
    state_dict = {str.replace(k,'module.',''): v for k,v in checkpoint['state_dict'].items()}
    model.load_state_dict(state_dict)
    
    # hacky way to deal with the upgraded batchnorm2D and avgpool layers...
    for i, (name, module) in enumerate(model._modules.items()):
        module = recursion_change_bn(model)
    model.avgpool = torch.nn.AvgPool2d(kernel_size=14, stride=1, padding=0)
    
    model.eval()



    
    model.eval()
    
    features_names = ['layer4','avgpool'] # this is the last conv layer of the resnet
    for name in features_names:
        model._modules.get(name).register_forward_hook(hook_feature)
    return model

def test_iodetector():

    # load the labels
    classes, labels_IO, labels_attribute, W_attribute = load_labels()

    # load the model
    features_blobs = []
    model = load_model()

    # load the transformer
    tf = returnTF() # image transformer

    # get the softmax weight
    params = list(model.parameters())
    weight_softmax = params[-2].data.numpy()
    weight_softmax[weight_softmax<0] = 0

    # load the test image
    #img_url = '/content/x.jpg'
    #os.system('wget %s -q -O test.jpg' % img_url)
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]  # Add more if needed
    image_files = []
    directory = "testImages"
    for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                if any(filename.endswith(ext) for ext in image_extensions):
                    image_files.append(os.path.join(directory, filename))

    for img_file in image_files:
        print(img_file)
        img = Image.open(img_file)
        input_img = V(tf(img).unsqueeze(0))

        # forward pass
        logit = model.forward(input_img)
        h_x = F.softmax(logit, 1).data.squeeze()
        probs, idx = h_x.sort(0, True)
        probs = probs.numpy()
        idx = idx.numpy()

        #print('RESULT ON ' + img_url)

        # output the IO prediction
        io_image = np.mean(labels_IO[idx[:10]]) # vote for the indoor or outdoor
        if io_image < 0.5:
            if 'INT.' in img_file:
                print('Correct Prediction: --TYPE OF ENVIRONMENT: indoor')
            else:
                print("Incorrect Prediction: Outdoor Image predicted as indoor")
        else:
            if 'EXT.' in img_file:
                print('Correct Prediction: --TYPE OF ENVIRONMENT: outdoor')
            else:
                print("Incorrect Prediction: Indoor Image predicted as outdoor")
            

        
        # output the prediction of scene category
        print('--SCENE CATEGORIES:')
        for i in range(0, 5):
            print('{:.3f} -> {}'.format(probs[i], classes[idx[i]]))


def run_iodetector(img_file):
    output = {}
    classes, labels_IO, labels_attribute, W_attribute = load_labels()

    # load the model
    features_blobs = []
    model = load_model()

    # load the transformer
    tf = returnTF() # image transformer

    # get the softmax weight
    params = list(model.parameters())
    weight_softmax = params[-2].data.numpy()
    weight_softmax[weight_softmax<0] = 0

    # load the test image
    #img_url = '/content/x.jpg'
    #os.system('wget %s -q -O test.jpg' % img_url)
    # image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]  # Add more if needed
    # image_files = []
    # directory = "testImages"
    # for filename in os.listdir(directory):
    #         if os.path.isfile(os.path.join(directory, filename)):
    #             if any(filename.endswith(ext) for ext in image_extensions):
    #                 image_files.append(os.path.join(directory, filename))

    #for img_file in image_files:
    #print(img_file)
    img = Image.open(img_file)
    if img.mode != 'RGB':
            img = img.convert('RGB')
    #print(np.array(img).shape)
    input_img = V(tf(img).unsqueeze(0))

    # forward pass
    logit = model.forward(input_img)
    h_x = F.softmax(logit, 1).data.squeeze()
    probs, idx = h_x.sort(0, True)
    probs = probs.numpy()
    idx = idx.numpy()
    #print(labels_IO[idx[:10]],probs[:10])
    io_image = np.average(labels_IO[idx[:10]],weights= probs[:10]) 
    output["Image"] = img_file
    if io_image<0.5:
            output["Environment Type"] = "Indoor"
    else:
            output["Environment Type"] = "Outdoor"
    output["Scene Category"] =[{"Description":"Probability"}]
    scene = {}
    for i in range(5):
        scene[classes[idx[i]]] = str(round(probs[i],3))
      
    output["Scene Category"].append(scene)
    #print(output)  
    return output