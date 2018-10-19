import markovify , glob, random , sys

dire = "/Users/caioluders/Desktop/Textos/p03ms/*"
dire = glob.glob(dire)
text = ""

for n in dire :
	try : 
		with open(n) as f :
			lines = f.readlines()
			for l in lines :
				l = l.strip()
				if l != "" :
					text += l+"\n"
	except :
		pass
text_model = markovify.NewlineText(text,state_size=2).to_json()

fo = open(sys.argv[1],'w')
fo.write(text_model)
fo.close()
