# Arcade Catalog 1.2.0 para MiSTer FPGA

O **Arcade Catalog** organiza automaticamente os MRAs instalados no MiSTer em árvores derivadas, sem alterar o conteúdo oficial de `_Arcade`.

Projeto e curadoria: **Rafael "Riris" Barbosa (@HeresAChallenger)**. Código desenvolvido com auxílio do ChatGPT. A automação foi inspirada pelo **MiSTerZine**, de Matija Erceg. A classificação usa metadados dos próprios MRAs, MiSTer Arcade Database e MAME, conforme o tipo de informação.

## O que ele cria

- `_#Arcade - Por Empresa`
- `_#Arcade - Por Placa`
- `_#Arcade - Por Genero`
- `_#Arcade - Por Ano`
- `_#Arcade - Alternativos` quando os MRAs opcionais selecionados estiverem instalados

As árvores são derivadas. Os MRAs originais permanecem em `/media/fat/_Arcade`.

## Instalação

1. Baixe `Arcade_Catalog_1.2.0.sh`.
2. Copie para `/media/fat/Scripts/` no cartão/armazenamento do MiSTer.
3. Abra **Scripts** no MiSTer e execute `Arcade_Catalog_1.2.0.sh`.
4. Escolha **Atualizar catalogo**. Na primeira instalação, a ausência dos índices locais faz o próprio script executar a reconstrução necessária.

Depois disso, use **Atualizar catalogo** normalmente. O processo é incremental: itens inalterados não são recopiados.

## Atualização online das bases

O script consulta por padrão:

`https://raw.githubusercontent.com/HeresAChallenger/Arcade-Catalog-MiSTer/refs/heads/main/remote/manifest.tsv`

As bases são baixadas por HTTPS, verificadas por **SHA-256**, validadas antes da ativação e recebem backup da versão anterior. Se a rede ou a base remota estiver indisponível, a base local é preservada e o catálogo continua funcionando.

## Por Ano

A versão 1.2.0 usa uma tabela canônica por `setname` antes do fallback local. Isso impede que um valor antigo de snapshot substitua um ano canônico conhecido. Casos sem ano aplicável, como BIOS/containers multigame definidos pela política editorial, ficam fora das pastas cronológicas.

## Desempenho incremental

Na validação de referência em 17/10/2026, com **1.255 MRAs principais**, uma atualização sem alterações terminou em **6 segundos**. Esse número é apenas uma referência; tempo real varia conforme cartão, armazenamento e conjunto instalado.

## Opções úteis

**Atualizar catalogo** aplica mudanças incrementais e verifica bases online. **Verificar novidades** faz a checagem sem reconstruir. **Reconstruir catalogo** recria as árvores derivadas. **Ver relatorio** mostra estado e versões. **Exportar inventario para curadoria** gera material para manutenção das bases. **Gerar pacote de diagnostico** reúne informações para investigar problemas sem modificar jogos.

## Segurança de dados

O Arcade Catalog não precisa apagar ou reescrever os MRAs oficiais para organizar o acervo. A opção de remoção exclui apenas as árvores geradas e seus índices locais. Atualizações remotas são ativadas somente depois de validação de formato e SHA-256.

## Estrutura do repositório

`Arcade_Catalog_1.2.0.sh` é o instalador/runtime público. A pasta `remote/` contém as bases que podem ser atualizadas sem trocar o script. A pasta `builder/` contém ferramentas de geração/auditoria das bases de anos. A pasta `tools/` contém utilitários locais de validação e geração do manifesto remoto.

## Sobre a automação das bases

A versão pública já suporta atualização remota independente do script. A reconstrução automática completa das bases a partir de todos os repositórios upstream depende da configuração exata de fontes do projeto; ela não é necessária para instalar ou usar o 1.2.0 e não foi substituída por URLs presumidas.

## Créditos

- Rafael "Riris" Barbosa (@HeresAChallenger): projeto, conceito, testes e curadoria.
- ChatGPT/OpenAI: auxílio no desenvolvimento e revisão do código.
- Matija Erceg / MiSTerZine: inspiração para a automação e organização de dados.
- Projeto MiSTer FPGA, autores dos cores e mantenedores das distribuições de MRAs.
- MAME e MiSTer Arcade Database: referências de metadados utilizadas na curadoria.

Este projeto não distribui ROMs de jogos.
