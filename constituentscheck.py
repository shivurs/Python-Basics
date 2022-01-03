from constituents import *
from list2parsetree import *

t_the = Token('DT', 'The')
t_cat = Token('NN', 'cat')
p_the_cat = Phrase('NP', [t_the , t_cat ])

# print(t_the)
# print(t_cat)
# print(p_the_cat)

sentence = [ ' S ' ,
[ ' NP ' ,
[ ' DT ' , ' The ' ],
[ ' NN ' , ' cat ' ]
],
[ ' VP ' ,
[ ' VB ' , ' chases ' ],
[ ' NP ' ,
[ ' DT ' , ' the ' ],
[ ' NN ' , ' mouse ' ]
]
],
[ ' PUNCT ' , ' . ' ]
]

print(list2parsetree(sentence))