from keras.models import model_from_json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def load_z(target):
    with open("./z_value/{}.txt".format(target), "r") as f:
        z_value = f.read().replace("\n", "").replace("[", " ").replace("]", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ")
        z_value = z_value[1:-1].split(" ")
        z_value = [float(f) for f in z_value]
        z_value = np.array(z_value).reshape(100, 100)
    return z_value

def load_model(target):
    json_file = open("./model/{}/{}.json".format(target,target), "r")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("./model/{}/{}.h5".format(target, target))
    return loaded_model

def plot(samples):
    fig = plt.figure(figsize=(10, 10))
    gs = gridspec.GridSpec(10, 10)
    gs.update(wspace=0.05, hspace=0.05)

    for i, sample in enumerate(samples):
        ax = plt.subplot(gs[i])
        plt.axis('off')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_aspect('equal')
        plt.imshow(sample.reshape(28, 28), cmap='Greys_r')
    plt.tight_layout()

    return fig

def div2_draw(z,x1,x2,y1,y2):# 4개의 모양, 2개의 축을 이용하여 변화되는 모습을 그림
    x1 = z[x1]
    x2 = z[x2]
    y1 = z[y1]
    y2 = z[y2]
    for i in range(100):
        one = i % 10
        ten = int(i / 10)
        z[i] = ((x1 * (10 - one) + x2 * one) + (y1 * (10 - ten) + y2 * ten)) / 20
    return z


def div1_draw(z, x, y):
    x = z[x]
    y = z[y]
    z[0] = np.zeros(100)
    for i in range(1, 100):
        one = i % 10
        ten = int(i/10)
        z[i] = (x*one + y*ten)/(one+ten)
    return z


loaded_model = load_model("M")
z = load_z("M")
#z = div2_draw(z, 0,80, 65, 89)
z = div1_draw(z, 0, 80)
generated_images = loaded_model.predict(z)

fig = plot(generated_images)
plt.show()

plt.close(fig)
