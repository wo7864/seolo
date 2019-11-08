import os

for i in range(1, 27):
    com = 'mv infogan_model/type4/type3_{}.ckpt.data-00000-of-00001 infogan_model/type4/type4_{}.ckpt.data-00000-of-00001'.format(i,i)
    os.system(com)
    com = 'mv infogan_model/type4/type3_{}.ckpt.meta infogan_model/type4/type4_{}.ckpt.meta'.format(i,i)
    os.system(com)
    com = 'mv infogan_model/type4/type3_{}.ckpt.index infogan_model/type4/type4_{}.ckpt.index'.format(i,i)
    os.system(com)