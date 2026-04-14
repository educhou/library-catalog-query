# 📚 Aplicação de Consulta de Catálogo para Bibliotecários

**Sistema web profissional para busca e consulta de informações de livros**

## 🎯 Objetivo

Criar uma ferramenta rápida, intuitiva e profissional para bibliotecários consultarem dados de livros usando ISBN, título ou nome do autor, com integração à base de dados do Open Library.

## 🚀 Como Começar

### Inicio Rápido

```bash
# Opção 1: Script de inicialização (recomendado)
bash start_app.sh

# Opção 2: Comando manual
python app.py
```

Depois, abra seu navegador em: **http://localhost:5000**

### Requisitos Obrigatórios

- Python 3.7 ou superior
- Conexão com Internet
- Um navegador web moderno

### Instalação Completa

```bash
# 1. Instalar dependências Python
pip install -r requirements.txt

# 2. Executar a aplicação
python app.py

# 3. Acessar no navegador
# http://localhost:5000
```

## 💻 Interface e Uso

### Tela Principal

A aplicação possui uma interface limpa com:

- **Campo de Busca**: Digite seu termo de pesquisa
- **Seletor de Tipo**: Escolha como buscar (ISBN, Título ou Autor)
- **Botão Buscar**: Dispara a pesquisa
- **Botão Limpar**: Reseta formulário e resultados
- **Dicas de Uso**: Orientações para cada tipo de busca

### Tipo 1: Busca por ISBN

**Quando usar**: Quando você tem o código ISBN da obra

**Como fazer**:
1. Selecione "ISBN" no menu
2. Digite o código (com ou sem hífens)
3. Clique em "Buscar"

**Exemplos válidos**:
```
978-0-596-00712-6     ← Com hífens
9780596007126        ← Sem hífens
978 0 596 007126     ← Com espaços
0596007124          ← ISBN-10
```

**Resultado esperado**: Uma única obra com todos os dados disponíveis

### Tipo 2: Busca por Título

**Quando usar**: Quando você sabe o nome do livro

**Como fazer**:
1. Selecione "Título" no menu
2. Digite o título (completo ou parcial)
3. Clique em "Buscar"

**Exemplos**:
```
Clean Code              → Procura livros com "Clean Code"
Design Patterns        → Procura livros sobre padrões
Harry Potter          → Procura série Harry Potter
The                   → Procura todos os livros começando com "The"
```

**Resultado esperado**: Lista de múltiplos livros e seus dados

### Tipo 3: Busca por Autor

**Quando usar**: Quando você quer encontrar obras de um determinado autor

**Como fazer**:
1. Selecione "Autor" no menu
2. Digite o nome do autor
3. Clique em "Buscar"

**Exemplos**:
```
Robert Martin         → Livros de Robert C. Martin
J.K. Rowling         → Obras de J.K. Rowling  
Stephen King         → Livros de Stephen King
Ada Lovelace         → Obras históricas
```

**Resultado esperado**: Autores encontrados com contagem de obras

## 📊 Campos de Dados Retornados

Para cada livro encontrado, a aplicação exibe:

| Campo | Descrição | Disponibilidade |
|-------|-----------|-----------------|
| **ISBN** | Código Internacional do Livro (ISBN-10 ou 13) | ✅ Sempre |
| **Título** | Nome da obra | ✅ Geralmente |
| **Autor** | Nome(s) do(s) autor(es) | ⚠️ Frequentemente |
| **Editora** | Publicadora/Editora | ✅ Geralmente |
| **Data Publicação** | Ano ou data completa | ✅ Geralmente |
| **Páginas** | Número de páginas | ⚠️ Às vezes |
| **Assunto** | Categorias/Temas (DDC, LCSH) | ⚠️ Varia |
| **Resumo** | Descrição/Abstract da obra | ⚠️ Às vezes |

**Legenda**: ✅ Confiável | ⚠️ Pode não estar disponível | ❌ Não disponível

