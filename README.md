# Témoignages

Parce qu'on :heart: générer des trucs depuis de spreadsheets.

[Spreadsheets Sample](https://docs.google.com/spreadsheets/d/1ETB640Yx0MX8VSdYQ9KZArrOAzz1Z-fwhp9Pqpy3z6c/edit?usp=sharing)

## Installation / Utilisation

- Install :

```bash
$ pip install -r requirements.txt
```
```bash
$ npm install -g less
```

- Run, publier le spreadsheets sur le web puis :

```bash
$ python3 do.py [build|watch] (<sheet-id>|<file.json>)
```

- Pour importer des tweets, il faut un fichier de configuration `twitter.json` :

```json
{
  "api_key": "<api-key>",
  "api_secret": "<api-secret>"
}
```

## Mise en ligne
1. Compléter les meta-tags en remplaçant l'url dans `./dist/index.html`
2. Décommenter et compléter les tracking-tags dans `./dist/index.html`
3. Ajouter une image d'appel dans `./dist/social.jpg`
4. Eventuelement ajuster les styles dans `./dist/style.css`
5. Uploader sur le ftp le contenu du dossier `./dist/`


## License

> The MIT License (MIT)
>
> Copyright (c) Libé Six Plus 2015
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without > limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following > conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO > EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR > THE USE OR OTHER DEALINGS IN THE SOFTWARE.
