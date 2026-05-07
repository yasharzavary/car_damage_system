from flask import Flask, request, jsonify
import torch
from torch import nn
from torchvision import models, transforms
from PIL import Image
import io

app = Flask(__name__)

# model class names
class_names = ['Front Breakage', 'Front Crushed', 'Front Normal',
               'Rear Breakage', 'Rear Crushed', 'Rear Normal']

class CarClassifierResNet(nn.Module):
    def __init__(self, num_classes=6, dropout_rate=0.5):
        super().__init__()
        self.model = models.resnet50(weights=None)
        for param in self.model.parameters():
            param.requires_grad = False
        for param in self.model.layer4.parameters():
            param.requires_grad = True
        self.model.fc = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(self.model.fc.in_features, num_classes)
        )
    def forward(self, x):
        return self.model(x)

# load trained model
model = CarClassifierResNet(num_classes=6)
model.load_state_dict(torch.load("model/saved_model.pth", map_location="cpu"))
model.eval()

@app.route('/', methods=['GET'])
def health():
    return "OK"

@app.route('/predict', methods=['POST'])
def predict():
    # get image and convert to RGB
    file = request.files['image']
    image = Image.open(io.BytesIO(file.read())).convert("RGB")
    # transform data to size of input depend on model
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])
    # predict and send back the data
    tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(tensor)
        _, predicted = torch.max(output, 1)
    return jsonify({"result": class_names[predicted.item()]})

if __name__ == '__main__':
    print("Inference server running on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)