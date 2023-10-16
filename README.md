# Problemas a Serem Solucionados

Soluções aproximadas, próximas do pronto global.  
Roteamento de Veículos, Caixeiro viajante, Mochila, Otimização Combinatória.

É um procedimento adapatativoo **auxiliar** que guia o algoritmo na busca local. 

## Meta-Heurísticas

 - Algoritmos Genéticos
 - Simulated Annealing
 - Busca Tabu
 - Ant Colony -> Biology!!! Swarm Operations!!

# Busca Tabu

 - Procedimento Adaptativo Auxiliar
 - É tentado adquirir um resultado próximo ao ótimo global

1. Ponto inicial
1. Iteração contínua para melhor solução na vizinhança
1. A lista permanece salva durante algumas iterações (Ou tempo)
    - Estrutura de memórias para facilitar 
1. É esperado que se encontre um ótimo local muito próximo do ótimo global.

## Heurísticas

1. Utilizar heurísticas de Descida
1. Mover para o melhor vizinho (Facilmente fica preso num ótimo local, Hill Climbing).
1. Criar a lista tabu!
    - Armazenar as últimas T soluções
    - Problemas: Testar se uma solução está ou não na lista Tabu, pelo fato dela ser muito grande pode demorar muito tempo para testar.
    - Para solucionar a ideia é criar uma lista de movimentos reversos.
    - Porém isso traz outro problema, uma lista de movimentos é muito restritiva.

## Critérios de Aceitação do Movimento

Os critérios de busca tem como base a busca de minimização, então devemos manter ciência ao usar os algoritmos de comparação.

- Retirar o **status** Tabu de um movimento sobdeterminadas circunstâncias.
- Aceitar um movimento, mesmo que tabu, se ele melhorar o valor da função objetivo global.
- Explora a cada iteração um subcojunto V da vizinhança N(s) da solução corrente s.
- Os melhores membros de V, pela função de fitness, são escolhidos como a nova soluão corrente, mesmo que a nova seja pior que a anterior.
    - O Motivo de escolher o melhor vizinho é a busca de sair de ótimo local.
    - Só que isso pode gerar ciclos, é aí que a lista de tabus funciona.
- A lista salva os últimos N movimentos em uma lista T. Fila de tamanho fixo, onde ao entrar um o último saí.
- Sendo assim, ao pesquisar na lista dos vizinhos, o vizinho que tiver seu movimento na lista Tabu, deverá sair da consulta.
- Porém com os tabus, a pesquisa pode acabar não indo para outros pontos de interesse, tendo uma busca prematura.
- Para solucionar isso, Há a chamada "Função Aspiração", um mecanismo que ajuda a retirar sob algumas circuntâncias o status tabu de um movimento, para que ele possa ser revisitado.
- Nível de aspiração A(V): uma solução S' em V pode ser gerada se f(S') < A(f(s)), independente se o movimento escolhido dentro de V estiver já na lista de tabu. 
 
Ex: Caso a aspiração seja A(f(s)) = f(s*), sendo "s*" a melhor solução encontrada até então.

## Critério de Parada

- Número Máximo de interações
- Valor da melhor solução chega proximo de um threshold


# Recursos

- https://www.ime.unicamp.br/~sandra/MS915/handouts/BuscaTabu.pdf
