# 
# A Simple Ranking

Extension de requête et ranking. Le ranking prend en compte :

- le pourcentage de matching par document avec un poids moins important pour les stop words
- la longueur des titres : privilégie les titres plus courts
- le nombre d'occurence des mots de la requête (hors stopwords) dans le titre
- la position des mot dans la phrase : privilégie les titres dans le lequel les mots apparaissent dans le même ordre et à une même distance

## Auteur

Francois Wallyn


## Installation des packages

```bash
  pip install -r requirements.txt
```
    
## Usage/Exemples
Pour lancer un exemple de ranking à partir d'un index inversé et d'un ensemble de documents.

```bash
python3 main.py --req="Ma requête" --match_all --path_to_save_json /path/to/directory 
```
Avec les paramètres : 

- `--req` : la requête souhaitée
- `--match_all` : si présent alors les documents filtrés doivent matcher tous les mots de la requête, si absent au moins un mot.
- `--path_to_save_json` directory dans laquelle la requête le fichier result.json sera créé

Le fichier result sont de la forme :

```json
{
    "result" : [
        {
            "url" : "url1",
            "title" : "title1",
            "id" : "idX",
            "score" : 10
        },
        {
            "url" : "url2",
            "title" : "title2",
            "id" : "idY",
            "score" : 8
        },
    ],
    "n_doc_index": 500, 
    "n_doc_after_filtre": 2
}
```

