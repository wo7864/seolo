import os

for i in range(1, 27):
    com = 'mv infogan_model/type2/baram_{}_380.ckpt.data-00000-of-00001 infogan_model/type2/type2_{}.ckpt.data-00000-of-00001'.format(i,i)
    os.system(com)
    com = 'mv infogan_model/type2/baram_{}_380.ckpt.meta infogan_model/type2/type2_{}.ckpt.meta'.format(i,i)
    os.system(com)
    com = 'mv infogan_model/type2/baram_{}_380.ckpt.index infogan_model/type2/type2_{}.ckpt.index'.format(i,i)
    os.system(com)