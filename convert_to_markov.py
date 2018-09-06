import markovify , glob, random

dire = "/Users/caioluders/Desktop/Textos/p03ms/*"
dire = glob.glob(dire)
text = ""

for n in dire :
	with open(n) as f :
		lines = f.readlines()
		for l in lines :
			l = l.strip()
			if l != "" :
				text += l+"\n"

text_model = markovify.NewlineText(text,state_size=2)

for i in range(random.randint(3,10)) :
	print(text_model.make_sentence(tries=1000,max_overlap_ratio=15))
