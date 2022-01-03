from constituents import *

t_The = Token('DT', 'The')
t_cat = Token('NN', 'cat')
p_the_cat = Phrase('NP', [t_The , t_cat ])

t_chases = Token('VB', 'chases')
t_the = Token('DT', 'the')
t_mouse = Token('NN', 'mouse')
p_chases = Phrase('VP', [t_chases, Phrase('NP', [t_the, t_mouse])])

t_stop = Token('PUNCT', '.')

sent = Phrase('S',[p_the_cat, p_chases, t_stop])
