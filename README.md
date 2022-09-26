# Simplex 2 fases dual

Desenvolvido por Diogo Neiss e Carlos Magalhães para a disciplina de Pesquisa Operacional

[Ver relatório de testes de unidade](https://htmlpreview.github.io/?https://github.com/diogoneiss/Simplex-Testing/blob/master/report.html) 


*Como testar?*

1. Baixar dependencias do arquivo `requirements.txt`, com `pip install -r .\requirements.txt` ou `python -m pip install -r .\requirements.txt`
2. Digite `pytest` na linha de comando, após baixar os requirements, que ele encontrará todos os testes automáticos.

**Modo verboso**: Use `pytest -v`

**Modo reduzido, quieto**: Use `pytest -q`



Existem dois testes: unitários e end-to-end. O end-to-end compara se você tem a saída correta, comparando com o scipy, ao ler um arquivo.

## Como usar os testes end-to-end

Eu fiz data driven testing, então você precisa garantir que um arquivo out.txt tenha saída do seu código do main.py com o formato e conteúdo que o professor pediu, vou comparar ele com o scipy.

Pode ser testado rodando simplexTest.py

## Como usar os testes unitários/integração

Eu fiz testes automáticos para várias entradas exemplo e disponibilizei dentro de /tests , junto com a saída esperada em cada etapa do teste, em arquivos .data

Basicamente você tem duas opções, eu recomendo a primeira. A terceira é *extremamente* desencorajada

1. Adaptar os mesmos nomes de função para ficar parecido e rodar os testes conforme as instruções, como qualquer pessoa sensata e preguiçosa faria, e tudo funciona automático. Talvez você queira adaptar ignorar um ou outro teste, basta colocar um `@pytest.mark.skip(reason="digite aqui seu motivo")` e ele será ignorado
2. Criar atributos numa classe `Simplex`, como eu fiz no template, e rodar apenas os testes de integração, através do comando `pytest <ainda nao implementei`, que usará apenas os testes de integração, mockando entrada e lendo as saídas/atributos. É **obrigatório** retornar o objeto da classe simplex, já que sem ele não dá pra ver se os objetos parciais estão no formato que eu quero.
3. Ler na mão e fazer as asserções de cada etapa dentro do seu código, seja hard-coded ou com leitura e parse dos arquivos que eu criei. Isso não só parece mal feito e errado como é mal feito e errado, mas quero te dar essa opção, caso opte por não usar código modularizado e coeso.

### Primeira Opção

Siga as instruções do começo, digite pytest e tudo vai se testar automático.

Crie as funções com as assinaturas que eu usei, como listado no arquivo base.py

TODOS os testes vão dar erro, afinal você não tem todas as funções funcionando. Você pode escolher fazer Test-Driven-Development e deixar os erros "se resolverem" enquanto programa ou testar só no final, sua escolha. O melhor jeito de fazer TDD é "pulando" os testes de função que você ainda não implementou, reduzindo os skips gradativamente, com uns `pass` seletivos.

### Segunda Opção

Nessa opção você não usará os scripts de teste unitário que eu fiz, apenas conferirá os atributos parciais

Durante a execução seu objeto Simplex deve possuir os seguintes atributos, que podem ser conferidos no arquivo `simplexObjectTemplate.py`

1. N
2. M
3. Vetor C, lido da entrada
4. Matriz AB, lida da entrada
5. Tableau básico
6. Tableau com VERO
7. PL auxiliar base
8. Segunda fase, com a base trivial presente e as variaveis sintéticas da PL removidas 
9. Segunda fase em forma canônica
10. Tipo de PL, com os valores podendo ser "otima", "inviavel", "ilimitada"
11. Certificado
12. Valor objetivo encontrado no momento que encontrou o certificado

Exemplo:
Se você tem uma função que lê, cria tableau e monta vero, você salvará o valor da variável contendo esse vero criado dentro do respectivo atributo, para que ao final da execução ele tenha a sua matriz dentro.

O que vou fazer é conferir cada valor desse com o esperado para a sua entrada e ver se bate. ATENTE-SE para seguir as convenções usadas em sala

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

## Entrada

A primeira linha da entrada contem dois inteiros m e n, o número de restrições e variáveis.
A segunda linha contem m inteiros, ci , que foram vetor de custo.
Cada uma das n linhas seguintes contém m + 1 inteiros que representam as restrições. Para a i-ésima linha, os m primeiros números são Ai,1, Ai,2,...,Ai,m enquanto o último é Bi
