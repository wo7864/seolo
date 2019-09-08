import os

font_list = ['bangwool', 'bangwool_b', 'baram', 'baram_b', 'bawi', 'bawi_b', 'bburi', 'bidan', 'bidan_b', 'bori',
             'bori_b', 'buddle', 'buddle_b', 'dasle', 'goorm', 'groom_b', 'jandi', 'janggun', 'namu',
             'namu_b', 'namu_c', 'sandle', 'seassack', 'seassack_b', 'sonmut', 'sonmut_b', 'taepoong', 'yetdol', 'yuwool']

for i in font_list:
    for j in range(1, 28):
        os.system('mkdir asdf\\{}\\{}'.format(i, str(j)))
