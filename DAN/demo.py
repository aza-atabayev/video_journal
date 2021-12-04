import os
import argparse

from PIL import Image
import cv2

import torch
from torchvision import transforms

from DAN.networks.dan import DAN

crop_sizes = {
    "x1": 600,
    "y1": 100,
    "x2": 1150,
    "y2": 600,
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, help='Image file for evaluation.')
    parser.add_argument('--video', type=str, help='Video file for evaluation')
 
    return parser.parse_args()

class Model():
    def __init__(self):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.data_transforms = transforms.Compose([
                                    transforms.Resize((224, 224)),
                                    transforms.ToTensor(),
                                    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                    std=[0.229, 0.224, 0.225])
                                ])
        self.labels = ['neutral', 'happy', 'sad', 'surprise', 'fear', 'disgust', 'anger', 'contempt']

        self.model = DAN(num_head=4, num_class=8)
        checkpoint = torch.load('DAN/checkpoints/affecnet8_epoch5_acc0.6209.pth',
            map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'],strict=True)
        self.model.to(self.device)
        self.model.eval()
    
    def fit(self, img):
        #img = Image.open(path).convert('RGB')
        img = Image.fromarray(img)
        img = self.data_transforms(img)
        img = img.view(1,3,224,224)
        img = img.to(self.device)

        with torch.set_grad_enabled(False):
            out, _, _ = self.model(img)
            _, pred = torch.max(out,1)
            index = int(pred)
            label = self.labels[index]

            return index, label

def get_prediction_video(video_path):
    assert os.path.exists(video_path)
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    n_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print(fps, n_frames)   

    #x1, y1, x2, y2 = crop_sizes["x1"], crop_sizes["y1"], crop_sizes["x2"], crop_sizes["y2"]
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    model = Model()
    prediction = []
    for idx in range(0, n_frames, int(1/2*fps)):
        video.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('gray.jpeg',gray)
        face = face_cascade.detectMultiScale(gray, 1.1, 4)
        if face != ():
            x, y, w, h = face[0]
            frame = frame[y:y+h, x:x+w]
            cv2.imwrite('frame.jpeg',frame)
            index, label = model.fit(frame)
            prediction.append((label, idx/fps))
        else:
            prediction.append(("neutral", idx/fps))
        print(f'emotion label: {label} at {idx/fps} seconds')
    return prediction


if __name__ == "__main__":
    args = parse_args()

    model = Model()

    #image = args.image
    video_path = args.video
    #assert os.path.exists(video_path)
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    n_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print(fps, n_frames)   

    x1, y1, x2, y2 = crop_sizes["x1"], crop_sizes["y1"], crop_sizes["x2"], crop_sizes["y2"]

    #assert os.path.exists(image)
    for idx in range(0, n_frames, int(1/2*fps)):
        video.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = video.read()
        frame = frame[y1:y2, x1:x2]
        index, label = model.fit(frame)
        print(f'emotion label: {label} at {idx/fps} seconds')
    video.release()

