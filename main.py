import logging
from typing import Dict, Optional

from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

from config import TELEGRAM_TOKEN
from data_fetcher import buscar_stats_jogador

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def formatar_stats(nome: str, stats: Optional[Dict[str, Dict[str, int]]]) -> str:
    if not stats:
        return f"{nome}: dados indisponíveis."

    linhas = [f"{nome}"]
    for superficie, info in stats.items():
        wins = info.get("wins", "?")
        losses = info.get("losses", "?")
        linhas.append(f"  • {superficie.title()}: {wins}-{losses}")
    return "\n".join(linhas)


async def partida_handler(update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    linhas = texto.splitlines()
    if len(linhas) != 4:
        await update.message.reply_text(
            "Formato inválido. Envie:\nDATA\nHORA\nJOGADOR1\nJOGADOR2"
        )
        return

    data, hora, jogador1, jogador2 = linhas
    stats1 = buscar_stats_jogador(jogador1)
    stats2 = buscar_stats_jogador(jogador2)

    mensagem = (
        f"📅 {data} ⏰ {hora}\n\n"
        f"{formatar_stats(jogador1, stats1)}\n\n"
        f"{formatar_stats(jogador2, stats2)}"
    )
    await update.message.reply_text(mensagem)


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, partida_handler))
    logger.info("Bot iniciado. Aguardando mensagens...")
    app.run_polling()


if __name__ == "__main__":
    main()

