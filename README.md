# Arcade Catalog 1.2.2 para MiSTer FPGA

O **Arcade Catalog** organiza automaticamente os MRAs instalados no MiSTer em árvores derivadas, sem alterar o conteúdo oficial de `_Arcade`.

Projeto e curadoria: **Rafael "Riris" Barbosa (@HeresAChallenger)**. Código desenvolvido com auxílio do ChatGPT/OpenAI. A automação foi inspirada pelo **MiSTerZine**, de Matija Erceg. A classificação utiliza metadados dos próprios MRAs, MiSTer Arcade Database, MAME e CatVer, conforme o tipo de informação.

## O que ele cria

- `_#Arcade - Por Empresa`
- `_#Arcade - Por Placa`
- `_#Arcade - Por Genero`
- `_#Arcade - Por Ano`
- `_#Arcade - Alternativos`

As árvores são derivadas. Os MRAs originais permanecem em `/media/fat/_Arcade`.

O Arcade Catalog utiliza links simbólicos para `cores` nas árvores derivadas para que os MRAs reorganizados continuem encontrando os RBFs instalados em `/media/fat/_Arcade/cores`. Esses links não duplicam os arquivos dos cores.

## Novidades da versão 1.2.2

A versão 1.2.2 consolida a classificação, a normalização das árvores e a curadoria introduzidas na linha 1.2.x.

Entre as principais mudanças:

- catálogo principal validado com **1.564 MRAs**;
- **1.564/1.564** entradas validadas em Empresa, Placa, Gênero e Ano;
- zero MRAs faltantes ou extras nas quatro árvores principais;
- zero links quebrados;
- zero classificações pendentes em Empresa/Placa;
- correções e ampliação da taxonomia de hardware;
- suporte à família **Face LINDA**, incluindo *Magical Cat Adventure* e *Nostradamus*;
- correções de classificação para *Guts n' Glory*, *Escape from the Planet of the Robot Monsters* e *Mille Miglia 2*;
- normalização da família **Williams/Midway Y-Unit**;
- correções na classificação por gênero;
- correção do parser TSV utilizado na curadoria de Alternativos;
- curadoria de Alternativos validada com **162/162 entradas disponíveis**;
- normalização segura de nomes compatíveis com FAT;
- melhorias no diagnóstico e na reconciliação das árvores geradas.

## Descoberta de MRAs

O Arcade Catalog investiga recursivamente `_Arcade`, permitindo que MRAs mantidos em subpastas também entrem nos catálogos de Empresa, Placa, Gênero e Ano.

A descoberta exclui áreas especiais que não pertencem ao catálogo principal, como `_alternatives`, `cores` e árvores antigas ou derivadas do próprio Arcade Catalog.

Quando o mesmo nome de MRA existe em mais de um local, o catálogo escolhe um representante canônico. A prioridade é:

1. MRA diretamente na raiz de `_Arcade`;
2. MRA em subpasta menos profunda;
3. em empate, caminho em ordem alfabética.

Isso evita que coleções espelhadas ou duplicadas multipliquem artificialmente o catálogo.

## Instalação

1. Baixe `Arcade_Catalog_1.2.2.sh`.
2. Copie para `/media/fat/Scripts/` no cartão ou armazenamento do MiSTer.
3. Abra **Scripts** no MiSTer e execute `Arcade_Catalog_1.2.2.sh`.
4. Escolha **Atualizar catalogo**.

Na primeira instalação, a ausência dos índices locais faz o próprio script executar a reconstrução necessária.

Quem já utiliza uma versão anterior da linha 1.2.x pode executar **Atualizar catalogo** normalmente. O processo preserva a lógica incremental e só reconstrói quando realmente necessário.

Usuários da RC12 podem migrar diretamente para a versão final 1.2.2 sem reconstrução completa.

## Atualização online das bases

O script consulta por padrão:

`https://raw.githubusercontent.com/HeresAChallenger/Arcade-Catalog-MiSTer/refs/heads/main/remote/manifest.tsv`

As bases são baixadas por HTTPS, verificadas por **SHA-256**, validadas antes da ativação e recebem backup da versão anterior.

Se a rede ou a base remota estiver indisponível, a base local é preservada e o catálogo continua funcionando normalmente.

