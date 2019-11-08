import tensorflow as tf
import infogan

def load():
    sess_list = []
    model_list = []
    font_list = ['type6', 'type7']
    for font in font_list:
        sess_list2 = []
        model_list2 = []
        for phoneme in range(1, 27):
            print('===================================')
            tf.reset_default_graph()
            sess = tf.compat.v1.Session()
            model = infogan.GAN(sess)
            save_dir = "./infogan_model/{}/".format(font)
            filename = "{}_{}.ckpt".format(font, phoneme)
            print(filename)
            model.saver.restore(sess, save_dir+filename)
            model_list2.append(model)
            sess_list2.append(sess)
        model_list.append(model_list2)
        sess_list.append(sess_list2)
    return model_list, sess_list


