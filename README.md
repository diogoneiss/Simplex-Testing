# Simplex 2 fases dual

Desenvolvido por Diogo Neiss para a disciplina de Pesquisa Operacional

Existem dois testes: unitários e end-to-end. O end-to-end compara se você tem a saída correta, comparando com o scipy, ao ler um arquivo.

## Como usar os testes end-to-end

Eu fiz data driven testing, então você precisa garantir que um arquivo out.txt tenha  saída do seu código do main.py com o formato e conteúdo que o professor pediu, vou comparar ele com o scipy.

Pode ser testado rodando simplexTest.py

## Como usar os testes unitários

Eu fiz testes automáticos para várias entradas exemplo e disponibilizei dentro de /tests , junto com a saída esperada em cada etapa do teste, em arquivos .data

Basicamente você tem duas opções, eu recomendo a primeira

1. Usar os mesmos nomes de função que eu e rodar os testes, como qualquer pessoa sensata e preguiçosa faria, e tudo funciona automático

2. Usar as mesmas entradas de teste e fazer as asserções de cada etapa dentro do seu código, seja hard-coded ou com leitura e parse dos arquivos que eu criei. Isso não só parece mal feito e errado como é mal feito e errado, mas quero te dar essa opção, caso opte por não usar código modularizado e coeso.

### Primeira Opção

Instale digite pytest e tudo vai se testar automático.

Crie as funções com as assinaturas que eu usei, como listado no arquivo base.py

TODOS os testes vão dar erro, afinal você não tem todas as funções funcionando. Você pode escolher fazer Test-Driven-Development e deixar os erros "se resolverem" enquanto programa ou testar só no final, sua escolha. O melhor jeito de fazer TDD é "pulando" os testes de função que você ainda não implementou, reduzindo os skips gradativamente.


### Segunda Opção

Nessa opção você não usará os scripts de teste que eu fiz.

Uma asserção seria, por exemplo, testar se a função soma, com 1 + 2, é == 3. Se for igual a asserção passa, se for diferente ela reporta que falhou com esse caso. Bem mais prático que print's e if elses durante o código.

Se você tem uma função que lê, cria tableau e monta vero, você colocará a asserção do teste manualmente (o que é uma prática não recomendada) dentro de cada etapa, ou seja, passe os mesmos valores que eu usei. Então se quer testar, por exemplo, uma entrada C = 1 3 6, você faz a asserção se o vetor C tem esses valores, depois se o tableu tem o - C | 0, depois se o tableu é | Vero | - C | 0 , tudo com os valores de teste que eu usei. Existe um código exemplo para o que eu exemplifiquei acima aqui.



## Especificação

Resolve equações na forma max c^t * x , sujeito a Ax <= B, com x >= 0

Parte teorica disponivel em:

Abaixo temos as etapas do simplex, todas possuem um teste associado.

### Primeira fase

1. Leitura da entrada (vetor C e matriz de restricoes)
2. Criação de tableau basico e variaveis de folga (auxiliares) para colocar em A' x = b
3. Adição do VERO
4. Execução da PL auxiliar para achar base trivial
5. Verificar se valor objetivo < 0, emitir certificado de inviabilidade com o VERO
6. Verificar presença de variaveis sinteticas na base, pivotar até elas não estarem mais na base, (Livro do Thie 3a ed, pagina 102 explica isso)
7. Verificar se existe B < 0. Se sim, executar simplex dual (terceira fase), senão iniciar segunda fase

### Segunda fase

1. Procurar primeiro Ci < 0
2. i se torna a coluna pivo
3. Procurar linha pivo, ou seja, calcular j tal que Aij > 0 e minimiza a razao (Bi / Aij) para todo j
4. Verificar se existe alguma coluna i tal que Ai e Ci sejam > 0. Se ocorrer, emitir certificado de ilimitado
5. Manipular todas as linhas, de modo que o pivo seja 1 e que tenham apenas 0's acima e abaixo dele nas demais linhas
6. Repetir até b>=0 e C <= 0 (C no tableu é negativo!!!), sabemos que é ótimo
7. Emitir certificado e valor do ótimo

### Terceira fase (Dual)

1. Encontrar linha j com B negativo
2. Encontrar entrada i negativa que minimize -(Ci / Aij) e Ci >= 0
3. Pivotear igual no simplex
4. Se b>=0 e C <= 0 (C no tableu é negativo!!!), sabemos que é otimo

## Emissão de certificados

Se você usar o VERO, é trivial encontrar os certificados. Você precisará descobrir se é ilimitado, inviável ou ótimo.
