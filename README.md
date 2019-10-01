---
description: 'i-City-Tax - simplifica a consulta de Impostos.'
---

# i-City-Tax (Consulta de Impostos Simplificada)

Frontend e API Feita com Django 2.2 e python 3.7 que simplifica a consulta dos impostos dos produtos comercializados no Brasil através do Estado de Origem, Estado de Destino e código NCM do Produto. 

A API responde na porta 32122 e segue um estilo de arquitetura REST.

Há rotas para listar, filtrar, cadastrar e remover as alíqutotas do nosso cadastro, porém as consultas não são públicas. Para realizar as consultas é necessário ter um token de acesso ao sistema:
```js
{
    token: Tonken CSRF
    fk_state_origin: String
    fk_state_destiny: String
    ncm_code: String
}
```
Utilizar o método POST.
Exemplo:
```json
{
    "token": "dkhfdhhjdhfdhf89789789dsfsdnklancsacsah345435n32knç0-",
    "country": "55",
    "state": "SP",
    "ncm_code": "04022130",
}
```

Para todas as consultas o país e o estado de origem está contido no token de autenticação que identifica o cliente da i-City
Com exceção da documentação todas as rotas deve possuir um header com o token de acesso:
```json
{
    "headers": [{"authorization": "token dkjfksfdfy37462301232-012dixnhsx8qx32137n73893fdewhehdw"}]
}
```

As rotas são as seguintes:

3. **POST** /apis/taxes *- Traz o imposto de um determinado produto*

```json
{
    "message": "OK",
    "category": "4 / LEITE E LACTICÍNIOS; OVOS DE AVES; MEL NATURAL; PRODUTOS COMESTÍVEIS DE ORIGEM ANIMAL, NÃO ESPECIFICADOS NEM COMPREENDIDOS NOUTROS CAPÍTULOS",
    "product_NCM": "CREME DE LEITE,MAT.GORD.SUP.1,5%, S/AÇÚCAR",
    "unit": "KG / QUILOGRAMA",
    "from": "Alcindo Schleder - Brasil/RS",
    "to": "Brasil / RS",
    "product_ncm": "04022130",
    "taxes": [
        {
            "type_tax": "ICMS",
            "tax": 18.0
        }
    ]
}
```

5. **POST** /api/taxes/create Content-Type: application/json *- cadastra uma nova ferramenta*

O corpo da requisição deve conter as informações da ferramenta a ser cadastrada, sem o ID (gerado automaticamente pelo servidor). 

```json
{
    "title": "swagger",
    "link": "<https://swagger.io/>",
    "description": "Swagger tools takes the hard work out of generating and maintaining your API docs, ensuring your documentation stays up-to-date as your API evolves.",
    "tags":["node", "organizing", "documentation", "interactive", "developer", "https", "tests"]
}
```

A resposta, em caso de sucesso, é o mesmo objeto, com seu novo ID gerado.

```json
{
    "id": 5,
    "title": "swagger",
    "link": "<https://swagger.io/>",
    "description": "Swagger tools takes the hard work out of generating and maintaining your API docs, ensuring your documentation stays up-to-date as your API evolves.",
    "tags":["node", "organizing", "documentation", "interactive", "developer", "https", "tests"]
}
```

6. **DELETE** /api/taxes/:id *- remove uma ferramenta através de seu ID*

```json
{}
```

7. **PATCH** /api/taxes/:id Content-Type: application/json *- atualiza informações de uma ferramenta*

O corpo da requisição deve conter as informações da ferramenta a ser atualizada (id é ignorado)

```json
{
    "id": 5,
    "title": "Swagger Tools",
    "tags":["node", "design", "documentation", "interactive", "developer", "tests"]
}
```

A resposta, em caso de sucesso, é o mesmo objeto, com as informações atualizadas.

```json
{
    "id": 5,
    "title": "Swagger Tools",
    "link": "<https://swagger.io/>",
    "description": "Swagger tools takes the hard work out of generating and maintaining your API docs, ensuring your documentation stays up-to-date as your API evolves.",
    "tags":["node", "design", "documentation", "interactive", "developer", "tests"]
}
```

## Configuração e uso

### Instalação dos programas necessários (sem docker)

Para instalar este aplicativo localmente em uma máquina devemos ter previamente instalados
alguns pacotes no seu SO, que são:

1. *Python:* versão 3.6 ou maior;
2. *Postgresql:* versão 10.0 ou maior;
3. *Ferramentas auxiliares:* Após os passos 1 e 2 atualizar e instalar as ferramentas do requiriments.txt do python:
  - pip3 (gerenciador de pacotes python);
  - virtualenv (gerenciador de máquinas virtuais pyhton)  
  - pacotes auxiliares que estão contido no arquivo requeriments.txt

```bash
cd ~
mkdir icity_tax
cd icity_tax
python3 -m venv venv
source ./venv/bin/activate
pip install --update pip
```

### Instalação da aplicação

```bash
git clone https://github.com/AlcindoSchleder/icity-tax.git
pip install -r requiriments.txt
```

### Execução local

```bash
python ./manager.py runserver
```

### Testes

```bash
python ./manager.py tests
```
