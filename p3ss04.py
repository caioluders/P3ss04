import markovify , glob, random , argparse , json, random, os


def evolve(chain, mutation_rate) :
	'''
	Evolves a text model based on a mutation rate ( from 0 to 100 ), that is the probability
	the mutation occurs.
	The mutation consist of changing the weight of each chain of Markov,
	maybe I'll add a mutation to the chain itself later.
	'''
	for i in range(len(chain)) :
		for k in chain[i][1].keys() :
			if random.randint(0,100) <= mutation_rate :
				chain_items = list(chain[i][1].values())
				chain_items.sort()
				chain[i][1][k] = random.randint(chain_items[0],chain_items[-1]) # the max value of change is the double of the current weight

	return chain

def create_ecosystem(model, mutation_rate, maxeco) :
	'''
	Build the first ecosystem with maxeco members.
	'''
	ecosystem = []

	try :
		model = json.loads(model)
	except :
		SystemExit('JSON file is incorrect.')

	chain = json.loads(model["chain"])

	for i in range(maxeco) :
		model["chain"] = json.dumps(evolve(chain,mutation_rate))
		ecosystem.append(json.dumps(model))

	return ecosystem

def create_model(directory) :
	'''
	Read all the files of a directory and create a model based on that. Returns the JSON object of that model.
	'''
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

	return json.dumps(text_model)

def darwin(eco,overlap) :
	'''
	The user decides the best model, based on a, poorly implemented, bracket system.
	'''
	while(len(eco) > 1) :
		model1 = markovify.Text.from_json(eco[0])
		model2 = markovify.Text.from_json(eco[1])

		print("------POEMA-0---------")
		print_poem(model1,random.randint(3,10),overlap)
		print("------POEMA-1---------")
		print_poem(model2,random.randint(3,10),overlap)

		chosen = input("\n\nChoose one:")
		del eco[ 0 if "0" in chosen else 1]

	return eco

def print_poem(text_model, lines , overlap) :
	'''
	Print a poem with N lines.
	'''
	[ print(x) for x in create_poem(text_model,lines,overlap) ]

def create_poem(text_model , lines , overlap) :
	'''
	Create a poem with N lines.
	'''
	out = []
	for i in range(lines) :
		out.append(text_model.make_sentence(tries=10000,max_overlap_ratio=overlap))

	return out

def main(args) :

	if args.poems_dir :
		if os.path.isdir(args.poems_dir) :
			model = create_model(args.poems_dir)
		else :
			SystemExit('Argument --poems-dir is not a directory.')
	elif args.model :
		if os.path.isfile(args.model) :
			model = open(args.model,'r').read()
		else :
			SystemExit('Argument --model is not a file.')
	else :
		SystemExit("--model or --poems-dir are required.")

	if args.evolve :
		ecosystem = create_ecosystem(model,args.mutation_rate,args.ecosystem_size)

		ecosystem = darwin(ecosystem,args.overlap)

		while ( input("Stop ?") != "yes" ) :
			ecosystem = create_ecosystem(ecosystem[0],args.mutation_rate,args.ecosystem_size)
			ecosystem = darwin(ecosystem,args.overlap)

		model = ecosystem[0]

	if args.create_poems :
		print_poem(markovify.Text.from_json(model),args.create_poems,args.overlap)

	if args.save_model :
		file_model = open(args.save_model,'w')
		file_model.write(model)
		file_model.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Makes poetry with a Markov Chains and a Genetic algorithm.')
	parser.add_argument('--poems-dir',help='Directory which the poems are to create a new model.',action='store')
	parser.add_argument('--model',help='Use a already generated model in JSON format.', action='store')
	parser.add_argument('--save-model',help='Save the generated model to a JSON file.', action='store')
	parser.add_argument('--mutation-rate',help='The mutation rate of the genetic algorithm in percent.',action='store',default=3,type=int)
	parser.add_argument('--ecosystem-size',help="The number of members of a single ecosystem.",action='store',default=5,type=int)
	parser.add_argument('--create-poems',help='Create poems with N lines.', action='store',type=int)
	parser.add_argument('--evolve',help='Apply a genetic algorithm to evolve the current model.',action='store_true',default=False)
	parser.add_argument('--overlap',help='Max overlap ratio of a sentence in decimal.', action='store',type=float,default=0.75)
	main(parser.parse_args())
