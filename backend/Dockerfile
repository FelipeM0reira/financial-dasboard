FROM python:3.11-slim
# Começa com a imagem Python 3.11 (slim = versão leve)

WORKDIR /app
# Cria pasta /app e entra nela (como "cd /app")
# Todas as próximas operações acontecem aqui

RUN apt-get update && apt-get install -y gcc postgresql-client
# apt-get = gerenciador de pacotes do Linux
# Instala gcc (compilador C, precisa para alguns pacotes Python)
# postgresql-client (ferramenta para conectar ao PostgreSQL)
# && = executa os próximos comandos só se o anterior suceder
# rm -rf ... = deleta cache para economizar espaço

COPY requirements.txt .
# Copia requirements.txt do seu PC para /app no container
# Você precisa fazer isso ANTES de instalar, para usar RUN pip install

RUN pip intall --no-cache-dir -r requirements.txt
# pip = gerenciador de pacotes Python (como npm)
# -r requirements.txt = instala TUDO listado no arquivo
# --no-cache-dir = não guarda cache (economiza espaço)

COPY . .
# Copia TODO o código do backend (tudo em ./backend)
# Primeiro . = seu PC (tudo em backend/)
# Segundo . = container (/app)

EXPOSE 8000
# Diz ao Docker que esse container usa porta 8000
# Tipo: "Ei Docker, deixa eu alcançar essa porta lá fora"

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
  → Comando que roda quando container inicia
  → gunicorn = servidor web robusto
  → config.wsgi:application = aponta para seu Django app
  → --bind 0.0.0.0:8000 = escuta em todas as interfaces na porta 8000
  → --workers 4 = 4 processos para processar requisições