import corpus
import lm

text1 = """Hence! home, you idle creatures get you home: Is this a holiday? what! know you not, Being mechanical, you ought not walk Upon a labouring day without the sign Of your profession? Speak, what trade art thou?
Why, sir, a carpenter.
Where is thy leather apron and thy rule? What dost thou with thy best apparel on? You, sir, what trade are you?
Truly, sir, in respect of a fine workman, I am but, as you would say, a cobbler.
But what trade art thou? answer me directly.
A trade, sir, that, I hope, I may use with a safe conscience; which is, indeed, sir, a mender of bad soles.
What trade, thou knave? thou naughty knave, what trade?
Nay, I beseech you, sir, be not out with me: yet, if you be out, sir, I can mend you.
What meanest thou by that? mend me, thou saucy fellow!
Why, sir, cobble you.
Thou art a cobbler, art thou?"""

text2 = """Truly, sir, all that I live by is with the awl: I meddle with no tradesman's matters, nor women's matters, but with awl. I am, indeed, sir, a surgeon to old shoes; when they are in great danger, I recover them. As proper men as ever trod upon neat's leather have gone upon my handiwork.
But wherefore art not in thy shop today? Why dost thou lead these men about the streets?
Truly, sir, to wear out their shoes, to get myself into more work. But, indeed, sir, we make holiday, to see Caesar and to rejoice in his triumph.
Wherefore rejoice? What conquest brings he home? What tributaries follow him to Rome, To grace in captive bonds his chariot-wheels? You blocks, you stones, you worse than senseless things! O you hard hearts, you cruel men of Rome, Knew you not Pompey? Many a time and oft Have you climb'd up to walls and battlements, To towers and windows, yea, to chimney-tops, Your infants in your arms, and there have sat The livelong day, with patient expectation, To see great Pompey pass the streets of Rome: And when you saw his chariot but appear, Have you not made an universal shout, That Tiber trembled underneath her banks, To hear the replication of your sounds Made in her concave shores? And do you now put on your best attire? And do you now cull out a holiday? And do you now strew flowers in his way That comes in triumph over Pompey's blood? Be gone! Run to your houses, fall upon your knees, Pray to the gods to intermit the plague That needs must light on this ingratitude.
Go, go, good countrymen, and, for this fault, Assemble all the poor men of your sort; Draw them to Tiber banks, and weep your tears Into the channel, till the lowest stream Do kiss the most exalted shores of all. See whether their basest metal be not moved; They vanish tongue-tied in their guiltiness. Go you down that way towards the Capitol;
disrobe the images, If you do find them deck'd with ceremonies.
May we do so? You know it is the feast of Lupercal.
It is no matter; let no images Be hung with Caesar's trophies. I'll about, And drive away the vulgar from the streets: So do you too, where you perceive them thick. These growing feathers pluck'd from Caesar's wing Will make him fly an ordinary pitch, Who else would soar above the view of men And keep us all in servile fearfulness.
Calpurnia!
Peace, ho! Caesar speaks.
Calpurnia!
Here, my lord."""

text3 = """Why dost thou with thy best apparel on? you, sir, cobble you.
Where you perceive them thick. these growing feathers pluck'd from caesar's wing will make him fly an ordinary pitch, who else would soar above the view of men and keep us all in servile fearfulness."""

tokens1 = corpus.tokenize(text1)
tokens2 = corpus.tokenize(text2)
tokens3 = corpus.tokenize(text3)
test_text = 'answer me cat, answer me that.'

lang = lm.LanguageModel(2)
lang.train(tokens1 + tokens2 + tokens3)
generated = lang.greedy_generate()
print(generated)
print(lang.get_perplexity_score(generated))
