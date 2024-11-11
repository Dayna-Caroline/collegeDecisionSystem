# Projeto de Tomada de Decisão - Faculdade

Este projeto é um sistema de apoio à tomada de decisão para determinar o melhor município e os melhores cursos em diferentes mesorregiões do Estado de São Paulo para abrir uma nova unidade de faculdade.

## Dependências

Este projeto utiliza as seguintes bibliotecas:

### Backend (Arquivo `backend.py`):

- `pandas` - Para manipulação de dados.
- `folium` - Para geração de mapas interativos.
- `opencage` - Para geocodificação de coordenadas geográficas.
- `requests` - Para fazer requisições HTTP.
- `python-dotenv` - Para carregar variáveis de ambiente de um arquivo `.env`.

### Frontend (Arquivo `index.py`):

- `dash` - Framework para construção de interfaces web interativas.
- `dash-bootstrap-components` - Para usar componentes do Bootstrap no Dash.

### Pré-requisitos

1. **Python 3.7+**: O projeto foi desenvolvido e testado com Python 3.7 e versões superiores.
2. **Chave da API do OpenCage**: Você precisará de uma chave de API para utilizar o geocodificador do OpenCage. Você pode obter sua chave [aqui](https://opencagedata.com/).
3. **Arquivo `.env`**: O projeto usa o arquivo `.env` para armazenar variáveis sensíveis, como a chave da API. Certifique-se de criar esse arquivo na raiz do projeto e incluir sua chave API da seguinte forma:
   ```env
   API_KEY=sua_chave_api
   ```

## Como Executar

### 1. Instale as dependências

Crie um ambiente virtual e instale as dependências listadas no `requirements.txt`.

```bash
python -m venv venv
source venv/bin/activate  # No Windows, use: venv\Scripts\activate
pip install -r requirements.txt
```

Caso não encontre o `requirements.txt`, faça a instalação utilizando

```bash
pip install pandas folium opencage requests python-dotenv dash dash-bootstrap-components
```

### 3. Execute o projeto (inicie o servidor)

O Dash iniciará o servidor localmente em http://127.0.0.1:8050/. Você pode acessar a aplicação web diretamente no seu navegador. Execute o comando abaixo.

```bash
python index.py
```
