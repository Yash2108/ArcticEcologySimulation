import imageio
filenames=['plot' + str(img_count) + '.png' for img_count in range(1,70)]
with imageio.get_writer('movie.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)