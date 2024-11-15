import nltk
import requests 
import argparse
import csv

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument( "-i","--input")
    parser.add_argument("-o", "--output", default = "./LAB2_OUTPUT.tsv")
    parser.add_argument("--api_key")
    return parser.parse_args()
def main():
    args = get_args()
    uri = "https://uts-ws.nlm.nih.gov/rest/search/current"
    api_key = args.api_key
    with open(args.input, "r") as f:
        line = f.read()
    words = nltk.sent_tokenize(line)
    nouns = []
    for item in words:
        tokenized_words = nltk.pos_tag(nltk.word_tokenize(item))
        # get NN, NNS 
        for token in tokenized_words:
            if token[1] == "NN" or token[1] == "NNS":
              if token[0] not in nouns:
                nouns.append(token[0].lower())
    with open(args.output, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(['INPUT', 'CUI', 'NAME', 'SOURCE VOCAB'])
        
        for noun in nouns:
            # also make sure to check for its plural/singular forms
           search_terms = [noun]
           if noun[-1] =="s":
               search_terms.append(noun[:-1])
           else:
               search_terms.append(noun + "s")
           
           for term in search_terms:
                page = 0
                try:
                    while True:
                        page += 1
                        query = {
                            'string': term,
                            'apiKey': api_key,
                            'searchType': 'exact',
                            'sabs': 'MTH',
                            'pageNumber': page
                        }
                        r = requests.get(uri, params=query)
                        r.raise_for_status()
                        
                        outputs = r.json()
                        items = outputs.get('result', {}).get('results', [])
                        
                        if len(items) == 0:
                            break
        
                        for result in items:
                            writer.writerow([noun, result.get('ui'), result.get('name'), result.get('rootSource')])
                except Exception as e:
                    print(f"Error processing {term}: {e}")
if __name__ == '__main__':
    main()
            
    
        