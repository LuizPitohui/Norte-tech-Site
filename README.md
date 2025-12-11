# Norte-tech-Site# Norte Tech - Portal Corporativo

Este é o repositório oficial do portal web da **Norte Tech**, desenvolvido para gerenciar a presença digital da empresa, portfólio de serviços, notícias e processos seletivos.

O sistema foi construído utilizando **Django 6.0** e **Python 3.14**, com foco em uma arquitetura modular e escalável.

## 🚀 Funcionalidades Principais

### 1. Institucional (`core`)
* **Home Dinâmica:** Banner de vídeo (Hero), Destaques e Últimas Notícias.
* **Gestão de Conteúdo:** Textos institucionais ("Quem Somos", Missão, Visão, Valores) editáveis via Painel Administrativo.
* **Notícias:** Sistema completo de postagens com slug automático e editor de conteúdo.
* **Fale Conosco:** Formulário de contato que salva leads no banco de dados.

### 2. Portfólio de Serviços (`services`)
* Listagem de serviços categorizados.
* Página de detalhes de cada serviço.
* **API REST:** Endpoint (`/api/v1/servicos/`) para integração externa.

### 3. Área de Carreiras (`careers` & `accounts`)
* **Banco de Talentos:** Cadastro de usuários e currículos.
* **Gestão de Perfil:** Candidatos podem cadastrar Formação, Experiência e Cursos.
* **Vagas:** O RH publica vagas e os candidatos aplicam com um clique.
* **Onboarding:** Sistema para envio de documentos digitalizados (RG, CNH, ASO) com status de aprovação pelo RH.

---

## 🛠 Tecnologias Utilizadas

* **Backend:** Python 3.14, Django 6.0
* **API:** Django REST Framework
* **Banco de Dados:** SQLite (Desenvolvimento)
* **Gerenciamento de Dependências:** Poetry
* **Frontend:** HTML5, CSS3, Bootstrap 5
* **Admin Interface:** Django Jazzmin (Tema personalizado)

---

## ⚙️ Como Rodar o Projeto Localmente

### Pré-requisitos
* Python 3.14+
* [Poetry](https://python-poetry.org/)
### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/norte-tech-portal.git](https://github.com/seu-usuario/norte-tech-portal.git)
    cd norte-tech-portal
    ```

2.  **Instale as dependências:**
    ```bash
    poetry install
    ```

3.  **Ative o ambiente virtual:**
    ```bash
    poetry shell
    ```

4.  **Execute as migrações do banco de dados:**
    ```bash
    python manage.py migrate
    ```

5.  **Crie um superusuário (para acessar o Admin):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Inicie o servidor:**
    ```bash
    python manage.py runserver
    ```

O projeto estará acessível em: `http://127.0.0.1:8000/`

---

## 📂 Estrutura do Projeto

* `nortetech_site/` - Configurações globais do Django (`settings.py`, `urls.py`).
* `core/` - Funcionalidades base (Home, Sobre, Notícias, Contato).
* `services/` - Catálogo de serviços e API.
* `careers/` - Lógica de vagas e candidaturas.
* `accounts/` - Gestão de usuários, autenticação e perfil do candidato.
* `templates/` - Arquivos HTML globais e parciais (Navbar, Footer).
* `static/` & `media/` - Arquivos estáticos (CSS, Imagens, Uploads).

---

## 🔐 Acesso Administrativo

Acesse `http://127.0.0.1:8000/admin/` para gerenciar:
* Configurações da Empresa (Telefone, Redes Sociais, Textos).
* Publicar/Editar Notícias.
* Gerenciar Vagas e ver Candidatos.
* Aprovar/Reprovar documentos.

---

## 👨‍💻 Autor

Desenvolvido por **Luiz Fernando da Silva Guedes**.
*Engenharia da Computação - FUCAPI*