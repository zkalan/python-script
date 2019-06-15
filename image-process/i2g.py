import matplotlib.pyplot as plt
import imageio,os
images = []

f = 0
dir = os.listdir('.')
filenames = []
while f < 1000:
    fi = str(f)+'.png' 
    if fi in dir:
        filenames.append(str(f)+'.png')
    f += 1
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('bird.gif', images,duration=0.3)