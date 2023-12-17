import requests
def Translate(codefile,language):
	url = "https://open-ai-chatgpt.p.rapidapi.com/ask"
	code=open(codefile,"+r")
	query="Translate the following code in "+language[0]+"\n"+code.read()
	code.close()
	payload = { "query": query }
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": "d45fa3ee15msh8306b289aac3254p1de85fjsndabf055441ca",
		"X-RapidAPI-Host": "open-ai-chatgpt.p.rapidapi.com"
	}
	response = requests.post(url, json=payload, headers=headers)
	r=response.json()["response"].split("```")[1]
	outputFile="Result"+language[1]
	Rfile=open(outputFile,"w+")
	Rfile.write(r[r.find("\n"):])
	Rfile.close()
	return outputFile