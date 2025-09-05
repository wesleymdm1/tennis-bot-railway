# Tennis Bot

Bot do Telegram que consulta a Tennis API (RapidAPI) para exibir
estatísticas de jogadores separadas por tipo de piso.

## Configuração

Defina as seguintes variáveis de ambiente antes de executar:

```bash
export TELEGRAM_TOKEN="seu_token"
export API_KEY="sua_chave_rapidapi"
export API_HOST="tennis-api-atp-wta-itf.p.rapidapi.com"
```

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

Execute o bot:

```bash
python main.py
```

No Telegram, envie uma mensagem com quatro linhas:

```
05/09
16:10
Novak Djokovic
Carlos Alcaraz
```

O bot retornará as estatísticas de vitórias/derrotas de cada jogador por
piso (hard, clay, etc.).

## Observações

- Os nomes dos jogadores são pesquisados via endpoint `/tennis/v2/search`.
- Apenas as estatísticas disponíveis na API serão exibidas.
- Caso algum jogador não seja encontrado, será exibida mensagem de dados
indisponíveis.
