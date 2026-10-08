from datetime import datetime
from modules.clicar_imagem import clicar_imagem

# Tempo máximo para esperar um botão aparecer. O clicar_imagem clica assim que
# encontra a imagem, então um valor alto só "custa" tempo quando o sistema está lento.
TIMEOUT_PADRAO = 60


class EtapaFalhou(Exception):
    """
    Uma etapa da automação não pôde ser concluída (ex.: botão não apareceu na tela).

    Args:
        mensagem: descrição do erro (vai para o log)
        tentar_novamente: False quando repetir a filial não faz sentido
                          (ex.: o arquivo já foi baixado e só o rename falhou)
    """

    def __init__(self, mensagem, tentar_novamente=True):
        super().__init__(mensagem)
        self.tentar_novamente = tentar_novamente


def etapa(imagem, descricao, msg_erro, confidence=0.8, timeout=TIMEOUT_PADRAO):
    """Clica na imagem ou lança EtapaFalhou com a mensagem informada."""
    if not clicar_imagem(imagem, confidence=confidence, timeout=timeout, descricao=descricao):
        raise EtapaFalhou(msg_erro)


def registrar_filiais_com_erro(log, filiais, mensagem):
    """Registra a mesma falha para várias filiais (ex.: quando nem foi possível abrir o relatório)."""
    if not log:
        return
    for filial in filiais:
        log.registrar_filial(filial, sucesso=False, mensagem=mensagem,
                             inicio_filial=datetime.now())


def processar_filiais(filiais, processar_filial, voltar_tela_inicial, log=None, tentativas=3):
    """
    Executa processar_filial(filial) para cada filial. Se uma etapa falhar, volta
    para a tela inicial do relatório e tenta a mesma filial de novo (até `tentativas`
    vezes). Se ainda assim falhar, registra o erro e segue para a próxima filial.

    No log fica só o resultado final de cada filial, para o resumo do e-mail
    continuar com uma linha por filial.

    Args:
        filiais: lista de códigos de filial
        processar_filial: função(filial) -> mensagem de sucesso; lança EtapaFalhou em caso de erro
        voltar_tela_inicial: função() -> bool; deixa a tela pronta para começar uma filial
        log: instância de LogExecucao (opcional)
        tentativas: número máximo de tentativas por filial

    Returns:
        True se percorreu todas as filiais, False se precisou interromper
        (não conseguiu voltar para a tela inicial).
    """
    for indice, filial in enumerate(filiais):
        inicio_filial = datetime.now()
        erros = []

        print(f"\n{'='*60}")
        print(f"🏢 Processando filial: {filial}")
        print(f"{'='*60}\n")

        for tentativa in range(1, tentativas + 1):
            try:
                mensagem = processar_filial(filial)
                if erros:
                    mensagem += f" (na {tentativa}ª tentativa; antes: {' | '.join(erros)})"
                print(f"✅ Filial {filial} processada com sucesso!")
                if log:
                    log.registrar_filial(filial, sucesso=True, mensagem=mensagem,
                                         inicio_filial=inicio_filial)
                break

            except EtapaFalhou as e:
                erros.append(str(e))
                print(f"❌ Filial {filial} — tentativa {tentativa}/{tentativas}: {e}")

                ultima_tentativa = tentativa == tentativas or not e.tentar_novamente

                print("↩️  Voltando para a tela inicial do relatório...")
                if not voltar_tela_inicial():
                    msg = "Não foi possível voltar para a tela inicial do relatório"
                    print(f"🛑 {msg}. Interrompendo a automação.")
                    if log:
                        log.registrar_filial(filial, sucesso=False,
                                             mensagem=f"{' | '.join(erros)} | {msg}",
                                             inicio_filial=inicio_filial)
                    registrar_filiais_com_erro(log, filiais[indice + 1:],
                                               f"Não processada: {msg}")
                    return False

                if ultima_tentativa:
                    msg = (f"Falhou após {tentativa} tentativa(s): {' | '.join(erros)}"
                           if tentativa > 1 else erros[0])
                    if log:
                        log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                             inicio_filial=inicio_filial)
                    break

                print(f"🔁 Tentando a filial {filial} novamente...")

    return True
