## Para recriar o ambiente virtual a partir de requirements.txt

### 1. Cria um novo ambiente virtual

#### MAC/Linux:
```console
python3 -m venv venv
```
#### Windows:
```console
python -m venv venv
```

### 2. Ativa o ambiente virtual

#### MAC/Linux:
```console
source venv/bin/activate
```
#### Windows:
```console
venv\Scripts\activate
```


### 3. Instala as dependências a partir do ```requirements.txt```
```console
pip install -r requirements.txt
```

### Para sair do ambiente virtual
```console
deactivate
```

### Documentação da biblioteca wordcloud
```
https://amueller.github.io/word_cloud/
```
