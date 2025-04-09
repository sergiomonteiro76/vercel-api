from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict

app = FastAPI()

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de dados de usuários (otimizada como tuplas)
usuarios = [
    ("João Silva", "Copacabana", "21987654321"),
    ("Maria Oliveira", "Ipanema", "21912345678"),
    ("Carlos Souza", "Leblon", "21955556666"),
    ("Ana Costa", "Barra da Tijuca", "21999998888"),
    ("Pedro Santos", "Copacabana", "21977776666"),
    ("Lucia Ferreira", "Ipanema", "21988887777"),
    ("Marcos Rocha", "Tijuca", "21966665555"),
    ("Fernanda Lima", "Botafogo", "21944443333"),
    ("Ricardo Alves", "Copacabana", "21933332222"),
    ("Juliana Martins", "Ipanema", "21922221111"),
    ("Roberto Gomes", "Leblon", "21911110000"),
    ("Patricia Dias", "Barra da Tijuca", "21900009999"),
    ("Lucas Barbosa", "Tijuca", "21999990000"),
    ("Camila Ribeiro", "Botafogo", "21988881111"),
    ("Eduardo Pereira", "Copacabana", "21977772222"),
    ("Tatiane Castro", "Ipanema", "21966663333"),
    ("Gustavo Nunes", "Leblon", "21955554444"),
    ("Vanessa Cardoso", "Barra da Tijuca", "21944445555"),
    ("Felipe Torres", "Tijuca", "21933336666"),
    ("Amanda Freitas", "Botafogo", "21922227777")
]

# Cache para contagem de localidades
contagem_localidades = None

def atualizar_cache():
    global contagem_localidades
    contagem = defaultdict(int)
    for _, localidade, _ in usuarios:
        contagem[localidade] += 1
    contagem_localidades = dict(contagem)

# Atualiza cache na inicialização
atualizar_cache()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>API de Usuários RJ</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #2c3e50; }
                ul { list-style-type: none; padding: 0; }
                li { margin: 8px 0; }
                a { color: #3498db; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>API de Usuários RJ</h1>
            <p>Backend funcionando. Acesse o frontend em:</p>
            <a href="/frontend.html">Frontend Completo</a>
            <p>Endpoints disponíveis:</p>
            <ul>
                <li><a href="/usuarios">/usuarios</a> - Todos os usuários</li>
                <li><a href="/localidade/Ipanema">/localidade/{nome}</a> - Filtrar por localidade</li>
                <li><a href="/buscar?nome=João">/buscar?nome={nome}</a> - Buscar por nome</li>
                <li><a href="/histograma-data">/histograma-data</a> - Dados para gráfico (JSON)</li>
            </ul>
        </body>
    </html>
    """

@app.get("/usuarios", response_class=JSONResponse)
async def listar_usuarios():
    return [{"nome": nome, "localidade": loc, "telefone": tel} for nome, loc, tel in usuarios]

@app.get("/localidade/{local}", response_class=JSONResponse)
async def filtrar_localidade(local: str):
    local_lower = local.lower()
    return [{"nome": nome, "localidade": loc, "telefone": tel}
            for nome, loc, tel in usuarios if loc.lower() == local_lower]

@app.get("/buscar", response_class=JSONResponse)
async def buscar_por_nome(nome: str):
    nome_lower = nome.lower()
    return [{"nome": nome, "localidade": loc, "telefone": tel}
            for nome, loc, tel in usuarios if nome_lower in nome.lower()]

@app.get("/histograma-data", response_class=JSONResponse)
async def histograma_data():
    return contagem_localidades

# Se precisar adicionar/remover usuários dinamicamente:
def adicionar_usuario(nome: str, localidade: str, telefone: str):
    usuarios.append((nome, localidade, telefone))
    atualizar_cache()

def remover_usuario(nome: str):
    global usuarios
    usuarios = [user for user in usuarios if user[0] != nome]
    atualizar_cache()