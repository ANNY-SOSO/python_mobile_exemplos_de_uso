# 10a Desafio 2 Digitação (Aqui) ❌ 🎉 ⚠️ 🛍️ 🔄
import flet as ft
def main(page: ft.Page):
    # Configuraçoes inicias da página
    page.title = "Loja Virtual Mini"
    page.padding = ft.padding.only(top=40, left=20, bottom=20)
    page.scroll = ft.ScrollMode.AUTO # Permite rolagem automática
    page.bgcolor = ft.Colors.GREY_50   # Cor de fundo da página

    # Estado de aplicação - variáveis que armazenam dados do carrinho
    carrinho = []  # Lista que armazena os produtos no carrinho
    total_carrinho = 0.0  # Valor total dos produtos no carrinho

    # Elementos da interface (declarados primeiro para serem acessíveis nas funções)
    # Grid exibe os produtos em formato de grade
    area_produtos = ft.GridView(
        expand=1,  # Expande para ocupar espaço disponível
        runs_count=2,  # 2 colunas de produtos
        max_extent=180,  # Largura máxima de cada item
        child_aspect_ratio=0.9,  # Promorção altura/largura dos cards
        spacing=15,  # Espaçamento entre cards horizontalmente
        run_spacing=15 # Espaçamento entre cards verticalmente
    )
    # Textos que mostram informações do carrinho
    contador_carrinho = ft.Text("Carrinho (0)", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
    total_texto = ft.Text("Total: R$ 0,00", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
    # Lista que exibe os itens do carrinho
    lista_carrinho = ft.ListView(height=150, spacing=5)

    # Texto para exibir notificações ao usuário
    notificacao = ft.Text("", size=14, color=ft.Colors.BLUE_600, text_align=ft.TextAlign.CENTER)

    def adicionar_ao_carrinho(nome, preco):
        """Adiciona um produto ao carrinho de compras"""
        nonlocal total_carrinho # Permite modificar a variável global total_carrinho
        # Adiciona o produto como dicionário na lista do carrinho
        carrinho.append({"nome": nome, "preco":preco})
        # Soma o preço do produto ao total
        total_carrinho += preco
        # Atualiza a interface do carrinho
        atualizar_carrinho()
        # Mostra notificação de sucesso
        mostrar_notificacao(f"✅ {nome} adicionado!")

    def criar_card_produto(nome, preco, categoria, emoji, cor):
        """Cria um card de produto reutilizável que funciona como botão"""
        return ft.Container(
            content=ft.Column([
                # Emoji do produto
                ft.Text(emoji, size=40, text_align=ft.TextAlign.CENTER),
                # Nome do produto
                ft.Text(
                    nome,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                    max_lines=2, # Permite quebra de linha para nomes longos
                    overflow=ft.TextOverflow.ELLIPSIS  # Adiciona ... se muito longo
                ),
                # Preço do produto
                ft.Text(
                    f"R$ {preco:.2f}",
                    size=14,
                    color=ft.Colors.WHITE70,
                    text_align=ft.TextAlign.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10  # Espaçamento entre elementos da coluna
            ),
        bgcolor=cor, # Cor de fundo específica do produto
        padding=20, # Espaçamento interno
        border_radius=15,  # Bordas arredondadas
        width=160,  # Largura fixa do card
        height=180,   # Altura fixa do card
        # Sombra para dar profundidade
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK)
        ),
        # Tornando o card interno clicável - chama função de adicionar ao carrinho
        on_click=lambda e, n=nome, p=preco: adicionar_ao_carrinho(n, p),
        # Efeito visual de ondulação ao clicar (ripple effect)
        ink=True,
        # Animação suave para transições
        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        )
    
    # Lista de produtos disponíveis na loja
    # Cada produto é um dicionário com informações como nome, preço, categoria, emoji e cor
    produtos = [
        {"nome": "Smartphone", "preco": 899.99, "categoria": "Eletrônicos", "emoji": "📱", "cor":ft.Colors.BLUE_600},
        {"nome": "Notebook", "preco": 2499.90, "categoria": "Eletrônicos", "emoji": "💻", "cor":ft.Colors.PURPLE_600},
        {"nome": "Tênis", "preco": 299.99, "categoria": "Roupas", "emoji": "👟", "cor":ft.Colors.GREEN_600},
        {"nome": "Camiseta", "preco": 89.90, "categoria": "Roupas", "emoji": "👕", "cor":ft.Colors.ORANGE_600},
        {"nome": "Livro", "preco": 45.00, "categoria": "Educação", "emoji": "📚", "cor":ft.Colors.BROWN_600},
        {"nome": "Fone", "preco": 199.99, "categoria": "Eletrônicos", "emoji": "🎧", "cor":ft.Colors.RED_600},
        {"nome": "Relógio", "preco": 350.00, "categoria": "Acessórios", "emoji": "⌚", "cor":ft.Colors.TEAL_600},
        {"nome": "Óculos", "preco": 250.00, "categoria": "Acessórios", "emoji": "🕶️", "cor":ft.Colors.INDIGO_600},
    ]
    


    # Elementos de filtro de interface
    # Dropdown para filtrar por categoria
    filtro_categoria = ft.Dropdown(
        label="Categoria",
        width=150,
        value="Todas",
        options=[
            ft.dropdown.Option("Todas"),
            ft.dropdown.Option("Eletrônicos"),
            ft.dropdown.Option("Roupas"),
            ft.dropdown.Option("Educação"),
            ft.dropdown.Option("Acessórios")
        ]
    )

    # Dropdown para filtrar por faixa de preço
    filtro_preco = ft.Dropdown(
        label="Preço",
        width=150,
        value="Todos",
        options=[
            ft.dropdown.Option("Todas"),
            ft.dropdown.Option("Até R$ 100"),
            ft.dropdown.Option("R$ 100-500"),
            ft.dropdown.Option("Acima R$ 500")
        ]
    )

    # Campo de texto para buscar produtos por nome
    campo_busca = ft.TextField(
        label="Buscar produto",
        width=200,
        prefix_icon=ft.Icons.SEARCH
    )

    def remover_do_carrinho(index):
        """Remove um poduto específico do carrinho usado seu índice"""
        nonlocal total_carrinho

        if 0 <= index <len(carrinho):

            produto = carrinho.pop(index)

            total_carrinho -= produto["preco"]

            atualizar_carrinho()

            mostrar_notificacao(f"❌ {produto['nome']} removido!")

    def atualizar_carrinho():
        """Atualiza a exibição do carrinho na interface"""

        contador_carrinho.value = f"Carrinho ({len(carrinho)})"

        total_texto.value = f"Total: R$ {total_carrinho:.2f}"


        lista_carrinho.controls.clear()


        for i, item in enumerate(carrinho):

            linha_produto = ft.Row([

                ft.Text(f"{item['nome']}", expand=True),

                ft.Text(f"R$ {item['preco']:.2f}", color=ft.Colors.GREEN_600),

                ft.IconButton(
                    ft.Icons.DELETE,
                    icon_color=ft.Colors.RED,
                    on_click=lambda e, idx=i: remover_do_carrinho(idx)
                )
            ], spacing=10)


            lista_carrinho.controls.append(linha_produto)

        # Atualizar a página para refletir as mudanças
        page.update()
    
    def carregar_produtos(e=None):
        """Carrega e exibe produos aplicando os filtros selecionados"""

        area_produtos.controls.clear()


        categoria = filtro_categoria.value
        preco_faixa = filtro_preco.value
        busca = (campo_busca.value or "").lower()


        for produto in produtos:
            # aplica filtro de categoria
            if categoria != "Todas" and produto["categoria"] != categoria:
                continue

            # Aplica filtro de preço
            if preco_faixa == "Até R$ 100" and produto["preco"] > 100:
                continue
            elif preco_faixa == "R$ 100-500" and not (100 <= produto["preco"] <= 500):
                continue
            elif preco_faixa == "Acima R$ 500" and produto["preco"] <= 500:
                continue

            # Aplica filtro de busca por nome
            if busca and busca not in produto["nome"].lower():
                continue

            # Se chegou ate aqui, o produto por todos os filtros
            # Cria o card do produto
            card = criar_card_produto(
                produto["nome"],
                produto["preco"],
                produto["categoria"],
                produto["emoji"],
                produto["cor"]
            )

            area_produtos.controls.append(card)

        
        page.update()

    def finalizar_compra(e):
        """Finaliza a compra - limpa o carrinho e zera o total"""
        nonlocal total_carrinho # Permite modificar a variável global
        if len(carrinho) > 0:

            carrinho.clear()

            total_carrinho = 0.0

            atualizar_carrinho()

            mostrar_notificacao("⚠️ Carrinho vazio!")

    def limpar_filtros(e):
        """Limpa todos os filtros e redefine para valores padrão"""

        filtro_categoria.value = "Todas"
        filtro_preco.value = "Todos"
        campo_busca.value = ""


        carregar_produtos()


        mostrar_notificacao("🔄 Filtros limpos!")

    def mostrar_notificacao(mensagem):
        """Exibe uma mensagem de notifcação para o usuário"""
        notificacao.value = mensagem
        page.update()
    


    for controle in [filtro_categoria, filtro_preco, campo_busca]:
        controle.on_change = carregar_produtos
    

    carregar_produtos()

    
    page.add(
        ft.Column([

            ft.Text(
                "🛍️ Loja Virtual Mini",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_800,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                "Encontre os melhores produtos!",
                size=14,
                color=ft.Colors.GREY_600,
                text_align=ft.TextAlign.CENTER
            ),

            ft.Row(
                [filtro_categoria, filtro_preco],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),



            ft.Row([
                campo_busca,
                ft.ElevatedButton(
                    "🔄 Limpar Filtros",
                    on_click=limpar_filtros,
                    bgcolor=ft.Colors.ORANGE_400,
                    color=ft.Colors.WHITE,
                    height=40,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=12, weight=ft.FontWeight.BOLD)
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15
            ),


            ft.Container(
                content=area_produtos,
                height=400,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=10,
                padding=10
            ),

            # Seção do carrinho de comprars 
            ft.Container(
                content=ft.Column([

                    ft.Row(
                        [contador_carrinho, total_texto],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    lista_carrinho,

                    ft.Row([
                        ft.ElevatedButton(
                            "🛒 Finalizar Compra",
                            on_click=finalizar_compra,
                            bgcolor=ft.Colors.GREEN,
                            color=ft.Colors.WHITE,
                            width=200
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    notificacao
                ], spacing=10),
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=10,

                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=3,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)
                )
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
        )
    )

ft.app(target=main)
    