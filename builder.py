from conlltoken import ConLLToken

class ConLLUTokenBuilder:
    pass

    def buildToken(self, line):
        line = line.split()
        form = line[1]
        lemma = line[2]
        pos = line[3]
        morph = line[5]
        token = ConLLToken(form,lemma,pos,morph)
        return token


class ConLL09TokenBuilder:
    pass

    def buildToken(self, line):
        line = line.split()
        form = line[1]
        lemma = line[2]
        pos = line[4]
        morph = line[6]
        token = ConLLToken(form,lemma,pos,morph)
        return token


# builder = ConLLUTokenBuilder()
# line = "1 The the DET _ Definite=Def|PronType=Art _ _ _ _"
# tok = builder.buildToken(line)

# print("Token:", tok)
# print("Type:", type(tok))

