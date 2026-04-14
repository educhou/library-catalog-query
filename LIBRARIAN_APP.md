# Aplicação de Consulta de Catálogo para Bibliotecários

Uma aplicação web profissional para bibliotecários buscarem e consultarem informações de livros de forma rápida e eficiente.

## Recursos

✅ **Busca por ISBN** - Procure livros pelo código ISBN (10 ou 13 dígitos)  
✅ **Busca por Título** - Encontre livros pelo título completo ou parcial  
✅ **Busca por Autor** - Localize obras por nome do autor  
✅ **Validação de ISBN** - Auto-correção de dígitos verificadores  
✅ **Interface Profissional** - Design otimizado para bibliotecários  
✅ **Integração Open Library** - Acesso a milhões de registros de livros  

## Requisitos

- Python 3.7+
- Flask
- Conexão com Internet (para integração com Open Library)

## Instalação

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a aplicação

```bash
python app.py
```

A aplicação estará disponível em: **http://localhost:5000**

## Uso da Aplicação

### Busca por ISBN
1. Selecione "ISBN" no menu de tipo de busca
2. Digite o ISBN (com ou sem hífens)
3. Clique em "Buscar"

**Exemplos válidos:**
- `978-0-596-00712-6`
- `9780596007126`
- `0-596-00712-0` (ISBN-10)

### Busca por Título
1. Selecione "Título" no menu
2. Digite o título completo ou parcial
3. Clique em "Buscar"

**Exemplos:**
- `Clean Code`
- `Design Patterns`
- `Harry Potter`

### Busca por Autor
1. Selecione "Autor" no menu
2. Digite o nome do autor
3. Clique em "Buscar"

**Exemplos:**
- `Robert Martin`
- `J.K. Rowling`
- `Gang of Four`

## Dados Retornados

A aplicação retorna os seguintes campos para cada livro:

| Campo | Descrição |
|-------|-----------|
| **ISBN** | Código internacional do livro |
| **Título** | Nome da obra |
| **Autor** | Nome do(s) autor(es) |
| **Editora** | Editora/Publicadora |
| **Data Publicação** | Quando o livro foi publicado |
| **Páginas** | Número de páginas (quando disponível) |
| **Assunto** | Temas/Categorias (Deewey, etc) |
| **Resumo** | Descrição/Abstract do livro |

## API Endpoints

### GET /api/search
Busca por ISBN, título ou autor

**Parâmetros:**
- `q` (required): Termo de busca
- `type` (required): isbn, title, ou author

**Exemplo:**
```
GET /api/search?q=Clean%20Code&type=title
```

### GET /api/lookup-isbn
Busca direta por ISBN

**Parâmetros:**
- `isbn` (required): ISBN do livro

**Exemplo:**
```
GET /api/lookup-isbn?isbn=978-0-596-00712-6
```

## Recursos Técnicos

- **Framework**: Flask
- **Fonte de Dados**: Open Library API
- **Frontend**: HTML5 + CSS3 + JavaScript vanilla
- **Tipo**: Aplicação web responsiva
- **Autenticação**: Não requerida

## Características da Interface

- ✅ Design responsivo (funciona em Desktop e Mobile)
- ✅ Busca em tempo real
- ✅ Validação de formulário
- ✅ Tratamento de erros
- ✅ Carregamento visual (spinner)
- ✅ Cards de resultado com destaque
- ✅ Dicas de uso integradas
- ✅ Tema visual profissional (púrpura/azul)

## Limitações e Notas

1. **Location (Localização)**: Não está disponível na API do Open Library. Seria necessário integração com catálogos locais para esta informação.

2. **Autor em Busca por ISBN**: Nem todos os registros no Open Library têm informação de autor estruturada.

3. **Taxa de Limite**: Open Library permite ~2000 requisições/hora por IP.

4. **Dados Offline**: A aplicação requer conexão com Internet para funcionar.

## Desenvolvimento Futuro

- [ ] Integração com catálogo local (SQLite)
- [ ] Cache de buscas frequentes
- [ ] Exportar resultados (PDF, CSV, Excel)
- [ ] Sistema de ranking de resultados
- [ ] Integração com WorldCat
- [ ] Dashboard de estatísticas
- [ ] Sistema de usuários e favoritos
- [ ] QR Code para leitura de ISBN
- [ ] Reserva de livros
- [ ] Sincronização com OPAC da biblioteca

## Troubleshooting

### Porta 5000 já está em uso
```bash
python app.py --port 5001
```

### Erro de conexão com Open Library
- Verifique sua conexão com Internet
- Tente novamente em alguns momentos
- Open Library pode estar temporariamente indisponível

### ISBN não encontrado
- Verifique se o ISBN está correto
- Nem todos os livros estão no Open Library
- Tente buscar por título ou autor

## Contato e Suporte

Para bugs ou sugestões, contate a equipe de TI da biblioteca.

## Licença

Desenvolvido para uso interno da biblioteca.
