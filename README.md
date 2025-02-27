Scraping Diário Oficial da União (DOU) - Automação com Python e Selenium

Sobre o Projeto

Este projeto automatiza a coleta de publicações do Diário Oficial da União (DOU), extraindo dados diretamente do site IN.gov.br usando Python, Selenium e Pandas.

A automação permite acessar todas as seções do DOU (Seção 1, Seção 2 e Seção 3), coletando todos os links de publicações disponíveis e extraindo os conteúdos de forma estruturada para análise posterior.

Os dados são salvos em arquivos Excel (.xlsx) para fácil manipulação e análise.

Funcionalidades

Coleta automática de publicações do DOU para um período específico.

Extração de links de todas as publicações disponíveis.

Navegação automática por todas as páginas do DOU.

Armazenamento dos dados em arquivos Excel.

Recuperação de conteúdo completo das publicações.

Verificação de conexão com a internet e retoma o processo automaticamente após uma falha.

Agendamento para execução diária.

Como Funciona

O script acessa o site do DOU, navegando pelas seções 1, 2 e 3.

Percorre todas as páginas disponíveis, garantindo que todas as publicações sejam coletadas.

Extrai os links de todas as publicações e os armazena temporariamente.

Acessa cada link individualmente, capturando o conteúdo completo da publicação.

Organiza os dados em um formato estruturado:

Ano da publicação

Data da publicação

Título da publicação

URL da publicação

Conteúdo textual completo

Salva os dados no PostgreSQL ou em arquivos Excel, conforme configurado.

Tecnologias Utilizadas

Python - Linguagem principal para automação

Selenium - Para navegação automática e scraping

Pandas - Para manipulação e estruturação dos dados

PostgreSQL - Banco de dados para armazenar os registros

Excel (.xlsx) - Alternativa de armazenamento local dos dados

WebDriverManager - Gerenciamento do ChromeDriver

Configuração e Execução

1. Instale as dependências

pip install -r requirements.txt


2. Execute o script

python scraping_dou.py

Isso iniciará a extração e processamento automático dos dados.

Estrutura do Projeto

📂 Scraping_DOU/
│── 📜 scraping_dou.py        # Código principal
│── 📜 requirements.txt       # Dependências
│── 📜 README.txt             # Documentação do projeto




Contato

Para dúvidas ou sugestões, abra uma issue no repositório do GitHub! 🚀
