# Changelog

## 1.2.1 — 2026-10-20

Correção de cobertura e desempenho da linha 1.2.x.

- Varredura recursiva de MRAs em subpastas de `/media/fat/_Arcade`.
- Inclusão dos MRAs encontrados em subpastas nos catálogos Empresa, Placa, Gênero e Ano.
- Exclusão segura de `_alternatives`, `cores` e árvores antigas/derivadas do Arcade Catalog durante a descoberta principal.
- Deduplicação por nome de MRA com prioridade para a raiz de `_Arcade`, depois menor profundidade e, em empate, ordem alfabética.
- Inventário canônico único compartilhado pelas etapas de classificação.
- Correção de restaurações falsas introduzidas durante a otimização dos candidatos 1.2.1.
- Otimização da classificação por Ano: itens inalterados não repetem consultas de destino desnecessárias.
- Otimização da descoberta/validação de grandes árvores de `_Arcade`.
- Tempos detalhados de varredura e processamento para diagnóstico.
- Validação de referência: 23.857 MRAs candidatos, 4.156 MRAs canônicos únicos e atualização ociosa em 48 s no ambiente de desenvolvimento.

## 1.2.0 — 2026-10-17

Primeira versão pública da linha 1.2.x.

- Cinco árvores derivadas: Empresa, Placa, Gênero, Ano e Alternativos.
- Catálogo incremental com detecção de MRAs novos, modificados e removidos.
- Verificação e autorreparo de cópias ausentes nas árvores geradas.
- Fast path para evitar reprocessar Gênero e Ano quando os MRAs não mudaram.
- Correção do verificador do catálogo principal que causava milhares de restaurações falsas.
- Base de anos canônica por `setname`, com fallback local apenas quando necessário.
- Correção validada para DeathSmiles: Master em 2007 e Mega Black Label em 2008.
- Política explícita para itens sem ano aplicável, como BIOS e determinados multigames.
- Atualizações remotas por HTTPS, SHA-256, validação de formato e backup antes da ativação.
- Diagnóstico e exportação de inventário para curadoria.
- Tempo total exibido ao fim de Atualizar/Reconstruir.
- Validação de referência: 1.255 MRAs e atualização ociosa em 6 s no ambiente de desenvolvimento.
