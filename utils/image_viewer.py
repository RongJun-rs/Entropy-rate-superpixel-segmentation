import matplotlib.pyplot as plt


#TODO add possibility  to construct a grid
def show_multiple_images(imgs):
    fig,axs = plt.subplots(len(imgs),sharex=True,sharey=True)
    for i,img in enumerate(imgs):
        axs[i].imshow(img, cmap='gray')
    fig.show()