## 🔧 Recursos Técnicos

### Arquitetura

```
┌─────────────────────────┐
│   Navegador Web         │  ← Interface do Usuário
│   (HTML + CSS + JS)     │
└────────────┬────────────┘
             │ HTTP/JSON
┌────────────▼────────────┐
│   Flask Web Server      │  ← Servidor da Aplicação
│   (Python Backend)      │
└────────────┬────────────┘
             │ HTTP REST API
┌────────────▼────────────┐
│  Open Library API       │  ← Fonte de Dados
│  (Milhões de registros) │
└─────────────────────────┘
```

### API Endpoints

Você pode usar a aplicação programaticamente:

#### 1. Busca Geral
```
GET /api/search?q=TERMO&type=TIPO

Parâmetros:
  q    : Termo de busca (obrigatório)
  type : isbn | title | author (obrigatório)

Exemplos:
  GET /api/search?q=978-0-596-00712-6&type=isbn
  GET /api/search?q=Clean%20Code&type=title
  GET /api/search?q=Robert%20Martin&type=author
```

#### 2. Lookup Direto por ISBN
```
GET /api/lookup-isbn?isbn=ISBN

Parâmetros:
  isbn : Código ISBN (obrigatório)

Exemplo:
  GET /api/lookup-isbn?isbn=978-0-596-00712-6
```

### Validação de ISBN

A aplicação **automaticamente**:
- ✅ Remove hífens e espaços
- ✅ Valida dígitos verificadores (checksum)
- ✅ Corrige erros menores no checksum
- ✅ Aceita ISBN-10 e ISBN-13

## 🎨 Características da Interface

- **Design Responsivo**: Funciona em Desktop, Tablet e Mobile
- **Tema Profissional**: Cores neutras (púrpura e azul)
- **Acessibilidade**: Navegação por teclado, labels descritivos
- **Feedback Visual**: Spinner de carregamento, mensagens de erro claras
- **Otimização**: Carregamento rápido, busca com Enter

## ⚡ Dicas de Uso Profissional

### 1. Busca Mais Precisa
```
❌ Evite: "livro"
✅ Use: "O Código Limpo" ou ISBN
```

### 2. Tratamento de Resultados Vazios
```
Se não encontrar por ISBN:
  → Tente buscar por título
  → Verifique o ISBN está correto
  → Open Library pode não ter o livro
```

### 3. Múltiplos Resultados
```
Ao encontrar vários livros:
  → Compare títulos e autores
  → Verifique ano de publicação
  → Use ISBN para confirmação exata
```

### 4. Campos Ausentes
```
Se algum campo disser "Não disponível":
  → O Open Library não tem essa informação
  → Consulte a obra física ou outro catálogo
  → Mantenha sua base local de dados
```

## 🔍 Exemplos de Uso Completo

### Exemplo 1: Consultar um Livro Específico

**Cenário**: Você quer informações completas sobre o livro "Head First Design Patterns"

**Passos**:
1. Selecione "ISBN"
2. Digita: `978-0-596-00712-6`
3. Clica em "Buscar"

**Resultado**:
```
Título: Head First design patterns
Editora: O'Reilly
Data: 2004
Páginas: 638
Assunto: Computer software -- Development; Java
```

### Exemplo 2: Encontrar Obras de um Autor

**Cenário**: Encontrar quantas obras um autor tem catalogadas

**Passos**:
1. Selecione "Autor"
2. Digita: `Robert Martin`
3. Clica em "Buscar"

**Resultado**:
```
Robert C. Martin - 47 obras catalogadas
```

### Exemplo 3: Explorar Temas

**Cenário**: Encontrar livros sobre um tópico

**Passos**:
1. Selecione "Título"
2. Digita: `Machine Learning`
3. Clica em "Buscar"

**Resultado**:
Lista de ~100 livros sobre Machine Learning

## ⚙️ Configuração Avançada

### Mudar Porta (Padrão: 5000)

