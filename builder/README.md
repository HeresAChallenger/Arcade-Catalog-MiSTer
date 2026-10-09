# Arcade Catalog Builder 0.3 — anos canônicos

Esta revisão muda a regra do catálogo **Por Ano**: o `<year>` do MRA deixa de ser autoridade.

## Fonte canônica

O builder usa o `mameNNNNlx.zip` oficial publicado pelo MAME em cada release. Esse arquivo é a saída completa de `-listxml` e contém `setname`, descrição, ano e fabricante. A associação é feita pelo `<setname>` do MRA.

Prioridade:

1. override editorial explícito do Arcade Catalog;
2. política `Sem ano aplicável` para BIOS/multigame;
3. MAME oficial por `setname`;
4. `<year>` do MRA apenas se o set não existir no MAME;
5. `Ano desconhecido`.

O MAME aceita anos estimados como `1993?`. O builder usa a pasta `1993`, mas marca `confidence=estimated` no relatório para auditoria.

## Saídas

- `arcade_years.tsv`: base consumida pelo runtime do MiSTer;
- `arcade_year_audit.tsv`: divergências e fallbacks para revisão;
- `year_coverage.txt`: cobertura resumida.

## Multigames e BIOS

Entradas de infraestrutura não são colocadas em um ano histórico apenas porque o arquivo foi criado recentemente. `DECO Multigame (Darksoft v17)`, por exemplo, vai para **Sem ano aplicável**, e não 2022.

## Automação

O workflow baixa automaticamente o XML oficial da versão mais recente do MAME usando `gh release download`. Assim, novas versões do MAME não exigem alteração do script do MiSTer.

A etapa de coleta dos MRAs públicos permanece separada. Isso permite atualizar a base no GitHub e entregar ao MiSTer apenas um TSV compacto e validado.

## MisterZine

Nenhum dado ou código do catálogo MisterZine é usado. A arquitetura de atualização automática foi inspirada no projeto **MisterZine by Matija Erceg**, crédito conceitual mantido por cortesia.
