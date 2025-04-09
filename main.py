from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import pandas as pd
import matplotlib.pyplot as plt
import io
from typing import List

app = FastAPI()

# Base de dados de usuários
usuarios = [
    {"nome": "João Silva", "localidade": "Copacabana", "telefone": "21987654321"},
    {"nome": "Maria Oliveira", "localidade": "Ipanema", "telefone": "21912345678"},
    {"nome": "Carlos Souza", "localidade": "Leblon", "telefone": "21955556666"},
    {"nome": "Ana Costa", "localidade": "Barra da Tijuca", "telefone": "21999998888"},
    {"nome": "Pedro Santos", "localidade": "Copacabana", "telefone": "21977776666"},
    {"nome": "Lucia Ferreira", "localidade": "Ipanema", "telefone": "21988887777"},
    {"nome": "Marcos Rocha", "localidade": "Tijuca", "telefone": "21966665555"},
    {"nome": "Fernanda Lima", "localidade": "Botafogo", "telefone": "21944443333"},
    {"nome": "Ricardo Alves", "localidade": "Copacabana", "telefone": "21933332222"},
    {"nome": "Juliana Martins", "localidade": "Ipanema", "telefone": "21922221111"},
    {"nome": "Roberto Gomes", "localidade": "Leblon", "telefone": "21911110000"},
    {"nome": "Patricia Dias", "localidade": "Barra da Tijuca", "telefone": "21900009999"},
    {"nome": "Lucas Barbosa", "localidade": "Tijuca", "telefone": "21999990000"},
    {"nome": "Camila Ribeiro", "localidade": "Botafogo", "telefone": "21988881111"},
    {"nome": "Eduardo Pereira", "localidade": "Copacabana", "telefone": "21977772222"},
    {"nome": "Tatiane Castro", "localidade": "Ipanema", "telefone": "21966663333"},
    {"nome": "Gustavo Nunes", "localidade": "Leblon", "telefone": "21955554444"},
    {"nome": "Vanessa Cardoso", "localidade": "Barra da Tijuca", "telefone": "21944445555"},
    {"nome": "Felipe Torres", "localidade": "Tijuca", "telefone": "21933336666"},
    {"nome": "Amanda Freitas", "localidade": "Botafogo", "telefone": "21922227777"}
]


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <body>
            <h1>API de Usuários RJ</h1>
            <p>Endpoints disponíveis:</p>
            <ul>
                <li><a href="/usuarios">/usuarios</a> - Todos os usuários</li>
                <li><a href="/usuarios/Copacabana">/usuarios/{localidade}</a> - Filtrar por localidade</li>
                <li><a href="/buscar?nome=João">/buscar?nome={nome}</a> - Buscar por nome</li>
                <li><a href="/histograma">/histograma</a> - Gráfico de distribuição</li>
            </ul>
        </body>
    </html>
    """


@app.get("/usuarios", response_class=JSONResponse)
async def listar_usuarios():
    return usuarios


@app.get("/usuarios/{localidade}", response_class=JSONResponse)
async def filtrar_por_localidade(localidade: str):
    return [user for user in usuarios if user["localidade"].lower() == localidade.lower()]


@app.get("/buscar", response_class=JSONResponse)
async def buscar_por_nome(nome: str):
    return [user for user in usuarios if nome.lower() in user["nome"].lower()]


@app.get("/histograma")
async def gerar_histograma():
    df = pd.DataFrame(usuarios)
    contagem = df['localidade'].value_counts()

    plt.figure(figsize=(10, 6))
    contagem.plot(kind='bar', color='skyblue')
    plt.title('Distribuição de Usuários por Localidade')
    plt.xlabel('Localidade')
    plt.ylabel('Quantidade')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return Response(content=buf.getvalue(), media_type="image/png")