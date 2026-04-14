import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime


def _html_tabela_filiais(filiais: list, cor_badge: str, emoji: str) -> str:
    if not filiais:
        return "<p style='color:#666;margin:0'>Nenhuma</p>"
    itens = "".join(
        f"<span style='display:inline-block;background:{cor_badge};color:#fff;"
        f"border-radius:4px;padding:2px 8px;margin:2px;font-size:13px'>"
        f"{emoji} {f}</span>"
        for f in filiais
    )
    return f"<div style='line-height:2'>{itens}</div>"


def _montar_html(resumo: dict) -> str:
    """Monta o corpo do e-mail em HTML com visual profissional."""
    tipo       = resumo["tipo"]
    competencia = resumo["competencia"]
    inicio     = resumo["inicio"]
    fim        = resumo["fim"]
    total      = resumo["total"]
    n_ok       = resumo["sucesso"]
    n_err      = resumo["erros"]
    ok_lst     = resumo["filiais_ok"]
    err_lst    = resumo["filiais_err"]

    status_geral = "CONCLUÍDA COM SUCESSO ✅" if n_err == 0 else "CONCLUÍDA COM ERROS ⚠️"
    cor_status   = "#2e7d32" if n_err == 0 else "#b71c1c"
    pct_ok       = round(n_ok / total * 100) if total else 0

    barra_ok  = f"<div style='width:{pct_ok}%;background:#43a047;height:100%;border-radius:4px'></div>"
    barra_err = f"<div style='width:{100-pct_ok}%;background:#e53935;height:100%;'></div>"

    tab_ok  = _html_tabela_filiais(ok_lst,  "#43a047", "✅")
    tab_err = _html_tabela_filiais(err_lst, "#e53935", "❌")

    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;background:#f4f6f8;padding:0;margin:0">
  <table width="100%" cellpadding="0" cellspacing="0"
         style="background:#f4f6f8;padding:30px 0">
    <tr><td align="center">
      <table width="620" cellpadding="0" cellspacing="0"
             style="background:#fff;border-radius:8px;
                    box-shadow:0 2px 8px rgba(0,0,0,.12);overflow:hidden">

        <!-- Cabeçalho -->
        <tr>
          <td style="background:#1F4E79;padding:24px 32px">
            <h1 style="color:#fff;margin:0;font-size:22px">
              🤖 Extração automática de {tipo}
            </h1>
            <p style="color:#a8c8e8;margin:6px 0 0;font-size:14px">
              Relatório automático de execução
            </p>
          </td>
        </tr>

        <!-- Status geral -->
        <tr>
          <td style="padding:20px 32px 0">
            <div style="border-left:5px solid {cor_status};
                        background:#fafafa;padding:14px 18px;border-radius:4px">
              <p style="margin:0;font-size:18px;font-weight:bold;color:{cor_status}">
                {status_geral}
              </p>
              <p style="margin:4px 0 0;color:#555;font-size:13px">
                Competência: <strong>{competencia}</strong>
              </p>
            </div>
          </td>
        </tr>

        <!-- Métricas -->
        <tr>
          <td style="padding:20px 32px 0">
            <table width="100%" cellspacing="8" cellpadding="0">
              <tr>
                <td width="25%" align="center"
                    style="background:#e3f2fd;border-radius:6px;padding:16px">
                  <div style="font-size:28px;font-weight:bold;color:#1565c0">{total}</div>
                  <div style="font-size:12px;color:#555;margin-top:4px">Total de Filiais</div>
                </td>
                <td width="5%"></td>
                <td width="25%" align="center"
                    style="background:#e8f5e9;border-radius:6px;padding:16px">
                  <div style="font-size:28px;font-weight:bold;color:#2e7d32">{n_ok}</div>
                  <div style="font-size:12px;color:#555;margin-top:4px">Processadas OK</div>
                </td>
                <td width="5%"></td>
                <td width="25%" align="center"
                    style="background:#ffebee;border-radius:6px;padding:16px">
                  <div style="font-size:28px;font-weight:bold;color:#c62828">{n_err}</div>
                  <div style="font-size:12px;color:#555;margin-top:4px">Com Erro</div>
                </td>
                <td width="5%"></td>
                <td width="25%" align="center"
                    style="background:#f3e5f5;border-radius:6px;padding:16px">
                  <div style="font-size:28px;font-weight:bold;color:#6a1b9a">{pct_ok}%</div>
                  <div style="font-size:12px;color:#555;margin-top:4px">Taxa de Sucesso</div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Barra de progresso -->
        <tr>
          <td style="padding:16px 32px 0">
            <div style="height:10px;background:#eee;border-radius:4px;overflow:hidden;
                        display:flex">
              {barra_ok}{barra_err}
            </div>
          </td>
        </tr>

        <!-- Período -->
        <tr>
          <td style="padding:20px 32px 0">
            <table width="100%" style="background:#f9f9f9;border-radius:6px;
                                       border:1px solid #e0e0e0">
              <tr>
                <td style="padding:12px 16px;font-size:13px;color:#333">
                  🕐 <strong>Início:</strong> {inicio}
                </td>
                <td style="padding:12px 16px;font-size:13px;color:#333">
                  🕑 <strong>Fim:</strong> {fim}
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Filiais OK -->
        <tr>
          <td style="padding:20px 32px 0">
            <h3 style="margin:0 0 8px;color:#2e7d32;font-size:14px">
              ✅ FILIAIS PROCESSADAS COM SUCESSO ({n_ok})
            </h3>
            <div style="border:1px solid #c8e6c9;background:#f1f8f1;
                        border-radius:6px;padding:12px">
              {tab_ok}
            </div>
          </td>
        </tr>

        <!-- Filiais com erro -->
        <tr>
          <td style="padding:16px 32px 0">
            <h3 style="margin:0 0 8px;color:#c62828;font-size:14px">
              ❌ FILIAIS COM ERRO ({n_err})
            </h3>
            <div style="border:1px solid #ffcdd2;background:#fff8f8;
                        border-radius:6px;padding:12px">
              {tab_err}
            </div>
          </td>
        </tr>

        <!-- Rodapé -->
        <tr>
          <td style="padding:24px 32px;border-top:1px solid #e0e0e0;margin-top:20px">
            <p style="margin:0;font-size:12px;color:#999;text-align:center">
              📎 O log completo está anexado neste e-mail.<br>
              Este é um e-mail automático — não responda.
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
"""


def enviar_email_resultado(resumo: dict) -> bool:
    """
    Envia e-mail com o resultado da automação via Gmail (App Password).

    Args:
        resumo: dicionário retornado por LogExecucao.finalizar_execucao()

    Returns:
        True se enviado com sucesso, False caso contrário.
    """
    remetente    = os.getenv("GMAIL_REMETENTE")
    app_senha    = os.getenv("GMAIL_APP_SENHA")
    destinatario = os.getenv("EMAIL_DESTINATARIO", "")

    if not all([remetente, app_senha, destinatario]):
        print("⚠️  Variáveis de e-mail não configuradas no .env "
              "(GMAIL_REMETENTE, GMAIL_APP_SENHA, EMAIL_DESTINATARIO)")
        return False

    destinatarios = [d.strip() for d in destinatario.split(",") if d.strip()]

    tipo        = resumo["tipo"]
    n_err       = resumo["erros"]
    competencia = resumo["competencia"]
    status_subj = "✅ Sucesso" if n_err == 0 else f"⚠️ {n_err} erro(s)"
    assunto     = f"Extração automática {tipo} — {competencia} — {status_subj}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = assunto
    msg["From"]    = remetente
    msg["To"]      = ", ".join(destinatarios)

    # Corpo HTML
    msg.attach(MIMEText(_montar_html(resumo), "html", "utf-8"))

    # Anexar o log Excel se existir
    caminho_log = resumo.get("caminho_log", "")
    if caminho_log and os.path.exists(caminho_log):
        try:
            with open(caminho_log, "rb") as f:
                parte = MIMEBase("application",
                                 "vnd.openxmlformats-officedocument"
                                 ".spreadsheetml.sheet")
                parte.set_payload(f.read())
            encoders.encode_base64(parte)
            nome_anexo = os.path.basename(caminho_log)
            parte.add_header("Content-Disposition",
                             f'attachment; filename="{nome_anexo}"')
            msg.attach(parte)
            print(f"📎 Anexo adicionado: {nome_anexo}")
        except Exception as e:
            print(f"⚠️  Erro ao anexar log: {e}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remetente, app_senha)
            servidor.sendmail(remetente, destinatarios, msg.as_string())
        print(f"📧 E-mail enviado para: {', '.join(destinatarios)}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("❌ Falha de autenticação SMTP. Verifique GMAIL_APP_SENHA no .env.")
    except smtplib.SMTPException as e:
        print(f"❌ Erro SMTP ao enviar e-mail: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado ao enviar e-mail: {e}")
    return False