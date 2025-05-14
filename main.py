import time
from data_fetcher import buscar_partidas_ao_vivo, buscar_partidas_pre_jogo
from rules import avaliar_ao_vivo, avaliar_pre_jogo
from alerts import enviar_alerta_ao_vivo, enviar_alerta_pre_jogo

def executar_bot():
    print("🚀 Iniciando análise de partidas com dados reais...")
    while True:
        try:
            print("\n🔎 Analisando PRÉ-JOGO:")
            pre_jogo = buscar_partidas_pre_jogo()
            if not pre_jogo:
                print("Nenhuma partida pré-jogo encontrada.")
            for partida in pre_jogo:
                print(f"➡️ {partida['jogador1']} vs {partida['jogador2']} - 1º Saque: {partida['primeiro_saque']}%, BP: {partida['bp_convertidos']}%, TMAP: {partida['diferenca_tmap']}")
                if avaliar_pre_jogo(partida):
                    print("✅ Enviando alerta pré-jogo")
                    enviar_alerta_pre_jogo(partida)
                else:
                    print("❌ Não atende os critérios pré-jogo")

            print("\n🎾 Analisando AO VIVO:")
            ao_vivo = buscar_partidas_ao_vivo()
            if not ao_vivo:
                print("Nenhuma partida ao vivo encontrada.")
            for partida in ao_vivo:
                print(f"➡️ {partida['jogador1']} vs {partida['jogador2']} - Placar: {partida['pontuacao']}, 1º Saque: {partida['primeiro_saque']}%, TMAP: {partida['diferenca_tmap']}")
                if avaliar_ao_vivo(partida):
                    print("✅ Enviando alerta ao vivo")
                    enviar_alerta_ao_vivo(partida)
                else:
                    print("❌ Não atende os critérios ao vivo")

        except Exception as e:
            print("Erro:", e)

        time.sleep(90)

if __name__ == "__main__":
    executar_bot()
