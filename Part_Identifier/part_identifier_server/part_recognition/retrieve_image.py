import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np




fe = FeatureExtractor()
features = []
img_paths = []
for feature_path in Path("./parts_features").glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./rendered_parts") / (feature_path.stem + ".png"))
features = np.array(features)

img = Image.open("./parts_test_data/1.png")
# Extract its features
query = fe.extract(img)
# Calculate the similarity (distance) between images
dists = np.linalg.norm(features - query, axis=1)
# Extract 5 images that have lowest distance
ids = np.argsort(dists)[:5]
scores = [(dists[id], img_paths[id]) for id in ids]
# Visualize the result
axes=[]
fig=plt.figure(figsize=(8,8))

for a in range(1*5):
    score = scores[a]
    axes.append(fig.add_subplot(1, 5, a+1))
    subplot_title=str(score[0])
    axes[-1].set_title(subplot_title)  
    plt.axis('off')
    plt.imshow(Image.open(score[1]))
fig.tight_layout()
plt.show()