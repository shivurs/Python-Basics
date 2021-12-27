class ConLLToken:
    def __init__(self, form, lemma, pos, morph):
        self.form = form
        self.lemma = lemma
        self.pos = pos
        self.morph = morph

    def __str__(self):
        return f"{self.form},{self.lemma},{self.pos},{self.morph}"

    def is_punctuation(self):
        return self.pos == 'PUNCT'
    
    def is_inflected(self):
        return self.lemma != self.form.lower()

    def get_person(self):
        if self.morph[-1].isdigit() == True:
            return self.morph[-1]
        else:
            return None


