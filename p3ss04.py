import markovify , glob, random , argparse , json


def parse_model(model) :
	model = json.loads(model)
	print(model["chain"])
	import code; code.interact(local=locals())

def read_text(directory) :
	dire = directory+"*"
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

	return text_model

def create_poem(text_model,lines) :
	out = []
	for i in range(lines) :
		out.append(text_model.make_sentence(tries=1000,max_overlap_ratio=15))
		
	return out

def main() :
	
	f = open("c410.json","r")

	parse_model(f.read())

	#text_model = markovify.Text.from_json(f.read())

	f.close()

	#[ print(x) for x in create_poem(text_model,random.randint(3,10)) ]
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Makes poetry.')
	main()