O manifesto remoto também informa a versão mínima do Arcade Catalog necessária para utilizar cada conjunto de bases.

## Por Empresa e Por Placa

A classificação combina informações dos MRAs com uma base editorial de fabricantes, famílias de hardware e exceções conhecidas.

A versão 1.2.2 inclui correções de hardware e fabricante identificadas durante a auditoria final, além de uma etapa de reconciliação que remove cópias residuais de classificações antigas sem alterar os MRAs oficiais.

## Por Gênero

A classificação de gêneros utiliza uma combinação de base editorial, CatVer e regras de fallback.

Os nomes das pastas são sanitizados para compatibilidade com FAT, evitando caracteres inválidos ou terminações problemáticas sem alterar os dados originais utilizados internamente.

## Por Ano

A linha 1.2.x utiliza uma tabela canônica por `setname` antes do fallback local. Isso impede que um valor antigo de snapshot substitua um ano canônico conhecido.

Casos sem ano aplicável, como BIOS ou determinados containers multigame definidos pela política editorial, ficam em uma categoria própria em vez de receber um ano artificial.

## Alternativos

O catálogo `_#Arcade - Alternativos` reúne variantes selecionadas e outros MRAs opcionais disponíveis no conjunto instalado.

Na validação final da versão 1.2.2, a curadoria contém:

- **162 entradas selecionadas**;
- **162 disponíveis**;
- **0 ausentes**.

O parser utilizado nessa curadoria preserva corretamente campos vazios do formato TSV e aplica normalização segura aos nomes de pastas.

## Validação de referência da 1.2.2

A versão final foi auditada contra o catálogo efetivamente produzido no MiSTer.

Resultados:

- MRAs principais: **1.564**
- Por Empresa: **1.564/1.564**
- Por Placa: **1.564/1.564**
- Por Gênero: **1.564/1.564**
- Por Ano: **1.564/1.564**
- MRAs faltantes: **0**
- MRAs extras: **0**
- Links quebrados: **0**
- MRAs soltos nas raízes das árvores: **0**
- Classificações pendentes em Empresa/Placa: **0**
- Alternativos curados disponíveis: **162/162**

Os tempos de execução variam conforme cartão, armazenamento, quantidade de subpastas e conjunto de MRAs instalado.

## Opções úteis

**Atualizar catalogo**  
Aplica mudanças incrementais e verifica bases online.

**Verificar novidades**  
Faz a checagem sem reconstruir o catálogo.

**Reconstruir catalogo**  
Recria as árvores derivadas. Deve ser usado apenas quando necessário.

**Ver relatorio**  
Mostra o estado do catálogo e as versões das bases.

**Exportar inventario para curadoria**  
Gera material utilizado na manutenção das bases editoriais.

**Gerar pacote de diagnostico**  
Reúne índices, inventários, informações de duplicidade e estrutura das árvores para investigação de problemas, sem modificar jogos ou MRAs oficiais.

## Segurança de dados

O Arcade Catalog não precisa apagar ou reescrever os MRAs oficiais para organizar o acervo.

A opção de remoção exclui somente:

- as árvores geradas pelo Arcade Catalog;
- os índices locais utilizados pelo próprio script.

ROMs, RBFs e MRAs oficiais permanecem intactos.

Atualizações remotas são ativadas somente depois da validação de formato e SHA-256.

## Estrutura do repositório

`Arcade_Catalog_1.2.2.sh` é o instalador/runtime público.

A pasta `remote/` contém as bases que podem ser atualizadas sem substituir o script principal.

A pasta `builder/` contém ferramentas utilizadas para geração e auditoria das bases.

A pasta `generated/` contém resultados produzidos pelas rotinas de geração automatizada quando aplicável.

A infraestrutura de automação do repositório é mantida separadamente do runtime validado.

## Créditos

- Rafael "Riris" Barbosa (@HeresAChallenger): projeto, conceito, testes e curadoria.
- ChatGPT/OpenAI: auxílio no desenvolvimento, revisão e auditoria do código.
- Matija Erceg / MiSTerZine: inspiração para a automação e organização de dados.
- Projeto MiSTer FPGA, autores dos cores e mantenedores das distribuições de MRAs.
- MAME, CatVer e MiSTer Arcade Database: referências de metadados utilizadas na curadoria.

Este projeto não distribui ROMs de jogos.
