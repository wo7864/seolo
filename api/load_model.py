import tensorflow as tf
import infogan

def load():
    sess_list = []
    model_list = []
    for phoneme in range(1, 27):
        print('===================================')
        tf.reset_default_graph()
        sess = tf.compat.v1.Session()
        model = infogan.GAN(sess)
        save_dir = "./infogan_model/type2/"
        filename = "bidan_{}_{}.ckpt".format(phoneme, '380')
        print(filename)
        model.saver.restore(sess, save_dir+filename)
        model_list.append(model)
        sess_list.append(sess)
    return model_list, sess_list
