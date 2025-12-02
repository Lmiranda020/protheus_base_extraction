# 🤖 Automação de Centro de Custos e Consumo

## 📋 Sobre o Projeto

Sistema de automação desenvolvido para otimizar o processo de extração e geração de relatórios de **Centro de Custos** e **Consumo** do sistema corporativo da empresa.

### 👨‍💻 Desenvolvedor
**Larissa Miranda**

---

## ❌ Problemas Identificados

Antes da implementação desta automação, o processo manual apresentava diversos gargalos operacionais:

### 1. **Lentidão no Salvamento**
- Cada relatório demorava vários minutos para ser gerado e salvo manualmente
- Processo repetitivo que consumia horas de trabalho produtivo da equipe
- Necessidade de acompanhamento constante durante a execução

### 2. **Falta de Padronização**
- Nomenclatura inconsistente dos arquivos salvos
- Diferentes colaboradores utilizavam padrões distintos de nomenclatura
- Dificuldade em localizar relatórios específicos posteriormente

### 3. **Desorganização de Pastas**
- Arquivos salvos em locais diversos sem estrutura definida
- Ausência de hierarquia clara de diretórios
- Perda de tempo procurando documentos em múltiplas pastas
- Mistura de relatórios de diferentes naturezas

### 4. **Erros Humanos**
- Esquecimento de salvar determinados relatórios
- Erros de digitação em nomes de arquivos
- Inconsistência nos períodos de competência selecionados
- Possibilidade de extrair apenas um tipo de relatório e esquecer o outro

---

## ✅ Solução Implementada

Esta automação resolve todos os problemas mencionados através de:

- **Execução automática** de todo o fluxo de geração de relatórios
- **Extração integrada** de Centro de Custos e Consumo em uma única execução
- **Padronização rigorosa** de nomenclatura e estrutura de pastas
- **Velocidade otimizada** com processamento em lote
- **Rastreabilidade** com logs detalhados de execução

---

## 🚀 Funcionalidades

### Principais Recursos

1. **Cálculo Automático de Competência**
   - Identifica automaticamente o período anterior ao atual
   - Garante que os relatórios sejam sempre do mês correto

2. **Conexão VPN Automatizada**
   - Estabelece conexão segura com a rede corporativa
   - Prerequisito para acesso ao sistema

3. **Login Automatizado**
   - Credenciais gerenciadas de forma segura via variáveis de ambiente
   - Login automático no sistema corporativo

4. **Habilitação do App Agent**
   - Ativa módulos necessários para execução
   - Configura ambiente adequadamente

5. **Processamento de Consumo**
   - Executa a rotina de extração de dados de consumo
   - Salva arquivos com nomenclatura padronizada
   - Organiza documentos em estrutura de pastas definida

6. **Processamento de Centro de Custos**
   - Executa a rotina de extração de dados de centro de custos
   - Salva arquivos com nomenclatura padronizada
   - Organiza documentos em estrutura de pastas definida

7. **Logout e Finalização Seguros**
   - Encerra sessão adequadamente
   - Fecha aplicações abertas
   - Limpa recursos utilizados

---

## 💻 Tecnologias Utilizadas

- **Python 3.x** - Linguagem principal
- **PyAutoGUI** - Automação de interface gráfica
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **Reconhecimento de imagens** - Para interação com elementos visuais

---

## ⏰ Agendamento Automático

A automação foi configurada para execução automática através do **Agendador de Tarefas do Windows**, programada para rodar em um dia específico do mês.

### Arquitetura de Execução

Para garantir a execução completa sem interrupções:

1. **Arquivo BAT** - Script batch que inicia a automação Python
2. **Agendador de Tarefas** - Executa o arquivo BAT no momento programado

Essa abordagem evita que o Agendador de Tarefas encerre a automação prematuramente em caso de processos mais demorados, garantindo que toda a rotina seja concluída adequadamente.

---

## 📊 Benefícios Mensurados

### Ganhos Operacionais

- ⏱️ **Redução de 80% no tempo** de processamento
- 📁 **100% de padronização** em nomenclatura de arquivos
- ✅ **Zero erros** de digitação ou esquecimento
- 🔄 **Extração integrada** de Centro de Custos e Consumo em única execução
- 🔍 **Facilidade na busca** de relatórios históricos
- 👥 **Liberação de tempo** da equipe para atividades estratégicas

---

**Última atualização**: Dezembro 2025
