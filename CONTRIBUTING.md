# Guia de Contribuição

Este documento apresenta as orientações para os integrantes contribuírem
com o projeto de forma organizada utilizando Git e GitHub.

## Organização das branches

Antes de iniciar qualquer alteração, atualize a branch `development`:

```bash
git switch development
git pull origin development
```

Cada integrante deve criar uma branch própria a partir da `development`.

O padrão recomendado é:

```text
feature/nome-da-alteracao
```

Exemplo:

```text
feature/adicionar-documentacao
```

As alterações não devem ser realizadas diretamente nas branches `main`,
`development` ou `release`.

## Commits

Os commits devem ser pequenos, objetivos e descritivos.

Sempre que possível, devem seguir um padrão semântico, como:

```text
feat: adicionar funcionalidade
fix: corrigir erro
docs: atualizar documentação
style: ajustar estilo do projeto
refactor: reorganizar código
chore: realizar configuração
```

Exemplos:

```text
docs: atualizar documentação do projeto
feat: adicionar tela de cadastro
fix: corrigir validação do formulário
```

## Pull Requests

Após concluir uma alteração, o integrante deve enviar sua branch para o
repositório remoto e abrir um Pull Request para a branch `development`.

O fluxo correto é:

```text
feature/nome-da-alteracao → development
```

Antes de criar o Pull Request, é necessário verificar:

- a branch de origem;
- a branch de destino;
- os arquivos alterados;
- a descrição da alteração;
- a existência de conflitos.

## Fluxo de trabalho

O fluxo de contribuição do projeto deve seguir estas etapas:

1. Atualizar a branch `development`.
2. Criar uma branch `feature`.
3. Realizar a alteração na branch `feature`.
4. Criar um commit semântico.
5. Enviar a branch para o repositório remoto.
6. Abrir um Pull Request para `development`.
7. Integrar a branch após a verificação.
8. Atualizar a branch `development` local.

O fluxo geral das branches é:

```text
feature → development → release → main
```

## Integração das branches

Depois que todos os integrantes concluírem suas alterações e realizarem
a integração na branch `development`, a equipe deverá seguir o fluxo:

```text
development → release
release → main
```

A branch `main` representa a versão principal do projeto.

## Boas práticas

- Utilizar nomes claros para as branches.
- Fazer commits pequenos e descritivos.
- Não realizar alterações diretamente na `main`.
- Atualizar a `development` antes de iniciar uma nova tarefa.
- Conferir a origem e o destino antes de realizar um Pull Request.
- Evitar alterar os mesmos arquivos que outros integrantes estão modificando.
- Manter o histórico do projeto organizado.
