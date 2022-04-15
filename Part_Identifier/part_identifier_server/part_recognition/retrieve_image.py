import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

import cv2
import numpy as np

img = cv2.imread('./parts_test_data/5.png')   
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_blue = np.array([0, 0, 120])
upper_blue = np.array([180, 38, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
result = cv2.bitwise_and(img, img, mask=mask)
b, g, r = cv2.split(result)  
filter = g.copy()

ret,mask = cv2.threshold(filter,10,255, 1)
img[ mask == 0] = 255



fe = FeatureExtractor()
features = []
img_paths = []
for feature_path in Path("./parts_features").glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./rendered_parts") / (feature_path.stem + ".png"))
features = np.array(features)

img = Image.open("./parts_test_data/6.png")
# Extract its features
query = fe.extract(img)
# Calculate the similarity (distance) between images
dists = np.linalg.norm(features - query, axis=1)
# Extract 5 images that have lowest distance
ids = np.argsort(dists)[:3]
scores = [(dists[id], img_paths[id]) for id in ids]
# Visualize the result
axes=[]
fig=plt.figure(figsize=(20,8))

for a in range(1*3):
    score = scores[a]
    axes.append(fig.add_subplot(1, 3, a+1))
    subplot_title=str("{:.3f}".format(score[0]))
    axes[-1].set_title(subplot_title)  
    plt.axis('off')
    im = Image.open(score[1])
    plt.imshow(im, interpolation='nearest')
fig.tight_layout()
plt.show()