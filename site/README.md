# Visão geral do código

## Disponível em

ces22exc.pythonanywhere.com 

## Rotas

- `login/`: Permite se identificar com um `username`. Não existe senha, ou seja, o `username` funciona meramente como um `namespace` público

- `logout/`: Desfaz `login`

- `upload/`: Sob `POST`, guarda um arquivo no servidor (enviado pelo cliente). Sob `GET`, renderiza uma `template` para o cliente submeter um arquivo (somente imagens são permitidas)

- `/`: Renderiza uma `template` listando as imagens submetidas pelo usuário corrente, ou redireciona para `login/` caso o usuário não esteja autenticado

## Uso de sessões

Elas mantêm o usuário autenticado durante um tempo, mesmo que ele feche o navegador

## Uso de "cookies"

A template `login.html` tem código em javascript que fixa um cookie nomeado `username` no navegador. Sua utilidade é: caso o usuário tenha feito `logout` ou tenha sua sessão expirada, ele será redirecionado para `login/` caso tente ver suas fotos; neste ponto, o código javascript de `login.html` irá retomar o cookie guardado com `username` e mandará um pedido AJAX para `POST login/`, efetivamente autenticando o usuário e o redirecionando para a página de listagem de fotos. Em outras palavras, o usuário será autenticado automaticamente enquanto tive o cookie no navegador, mesmo que sua sessão (do lado do servidor) expire.

OBS: Esse comportamento automático da página `login.html` só é feito caso o usuário seja redirecionado involuntariamente para a página (por exemplo, quando ele tenta acessar suas fotos sem estar autenticado). Caso ele acesse a página de login manualmente, o código javascript não será executado (a diferenciação é feita por um `?forced=true` na URL da página de login)

## Base de dados

Usa-se `sqlite` como `backend`, manipulada pela ORM `SQLAlchemy`