```bash
# Editar app.py
# Procure a linha: app.run(...)
# Mude: port=5000 para port=5001
```

### Modo Produção

```bash
# Usar Gunicorn (mais robusto)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### HTTPS/SSL

```bash
# Usar um proxy reverso (nginx/Apache)
# Ou certificado auto-assinado:
pip install pyopenssl
# Configurar em app.py
```

## 🐛 Troubleshooting

### Problema: Porta 5000 já está em uso

**Solução 1**: Encontre e encerre o processo
```bash
lsof -i :5000        # Encontra processo
kill -9 PID          # Encerra
```

**Solução 2**: Use outra porta
```bash
# Editar app.py, mudar port=5000 para port=5001
python app.py
```

### Problema: "ISBN não encontrado"

**Por quê?**
- ISBN digitado incorretamente
- Livro não está no Open Library
- ISBN é inválido

**Solução**:
- Verifique o ISBN no livro físico
- Tente buscar por título ou autor
- Consulte outro catálogo

### Problema: "Nenhum resultado encontrado"

**Por quê?**
- Termo de busca muito genérico ou vago
- Livro não está no Open Library
- Erro de digitação

**Solução**:
- Use termos mais específicos
- Tente em inglês (Open Library é focado em inglês)
- Complete a busca com outra informação

### Problema: Aplicação lenta ou congelada

**Solução**:
- Verifique sua conexão com Internet
- Open Library pode estar lenta
- Tente novamente em alguns minutos
- Reinicie a aplicação

### Problema: Erro 500 (Erro Interno)

**Solução**:
- Verifique o console para detalhes do erro
- Reinicie: `python app.py`
- Atualize dependências: `pip install -r requirements.txt --upgrade`

## 📈 Estatísticas e Monitoramento

### Logs de Requisição

A aplicação exibe no console:
```
127.0.0.1 - - [14/Apr/2026 11:47:06] "GET /api/search?q=...&type=isbn HTTP/1.1" 200 -
```

**Interpretação**:
- `200` = Sucesso
- `404` = Não encontrado
- `500` = Erro do servidor
- `400` = Requisição inválida

## 🔒 Segurança

- ✅ Sem login necessário (biblioteca local)
- ✅ Sem armazenamento de dados sensíveis
- ✅ Apenas leitura (sem alterações na base)
- ✅ Conexão com Open Library é criptografada (HTTPS)

## 📚 Recursos Educacionais

### Documentação Online
- [Open Library API](https://openlibrary.org/api)
- [Flask Documentation](https://flask.palletsprojects.com)
- [HTTP API Basics](https://developer.mozilla.org/en-US/docs/Web/HTTP)

### Formato ISBN
- [ISBN Official](https://www.isbn-international.org)
- [ISBN Checksum Calculator](https://www.isbn-international.org/content/check-digit-algorithm)

## 🚀 Próximos Passos

### Melhorias Potenciais
- [ ] Base de dados local (cache)
- [ ] Exportar resultados (PDF/Excel)
- [ ] Integração com OPAC da biblioteca
- [ ] Leitor de código de barras/QR
- [ ] Sistema de reservas
- [ ] Estatísticas e relatórios

### Integrações Futuras
- [ ] WorldCat para cobertura global
- [ ] Google Books API
- [ ] Catálogo local (banco de dados)
- [ ] Sistema de usuários

## 📞 Suporte

Para problemas ou sugestões:
1. Consulte este guia (seção Troubleshooting)
2. Contate a equipe de TI da biblioteca
3. Verifique status do Open Library

## 📝 Changelog

### Versão 1.0 (Atual)
- ✅ Busca por ISBN, Título, Autor
- ✅ Validação e correção de ISBN
- ✅ Interface responsiva
- ✅ 8 campos de dados
- ✅ API REST endpoints

---

**Desenvolvido para bibliotecários. Por bibliotecários. 📚**

*Última atualização: Abril de 2026*
