import os

for i in range(2, 27):
    com = 'mv infogan_model/type1/bidan_{}_380.ckpt.data-00000-of-00001 infogan_model/type1/type1_{}.ckpt.data-00000-of-00001'.format(i,i)
    os.system(com)
    com = 'mv infogan_model/type1/bidan_{}_380.ckpt.meta infogan_model/type1/type1_{}.ckpt.meta'.format(i,i)
    os.system(com)
    com = 'mv infogan_model/type1/bidan_{}_380.ckpt.index infogan_model/type1/type1_{}.ckpt.index'.format(i,i)
    os.system(com)