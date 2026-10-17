# Changelog

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
