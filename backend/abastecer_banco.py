import sqlite3

def abastecer():
    print("⏳ A iniciar o abastecimento TOTAL da Base de Dados NutriCheck...")
    
    conexao = sqlite3.connect('nutricheck.db')
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alimentos (
            codigo_barras TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            ingredientes TEXT,
            alergenicos TEXT,
            imagem_url TEXT
        )
    ''')

    # Catálogo COMPLETO com códigos de barra formato EAN-13 (Brasil: 789...)
    produtos = [
        # ==========================================
        # 🥤 BEBIDAS NÃO ALCOÓLICAS
        # ==========================================
        ('7891000000001', 'Refrigerante Coca-Cola', 'Água gaseificada, açúcar, extrato de noz de cola, cafeína.', '', ''),
        ('7891000000002', 'Refrigerante Pepsi', 'Água gaseificada, açúcar, extrato de cola, cafeína.', '', ''),
        ('7891000000003', 'Refrigerante Guaraná Antarctica', 'Água gaseificada, açúcar, extrato de guaraná.', '', ''),
        ('7891000000004', 'Refrigerante Fanta Laranja', 'Água gaseificada, açúcar, suco de laranja.', '', ''),
        ('7891000000005', 'Refrigerante Sprite', 'Água gaseificada, açúcar, suco de limão.', '', ''),
        ('7891000000006', 'Refrigerante Schweppes Tônica', 'Água gaseificada, açúcar, quinino.', '', ''),
        ('7891000000007', 'Refrigerante Kuat', 'Água gaseificada, açúcar, extrato de guaraná.', '', ''),
        ('7891000000008', 'Refrigerante H2OH', 'Água gaseificada, suco de limão, edulcorantes.', '', ''),
        ('7891000000009', 'Refrigerante Limão Misteriosa', 'Água gaseificada, açúcar, suco de limão.', '', ''),
        ('7891000000010', 'Refrigerante Sukita', 'Água gaseificada, açúcar, suco de laranja.', '', ''),
        ('7891000000011', 'Suco de Laranja Do Bem', 'Suco de laranja integral.', '', ''),
        ('7891000000012', 'Néctar de Pêssego Maguary', 'Água, suco de pêssego, açúcar.', '', ''),
        ('7891000000013', 'Néctar de Goiaba Maguary', 'Água, suco de goiaba, açúcar.', '', ''),
        ('7891000000014', 'Suco Integral de Uva', 'Suco de uva integral.', '', ''),
        ('7891000000015', 'Suco Kapo Caixinha', 'Água, açúcar, suco de frutas.', '', ''),
        ('7891000000016', 'Suco Tang Pó Laranja', 'Açúcar, maltodextrina, polpa de laranja desidratada.', '', ''),
        ('7891000000017', 'Suco Tang Pó Maracujá', 'Açúcar, maltodextrina, polpa de maracujá desidratada.', '', ''),
        ('7891000000018', 'Refresco em Pó Clight', 'Maltodextrina, polpa de fruta, edulcorantes.', '', ''),
        ('7891000000019', 'Água de Coco Sococo', 'Água de coco.', '', ''),
        ('7891000000020', 'Água de Coco Kero Coco', 'Água de coco integral.', '', ''),
        ('7891000000021', 'Água Mineral Crystal sem Gás', 'Água mineral natural.', '', ''),
        ('7891000000022', 'Água Mineral Bonafont sem Gás', 'Água mineral natural.', '', ''),
        ('7891000000023', 'Água Mineral Minalba com Gás', 'Água mineral gaseificada artificialmente.', '', ''),
        ('7891000000024', 'Isotônico Gatorade', 'Água, sacarose, sais minerais.', '', ''),
        ('7891000000025', 'Energético Red Bull', 'Água gaseificada, taurina, cafeína.', '', ''),
        ('7891000000026', 'Energético Monster', 'Água gaseificada, açúcar, extrato de ginseng, taurina.', '', ''),
        ('7891000000027', 'Energético TNT', 'Água gaseificada, taurina, cafeína.', '', ''),

        # ==========================================
        # 🍺 CERVEJAS E BEBIDAS ALCOÓLICAS
        # ==========================================
        ('7892000000001', 'Cerveja Heineken Lata', 'Água, malte e lúpulo.', 'en:gluten', ''),
        ('7892000000002', 'Cerveja Brahma Lata', 'Água, malte, cereais não maltados, lúpulo.', 'en:gluten', ''),
        ('7892000000003', 'Cerveja Skol Lata', 'Água, malte, milho e lúpulo.', 'en:gluten', ''),
        ('7892000000004', 'Cerveja Antarctica Garrafa', 'Água, malte, cereais não maltados, lúpulo.', 'en:gluten', ''),
        ('7892000000005', 'Cerveja Budweiser Long Neck', 'Água, malte, arroz e lúpulo.', 'en:gluten', ''),
        ('7892000000006', 'Cerveja Itaipava Lata', 'Água, malte, cereais não maltados, lúpulo.', 'en:gluten', ''),
        ('7892000000007', 'Cerveja Bohemia', 'Água, malte e lúpulo.', 'en:gluten', ''),
        ('7892000000008', 'Cerveja Corona Long Neck', 'Água, malte, arroz, lúpulo.', 'en:gluten', ''),
        ('7892000000009', 'Cerveja Original', 'Água, malte, cereais não maltados, lúpulo.', 'en:gluten', ''),
        ('7892000000010', 'Cerveja Stella Artois', 'Água, malte e lúpulo.', 'en:gluten', ''),
        ('7892000000011', 'Cerveja Devassa', 'Água, malte e lúpulo.', 'en:gluten', ''),
        ('7892000000012', 'Cerveja Eisenbahn', 'Água, malte e lúpulo.', 'en:gluten', ''),
        ('7892000000013', 'Cachaça 51', 'Destilado de mosto fermentado de cana-de-açúcar.', '', ''),
        ('7892000000014', 'Cachaça Velho Barreiro', 'Destilado de mosto fermentado de cana.', '', ''),
        ('7892000000015', 'Cachaça Ypióca', 'Destilado de cana-de-açúcar.', '', ''),
        ('7892000000016', 'Vodka Smirnoff', 'Destilado alcoólico retificado.', '', ''),
        ('7892000000017', 'Vodka Absolut', 'Destilado de cereais.', '', ''),
        ('7892000000018', 'Whisky Johnnie Walker Red Label', 'Destilado alcoólico de malte envelhecido.', '', ''),
        ('7892000000019', 'Vinho Tinto Miolo Reserva', 'Fermentado de uvas tintas.', '', ''),
        ('7892000000020', 'Vinho Branco Aurora', 'Fermentado de uvas brancas.', '', ''),
        ('7892000000021', 'Espumante Chandon', 'Fermentado de uvas.', '', ''),
        ('7892000000022', 'Conhaque Dreher', 'Destilado de vinho e extrato de gengibre.', '', ''),
        ('7892000000023', 'Rum Bacardi', 'Destilado de melaço de cana.', '', ''),

        # ==========================================
        # ☕ CAFÉ, CHÁ E ACHOCOLATADO
        # ==========================================
        ('7893000000001', 'Café Torrado e Moído Pilão', 'Café torrado e moído.', '', ''),
        ('7893000000002', 'Café Torrado e Moído 3 Corações', 'Café torrado e moído.', '', ''),
        ('7893000000003', 'Café Torrado e Moído Melitta', 'Café torrado e moído.', '', ''),
        ('7893000000004', 'Café Solúvel Nescafé Gold', 'Café solúvel.', '', ''),
        ('7893000000005', 'Café Solúvel Sanka', 'Café solúvel descafeinado.', '', ''),
        ('7893000000006', 'Cappuccino Solúvel 3 Corações', 'Leite em pó, açúcar, café solúvel, cacau.', 'en:milk', ''),
        ('7891000369300', 'Achocolatado Nescau', 'Açúcar, cacau em pó, minerais, emulsificante lecitina de soja.', 'en:soybeans', ''),
        ('7896001000672', 'Achocolatado Toddy', 'Açúcar, cacau, extrato de malte, emulsificante lecitina de soja.', 'en:gluten, en:soybeans', ''),
        ('7893000000009', 'Chá Mate Leão', 'Folhas de erva-mate tostadas.', '', ''),
        ('7893000000010', 'Chá Verde Leão', 'Folhas de chá verde.', '', ''),
        ('7893000000011', 'Chá de Camomila', 'Capítulos florais de camomila.', '', ''),
        ('7612100018442', 'Achocolatado Ovomaltine Flocos Crocantes', 'Açúcar, extrato de cereal (cevada e malte), glucose, cacau em pó, sal, canela, emulsificante lecitina de soja e aromatizante.', 'en:gluten, en:soybeans', ''),
        ('7893000000013', 'Creme Crocante Ovomaltine', 'Açúcar, óleo vegetal, avelã, extrato de cereal com cacau, leite desnatado em pó, soro de leite em pó, emulsificante lecitina de soja.', 'en:gluten, en:milk, en:soybeans, en:nuts', ''),

        # ==========================================
        # 🧀 LATICÍNIOS
        # ==========================================
        ('7898080640611', 'Leite Integral UHT Italac', 'Leite integral e estabilizantes.', 'en:milk', ''),
        ('7894000000002', 'Leite Integral UHT Piracanjuba', 'Leite integral e estabilizantes.', 'en:milk', ''),
        ('7894000000003', 'Leite Integral UHT Parmalat', 'Leite integral e estabilizantes.', 'en:milk', ''),
        ('7894000000004', 'Leite Desnatado UHT Elegê', 'Leite desnatado e estabilizantes.', 'en:milk', ''),
        ('7894000000005', 'Leite Semidesnatado UHT Seleção', 'Leite semidesnatado e estabilizantes.', 'en:milk', ''),
        ('7894000000006', 'Leite em Pó Integral Ninho', 'Leite integral rico em cálcio.', 'en:milk', ''),
        ('7894000000007', 'Leite em Pó Desnatado Molico', 'Leite desnatado e vitaminas.', 'en:milk', ''),
        ('7891000053209', 'Leite Condensado Moça', 'Leite integral, açúcar e lactose.', 'en:milk', ''),
        ('7894000000009', 'Creme de Leite UHT', 'Creme de leite padronizado.', 'en:milk', ''),
        ('7894000000010', 'Iogurte Natural Danone', 'Leite integral e fermento lácteo.', 'en:milk', ''),
        ('7894000000011', 'Iogurte Grego Batavo', 'Leite concentrado e fermento lácteo.', 'en:milk', ''),
        ('7894000000012', 'Iogurte Líquido Yakult', 'Leite desnatado, açúcar, fermentos vivos.', 'en:milk', ''),
        ('7894000000013', 'Queijo Mussarela Tirolez', 'Leite pasteurizado, cloreto de sódio, coalho.', 'en:milk', ''),
        ('7894000000014', 'Queijo Parmesão Ralado Polenghi', 'Leite pasteurizado, cloreto de sódio, coalho.', 'en:milk', ''),
        ('7894000000015', 'Queijo Prato Vigor', 'Leite, sal, coalho, corante natural.', 'en:milk', ''),
        ('7894000000016', 'Queijo Coalho', 'Leite pasteurizado, sal, coalho.', 'en:milk', ''),
        ('7894000000017', 'Requeijão Cremoso Catupiry', 'Massa coalhada, creme de leite, sal.', 'en:milk', ''),
        ('7894000000018', 'Cream Cheese Philadelphia', 'Leite, creme de leite, sal, fermento lácteo.', 'en:milk', ''),
        ('7894000000019', 'Manteiga com Sal Aviação', 'Creme de leite pasteurizado e sal.', 'en:milk', ''),
        ('7894000000020', 'Manteiga sem Sal President', 'Creme de leite pasteurizado.', 'en:milk', ''),

        # ==========================================
        # 🍚 GRÃOS E LEGUMINOSAS
        # ==========================================
        ('7895000000001', 'Arroz Branco Tipo 1 Camil', 'Arroz agulhinha tipo 1.', '', ''),
        ('7895000000002', 'Arroz Branco Tipo 1 Tio João', 'Arroz agulhinha tipo 1.', '', ''),
        ('7895000000003', 'Arroz Branco Tipo 1 Pérola', 'Arroz agulhinha tipo 1.', '', ''),
        ('7895000000004', 'Arroz Branco Tipo 1 Namorado', 'Arroz agulhinha tipo 1.', '', ''),
        ('7895000000005', 'Arroz Integral Camil', 'Arroz integral.', '', ''),
        ('7895000000006', 'Arroz Parboilizado Urbano', 'Arroz parboilizado tipo 1.', '', ''),
        ('7895000000007', 'Feijão Carioca Tipo 1 Camil', 'Feijão carioca.', '', ''),
        ('7895000000008', 'Feijão Preto Camil', 'Feijão preto.', '', ''),
        ('7895000000009', 'Feijão Fradinho', 'Feijão fradinho.', '', ''),
        ('7895000000010', 'Feijão Jalo', 'Feijão jalo.', '', ''),
        ('7895000000011', 'Lentilha', 'Lentilhas secas.', '', ''),
        ('7895000000012', 'Grão de Bico', 'Grão de bico.', '', ''),
        ('7895000000013', 'Ervilha Seca', 'Ervilhas secas partidas.', '', ''),
        ('7895000000014', 'Milho de Pipoca', 'Grãos de milho para pipoca.', '', ''),
        ('7895000000015', 'Aveia em Flocos Finos', 'Flocos de aveia.', 'en:gluten', ''),
        ('7895000000016', 'Aveia em Flocos Grossos', 'Flocos de aveia inteiros.', 'en:gluten', ''),

        # ==========================================
        # 🌾 FARINHAS E AMIDOS
        # ==========================================
        ('7896000000001', 'Farinha de Trigo Tipo 1 Dona Benta', 'Farinha de trigo enriquecida com ferro e ácido fólico.', 'en:gluten', ''),
        ('7896000000002', 'Farinha de Trigo Tipo 1 Anaconda', 'Farinha de trigo enriquecida com ferro e ácido fólico.', 'en:gluten', ''),
        ('7896000000003', 'Farinha de Trigo Integral', 'Farinha de trigo integral.', 'en:gluten', ''),
        ('7896000000004', 'Farinha de Mandioca Torrada', 'Farinha de mandioca.', '', ''),
        ('7896000000005', 'Fubá de Milho', 'Farinha de milho.', '', ''),
        ('7896000000006', 'Fubá Mimoso', 'Farinha de milho fina.', '', ''),
        ('7896000000007', 'Amido de Milho Maizena', 'Amido de milho.', '', ''),
        ('7896000000008', 'Farinha de Rosca', 'Pão torrado e moído (farinha de trigo).', 'en:gluten', ''),
        ('7896000000009', 'Polvilho Doce', 'Amido de mandioca.', '', ''),
        ('7896000000010', 'Tapioca Granulada', 'Amido de mandioca granulado.', '', ''),
        ('7896000000011', 'Mistura para Bolo Chocolate', 'Farinha de trigo, açúcar, cacau em pó, soro de leite.', 'en:gluten, en:milk, en:soybeans', ''),
        ('7896000000012', 'Mistura para Bolo Laranja', 'Farinha de trigo, açúcar, aromatizantes.', 'en:gluten, en:soybeans', ''),
        ('7896000000013', 'Fermento em Pó Royal', 'Amido de milho, bicarbonato de sódio.', '', ''),

        # ==========================================
        # 🍝 MASSAS E INSTANTÂNEOS
        # ==========================================
        ('7897000000001', 'Macarrão Espaguete n°8', 'Sêmola de trigo durum, água.', 'en:gluten', ''),
        ('7897000000002', 'Macarrão Espaguete', 'Farinha de trigo, água.', 'en:gluten', ''),
        ('7897000000003', 'Macarrão Parafuso', 'Sêmola de trigo durum, água.', 'en:gluten', ''),
        ('7897000000004', 'Macarrão Penne', 'Sêmola de trigo durum, água.', 'en:gluten', ''),
        ('7897000000005', 'Macarrão Fusilli', 'Sêmola de trigo durum, água.', 'en:gluten', ''),
        ('7897000000006', 'Macarrão Farfalle', 'Sêmola de trigo durum, água.', 'en:gluten', ''),
        ('7897000000007', 'Macarrão Lasanha', 'Farinha de trigo, ovos, água.', 'en:gluten, en:eggs', ''),
        ('7897000000008', 'Macarrão Cabelo de Anjo', 'Farinha de trigo, água.', 'en:gluten', ''),
        ('7897000000009', 'Macarrão Instantâneo Miojo Galinha', 'Farinha de trigo, gordura vegetal, tempero.', 'en:gluten, en:soybeans', ''),
        ('7897000000010', 'Macarrão Instantâneo Cup Noodles', 'Farinha de trigo, gordura, temperos, proteína de soja.', 'en:gluten, en:soybeans', ''),
        ('7897000000011', 'Macarrão Instantâneo Turma da Mônica', 'Farinha de trigo, gordura vegetal, tempero.', 'en:gluten, en:soybeans', ''),
        ('7891079012351', 'Miojo Galinha Caipira', 'Farinha de trigo, gordura vegetal, tempero sabor galinha caipira.', 'en:gluten, en:soybeans', ''),
        ('7897000000013', 'Miojo Carne', 'Farinha de trigo, gordura vegetal, tempero sabor carne.', 'en:gluten, en:soybeans', ''),
        ('7897000000014', 'Miojo Frango', 'Farinha de trigo, gordura vegetal, tempero sabor frango.', 'en:gluten, en:soybeans', ''),
        ('7897000000015', 'Miojo Camarão', 'Farinha de trigo, gordura vegetal, tempero sabor camarão.', 'en:crustaceans, en:gluten', ''),
        ('7897000000016', 'Miojo Queijo', 'Farinha de trigo, gordura vegetal, tempero sabor queijo.', 'en:milk, en:gluten', ''),
        ('7897000000017', 'Cup Noodles Frango', 'Farinha de trigo, gordura vegetal, tempero de frango desidratado.', 'en:gluten, en:soybeans', ''),
        ('7897000000018', 'Cup Noodles Carne', 'Farinha de trigo, gordura vegetal, tempero de carne desidratada.', 'en:gluten, en:soybeans', ''),
        ('7897000000019', 'Cup Noodles Camarão', 'Farinha de trigo, gordura vegetal, camarão desidratado.', 'en:crustaceans, en:gluten', ''),
        ('7897000000020', 'Macarrão Lámen Gourmet', 'Farinha de trigo, temperos especiais.', 'en:gluten, en:soybeans', ''),
        ('7897000000021', 'Macarrão Instantâneo Sakura', 'Farinha de trigo, tempero à base de shoyu.', 'en:gluten, en:soybeans', ''),
        ('7897000000022', 'Yakissoba Instantâneo', 'Farinha de trigo, molho de soja desidratado.', 'en:gluten, en:soybeans', ''),

        # ==========================================
        # 🧈 ÓLEOS, GORDURAS E AÇÚCAR
        # ==========================================
        ('7898000000001', 'Óleo de Soja Liza', 'Óleo de soja refinado.', 'en:soybeans', ''),
        ('7898000000002', 'Óleo de Soja Soya', 'Óleo de soja refinado.', 'en:soybeans', ''),
        ('7898000000003', 'Óleo de Girassol Liza', 'Óleo de girassol refinado.', '', ''),
        ('7898000000004', 'Óleo de Milho Mazola', 'Óleo de milho refinado.', '', ''),
        ('7898000000005', 'Óleo de Coco Copra', 'Óleo de coco extravirgem.', '', ''),
        ('7898000000006', 'Azeite Extra Virgem Gallo', 'Azeite de oliva extravirgem.', '', ''),
        ('7898000000007', 'Azeite Extra Virgem Borges', 'Azeite de oliva extravirgem.', '', ''),
        ('7898000000008', 'Margarina Qualy', 'Óleos vegetais, leite desnatado, emulsificantes.', 'en:milk, en:soybeans', ''),
        ('7898000000009', 'Margarina Becel', 'Óleos vegetais líquidos e interesterificados.', 'en:soybeans', ''),
        ('7898000000010', 'Açúcar Cristal Caravelas', 'Açúcar cristal.', '', ''),
        ('7898000000011', 'Açúcar Refinado União', 'Açúcar refinado.', '', ''),
        ('7898000000012', 'Açúcar Mascavo Native', 'Açúcar mascavo.', '', ''),
        ('7898000000013', 'Açúcar Demerara', 'Açúcar demerara.', '', ''),
        ('7898000000014', 'Adoçante Sucralose Zero-Cal', 'Água, sorbitol, sucralose.', '', ''),
        ('7898000000015', 'Adoçante Stevia Doce Menos', 'Água, glicosídeos de esteviol.', '', ''),
        ('7898000000016', 'Sal Refinado Cisne', 'Sal, iodo.', '', ''),

        # ==========================================
        # 🧂 TEMPEROS, CONDIMENTOS E CALDOS
        # ==========================================
        ('7899000000001', 'Maionese Hellmann\'s', 'Água, óleo vegetal, ovos, vinagre, sal.', 'en:eggs, en:soybeans', ''),
        ('7899000000002', 'Ketchup Heinz', 'Tomate, açúcar, vinagre, sal.', '', ''),
        ('7899000000003', 'Mostarda Hemmer', 'Água, semente de mostarda, vinagre, sal.', 'en:mustard', ''),
        ('7899000000004', 'Molho de Tomate Heinz', 'Tomate, cebola, alho, azeite.', '', ''),
        ('7899000000005', 'Molho de Tomate Pomarola', 'Tomate, açúcar, sal, cebola.', '', ''),
        ('7899000000006', 'Extrato de Tomate Elefante', 'Tomate, açúcar.', '', ''),
        ('7899000000007', 'Molho de Pimenta Tabasco', 'Pimenta, vinagre, sal.', '', ''),
        ('7899000000008', 'Molho Shoyu Sakura', 'Água, soja, milho, sal.', 'en:soybeans', ''),
        ('7899000000009', 'Vinagre de Álcool Castelo', 'Fermentado acético de álcool.', '', ''),
        ('7899000000010', 'Vinagre de Maçã Mãe Terra', 'Fermentado acético de maçã.', '', ''),
        ('7899000000011', 'Caldo de Carne Knorr', 'Sal, gordura vegetal, amido, extrato de carne, soja.', 'en:soybeans, en:gluten', ''),
        ('7899000000012', 'Caldo de Frango Maggi', 'Sal, gordura vegetal, amido, soja.', 'en:soybeans, en:gluten', ''),
        ('7899000000013', 'Tempero Completo Fondor Maggi', 'Sal, farinha de milho, condimentos.', '', ''),
        ('7899000000014', 'Tempero Frango Assado Kitano', 'Sal, páprica, alho, cebola.', '', ''),
        ('7899000000015', 'Colorau Urucum', 'Semente de urucum moída.', '', ''),
        ('7899000000016', 'Orégano', 'Folhas de orégano.', '', ''),
        ('7899000000017', 'Pimenta do Reino Moída', 'Pimenta do reino.', '', ''),
        ('7899000000018', 'Alho Granulado', 'Alho desidratado.', '', ''),
        ('7899000000019', 'Canela em Pó', 'Canela moída.', '', ''),
        ('7899000000020', 'Cravo da Índia', 'Cravos secos.', '', ''),
        ('7899000000021', 'Louro em Folha', 'Folhas de louro secas.', '', ''),
        ('7899000000022', 'Caldo de Legumes Knorr', 'Sal, gordura vegetal, amido, extrato de legumes.', 'en:soybeans, en:gluten', ''),
        ('7899000000023', 'Caldo de Peixe Maggi', 'Sal, gordura vegetal, amido, extrato de peixe.', 'en:fish, en:soybeans', ''),
        ('7899000000024', 'Caldo de Costela Knorr', 'Sal, gordura vegetal, amido, extrato de carne.', 'en:soybeans, en:gluten', ''),
        ('7899000000025', 'Tempero Baiano', 'Cominho, coentro, pimenta, orégano.', '', ''),
        ('7899000000026', 'Chimichurri', 'Ervas desidratadas, alho, pimenta.', '', ''),
        ('7899000000027', 'Ervas Finas', 'Mix de ervas desidratadas.', '', ''),
        ('7899000000028', 'Noz Moscada', 'Noz moscada moída.', '', ''),
        ('7899000000029', 'Cominho em Pó', 'Cominho moído.', '', ''),
        ('7899000000030', 'Páprica Defumada', 'Pimentão vermelho seco e defumado.', '', ''),
        ('7899000000031', 'Curry em Pó', 'Cúrcuma, coentro, cominho, pimenta.', '', ''),
        ('7899000000032', 'Açafrão da Terra (Cúrcuma)', 'Cúrcuma moída.', '', ''),
        ('7899000000033', 'Alecrim Desidratado', 'Folhas de alecrim secas.', '', ''),
        ('7899000000034', 'Manjericão Desidratado', 'Folhas de manjericão secas.', '', ''),
        ('7899000000035', 'Sal Rosa do Himalaia', 'Sal do Himalaia.', '', ''),
        ('7899000000036', 'Pimenta Calabresa Seca', 'Pimenta calabresa em flocos.', '', ''),
        ('7899000000037', 'Mix de Tempero Churrasco', 'Sal grosso, alho, especiarias.', '', ''),

        # ==========================================
        # 🥫 ENLATADOS E CONSERVAS
        # ==========================================
        ('7890100000001', 'Atum em Óleo Gomes da Costa', 'Atum, óleo de soja, sal.', 'en:fish, en:soybeans', ''),
        ('7890100000002', 'Atum Light Coqueiro', 'Atum, água, sal.', 'en:fish', ''),
        ('7890100000003', 'Sardinha em Molho de Tomate Gomes da Costa', 'Sardinha, polpa de tomate, óleo de soja, sal.', 'en:fish, en:soybeans', ''),
        ('7890100000004', 'Ervilha em Lata Bonduelle', 'Ervilhas, água, sal.', '', ''),
        ('7890100000005', 'Milho Verde em Lata Bonduelle', 'Milho verde, água, sal.', '', ''),
        ('7890100000006', 'Palmito em Conserva Hemmer', 'Palmito, água, sal, ácido cítrico.', '', ''),
        ('7890100000007', 'Cogumelo Paris em Conserva', 'Cogumelos, água, sal.', '', ''),
        ('7890100000008', 'Azeitona Preta Goya', 'Azeitonas, água, sal.', '', ''),
        ('7890100000009', 'Azeitona Verde Hemmer', 'Azeitonas, água, sal.', '', ''),
        ('7890100000010', 'Creme de Milho Verde', 'Milho, creme de leite, sal.', 'en:milk', ''),
        ('7890100000011', 'Tomate Pelado', 'Tomates sem pele, suco de tomate.', '', ''),
        ('7890100000012', 'Patê de Presunto Sadia', 'Carne suína, água, amido, proteína de soja.', 'en:soybeans', ''),
        ('7890100000013', 'Picles em Conserva', 'Pepino, vinagre, sal.', '', ''),

        # ==========================================
        # 🥓 FRIOS, EMBUTIDOS E LATICÍNIOS EXTRAS
        # ==========================================
        ('7890200000001', 'Presunto Cozido Sadia', 'Carne suína, água, sal, proteína de soja.', 'en:soybeans', ''),
        ('7890200000002', 'Mortadela Bologna Perdigão', 'Carnes, gordura suína, água, proteína de soja.', 'en:soybeans', ''),
        ('7890200000003', 'Salsicha Hot Dog Sadia', 'Carne de ave, carne suína, proteína de soja.', 'en:soybeans', ''),
        ('7890200000004', 'Linguiça Calabresa Perdigão', 'Carne suína, carne mecanicamente separada, soja.', 'en:soybeans', ''),
        ('7890200000005', 'Linguiça Toscana Seara', 'Carne suína, água, sal, especiarias.', '', ''),
        ('7890200000006', 'Peito de Peru Defumado Sadia', 'Peito de peru, água, sal, proteína de soja.', 'en:soybeans', ''),
        ('7890200000007', 'Salame Milano Sadia', 'Carne suína, toucinho, sal, leite em pó.', 'en:milk', ''),
        ('7890200000008', 'Pepperoni Seara', 'Carne suína, carne bovina, especiarias.', '', ''),
        ('7890200000009', 'Bacon em Fatias Sadia', 'Barriga suína, sal, conservantes.', '', ''),
        ('7890200000010', 'Frango Inteiro Congelado Sadia', 'Cortes de frango.', '', ''),
        ('7890200000011', 'Coxa e Sobrecoxa Congelada Perdigão', 'Cortes de frango.', '', ''),
        ('7890200000012', 'Filé de Frango Congelado Seara', 'Peito de frango desossado.', '', ''),
        ('7890200000013', 'Hambúrguer Bovino Friboi', 'Carne bovina, água, gordura, proteína de soja.', 'en:soybeans', ''),
        ('7890200000014', 'Nuggets de Frango Sadia', 'Carne de frango, farinha de trigo, óleo, soja.', 'en:gluten, en:soybeans', ''),
        ('7890200000015', 'Almôndega de Carne Seara', 'Carne bovina, carne de ave, farinha de trigo, soja.', 'en:gluten, en:soybeans', ''),
        ('7890200000016', 'Carne Bovina Moída Congelada', 'Carne bovina.', '', ''),
        ('7890200000017', 'Costela Suína Congelada', 'Costela suína.', '', ''),
        ('7890200000018', 'Queijo Brie', 'Leite pasteurizado, fermento lácteo, mofo branco.', 'en:milk', ''),
        ('7890200000019', 'Queijo Gouda', 'Leite pasteurizado, sal, coalho, corante natural.', 'en:milk', ''),
        ('7890200000020', 'Queijo Cheddar Fatiado', 'Leite pasteurizado, sal, coalho, corante natural.', 'en:milk', ''),
        ('7890200000021', 'Queijo Provolone', 'Leite pasteurizado, sal, coalho, defumação.', 'en:milk', ''),
        ('7890200000022', 'Queijo Ricota', 'Soro de leite, leite pasteurizado.', 'en:milk', ''),
        ('7890200000023', 'Queijo Cottage', 'Leite desnatado pasteurizado, creme de leite, sal.', 'en:milk', ''),
        ('7890200000024', 'Iogurte Grego Zero', 'Leite desnatado, fermento lácteo, edulcorantes.', 'en:milk', ''),
        ('7890200000025', 'Petit Suisse de Morango', 'Leite, açúcar, preparado de morango.', 'en:milk', ''),
        ('7890200000026', 'Bebida Láctea Fermentada Yakult', 'Leite desnatado, açúcar, lactobacilos vivos.', 'en:milk', ''),
        ('7890200000027', 'Manteiga Ghee', 'Manteiga clarificada.', 'en:milk', ''),
        ('7890200000028', 'Nata Fresca', 'Creme de leite pasteurizado.', 'en:milk', ''),
        ('7890200000029', 'Creme Duplo de Leite', 'Creme de leite com alto teor de gordura.', 'en:milk', ''),
        ('7890200000030', 'Muçarela de Búfala', 'Leite de búfala pasteurizado, sal, coalho.', 'en:milk', ''),
        ('7890200000031', 'Iogurte Natural sem Lactose', 'Leite integral, enzima lactase, fermento lácteo.', 'en:milk', ''),

        # ==========================================
        # 🍪 BISCOITOS E SALGADINHOS
        # ==========================================
        ('7890300000001', 'Biscoito Cream Cracker', 'Farinha de trigo, gordura vegetal, sal, extrato de malte.', 'en:gluten, en:soybeans', ''),
        ('7890300000002', 'Biscoito Maria', 'Farinha de trigo, açúcar, gordura vegetal, leite em pó.', 'en:gluten, en:milk, en:soybeans', ''),
        ('7890300000003', 'Biscoito Maizena', 'Farinha de trigo, açúcar, gordura vegetal, amido.', 'en:gluten, en:soybeans', ''),
        ('7622300829643', 'Biscoito Recheado Oreo', 'Farinha de trigo, açúcar, gordura vegetal, cacau.', 'en:gluten, en:soybeans', ''),
        ('7890300000005', 'Biscoito Recheado Bono', 'Farinha de trigo, açúcar, gordura vegetal, soro de leite.', 'en:gluten, en:milk, en:soybeans', ''),
        ('7891000344444', 'Biscoito Recheado Passatempo', 'Farinha de trigo, açúcar, gordura, leite em pó.', 'en:gluten, en:milk, en:soybeans', ''),
        ('7890300000007', 'Biscoito Wafer Baunilha', 'Açúcar, farinha de trigo, gordura vegetal, leite.', 'en:gluten, en:milk, en:soybeans', ''),
        ('7890300000008', 'Biscoito Wafer Chocolate', 'Açúcar, farinha de trigo, gordura vegetal, cacau.', 'en:gluten, en:soybeans', ''),
        ('7890300000009', 'Biscoito de Polvilho Yoki', 'Polvilho, óleo vegetal, ovos, leite.', 'en:eggs, en:milk', ''),
        ('7890300000010', 'Biscoito Triunfo Água e Sal', 'Farinha de trigo, gordura, extrato de malte.', 'en:gluten, en:soybeans', ''),
        ('7890300000011', 'Salgadinho Cheetos', 'Sêmola de milho, óleo vegetal, queijo em pó.', 'en:milk, en:soybeans', ''),
        ('7892840800002', 'Salgadinho Ruffles Original', 'Batata, óleo vegetal, sal.', 'en:soybeans', ''),
        ('7890300000013', 'Salgadinho Doritos Nacho', 'Milho, óleo vegetal, preparado sabor queijo.', 'en:milk, en:soybeans', ''),
        ('7890300000014', 'Salgadinho Fandangos', 'Farinha de milho, óleo vegetal, preparado sabor queijo.', 'en:milk, en:soybeans', ''),
        ('7890300000015', 'Pipoca de Micro-ondas Manteiga', 'Milho, gordura vegetal, sal, aroma de manteiga.', 'en:milk', ''),
        ('7890300000016', 'Pipoca de Micro-ondas Natural', 'Milho para pipoca, sal.', '', ''),
        ('7890300000017', 'Barra de Cereal', 'Aveia, xarope de glicose, flocos de arroz, castanhas.', 'en:gluten, en:nuts', ''),
        ('7890300000018', 'Torrada Integral', 'Farinha de trigo integral, farinha de trigo enriquecida, gordura vegetal.', 'en:gluten, en:soybeans', ''),

        # ==========================================
        # 🍫 CHOCOLATES E DOCES
        # ==========================================
        ('7890400000001', 'Chocolate ao Leite Lacta', 'Açúcar, leite em pó integral, massa de cacau, manteiga de cacau.', 'en:milk, en:soybeans', ''),
        ('7890400000002', 'Chocolate Charge', 'Açúcar, xarope de glicose, amendoim, leite condensado, massa de cacau.', 'en:milk, en:peanuts, en:soybeans', ''),
        ('7622300990732', 'Chocolate Bis Original', 'Açúcar, farinha de trigo enriquecida, gordura vegetal, cacau, massa de cacau, amendoim, soro de leite em pó, leite integral em pó.', 'en:gluten, en:peanuts, en:milk, en:soybeans', ''),
        ('7890400000004', 'Chocolate Diamante Negro', 'Açúcar, massa de cacau, manteiga de cacau, leite em pó, mel, castanha-de-caju.', 'en:milk, en:nuts, en:soybeans', ''),
        ('7890400000005', 'Chocolate Laka', 'Açúcar, manteiga de cacau, leite em pó integral.', 'en:milk, en:soybeans', ''),
        ('7890400000006', 'Chocolate Suflair', 'Açúcar, leite em pó, manteiga de cacau, liquor de cacau.', 'en:milk, en:soybeans', ''),
        ('7891000249213', 'Chocolate Kit Kat', 'Açúcar, leite em pó, manteiga de cacau, farinha de trigo.', 'en:gluten, en:milk, en:soybeans', ''),
        ('7890400000008', 'Chocolate Alpino', 'Açúcar, leite em pó integral, massa de cacau, manteiga de cacau.', 'en:milk, en:soybeans', ''),
        ('7890400000009', 'Chocolate Twix', 'Açúcar, xarope de glicose, farinha de trigo, leite em pó.', 'en:gluten, en:milk, en:soybeans', ''),
        ('7890400000010', 'Chocolate Snickers', 'Açúcar, amendoim, xarope de glicose, leite em pó.', 'en:peanuts, en:milk, en:soybeans', ''),
        ('7890400000011', 'Chocolate M&Ms', 'Açúcar, massa de cacau, leite em pó integral.', 'en:milk, en:soybeans', ''),
        ('7890400000012', 'Barra de Chocolate 70% Cacau', 'Massa de cacau, açúcar, cacau em pó, emulsificantes.', 'en:soybeans', ''),
        ('7890400000013', 'Doce de Leite', 'Leite integral, açúcar.', 'en:milk', ''),
        ('7890400000014', 'Goiabada', 'Polpa de goiaba, açúcar, acidulante.', '', ''),
        ('7890400000015', 'Geleia de Morango', 'Morango, açúcar, pectina.', '', ''),
        ('7890400000016', 'Mel Silvestre', 'Mel de abelhas.', '', ''),
        ('7890400000017', 'Paçoca', 'Amendoim, açúcar, sal.', 'en:peanuts', ''),
        ('7890400000018', 'Cocada', 'Coco ralado, açúcar.', '', ''),

        # ==========================================
        # 🥐 PADARIA E MATINAIS
        # ==========================================
        ('7890500000001', 'Pão de Forma Integral', 'Farinha de trigo integral, farinha de trigo enriquecida, glúten.', 'en:gluten, en:soybeans', ''),
        ('7890500000002', 'Pão de Forma Tradicional', 'Farinha de trigo enriquecida, açúcar, óleo de soja.', 'en:gluten, en:soybeans', ''),
        ('7890500000003', 'Torrada Tradicional', 'Farinha de trigo, gordura vegetal, sal.', 'en:gluten, en:soybeans', ''),
        ('7890500000004', 'Panetone com Frutas', 'Farinha de trigo, frutas cristalizadas, uvas passas, ovo, leite.', 'en:gluten, en:eggs, en:milk, en:soybeans', ''),
        ('7890500000005', 'Panetone com Gotas de Chocolate', 'Farinha de trigo, gotas de chocolate, ovo, leite.', 'en:gluten, en:eggs, en:milk, en:soybeans', ''),
        ('7890500000006', 'Cereal Matinal Sucrilhos', 'Milho, açúcar, extrato de malte.', 'en:gluten', ''),
        ('7890500000007', 'Cereal Matinal Corn Flakes', 'Milho, açúcar, sal.', '', ''),
        ('7890500000008', 'Granola Tradicional', 'Aveia, flocos de milho, mel, uva passa, castanhas.', 'en:gluten, en:nuts', ''),
        ('7890500000009', 'Granola Original', 'Aveia em flocos, açúcar mascavo, castanhas.', 'en:gluten, en:nuts', ''),
        ('7890500000010', 'Farinha Láctea', 'Farinha de trigo, leite em pó, açúcar.', 'en:gluten, en:milk', ''),
        ('7890500000011', 'Mel de Abelha', 'Mel puro.', '', ''),

        # ==========================================
        # 🍨 SOBREMESAS E GELATINAS
        # ==========================================
        ('7890600000001', 'Gelatina de Morango', 'Açúcar, gelatina, reguladores de acidez.', '', ''),
        ('7890600000002', 'Gelatina de Uva', 'Açúcar, gelatina, aromatizantes.', '', ''),
        ('7890600000003', 'Pudim de Baunilha', 'Açúcar, amido, aromatizante, corantes.', '', ''),
        ('7890600000004', 'Creme para Sobremesa', 'Leite pasteurizado, açúcar, espessantes.', 'en:milk', ''),
        ('7890600000005', 'Sorvete de Creme', 'Água, açúcar, gordura vegetal, soro de leite.', 'en:milk, en:soybeans', ''),
        ('7890600000006', 'Picolé de Chocolate', 'Água, leite em pó, açúcar, cacau.', 'en:milk, en:soybeans', ''),
        ('7890600000007', 'Sorvete de Morango', 'Água, açúcar, gordura vegetal, leite desnatado.', 'en:milk', ''),
        ('7890600000008', 'Açaí em Polpa 1kg', 'Polpa de açaí, água, xarope de guaraná.', '', ''),
        ('7890600000009', 'Polpa de Frutas Maracujá', 'Polpa de maracujá pasteurizada.', '', ''),

        # ==========================================
        # 🥦 HORTIFRÚTI PROCESSADO
        # ==========================================
        ('7890700000001', 'Batata Palha Yoki', 'Batata, óleo vegetal, sal.', 'en:soybeans', ''),
        ('7890700000002', 'Batata Chips', 'Batata, óleo vegetal, sal.', 'en:soybeans', ''),
        ('7890700000003', 'Cenoura Baby em Embalagem', 'Cenouras miniatura.', '', ''),
        ('7890700000004', 'Alho Descascado em Embalagem', 'Dentes de alho frescos.', '', ''),
        ('7890700000005', 'Cebola Desidratada', 'Cebola seca.', '', ''),
        ('7890700000006', 'Tomate Cereja Embalado', 'Tomates cereja in natura.', '', ''),

        # ==========================================
        # 🥜 PASTAS, CREMES E SPREADS
        # ==========================================
        ('3017620422003', 'Creme de Avelã Nutella', 'Açúcar, óleo de palma, avelãs, cacau, leite em pó.', 'en:milk, en:nuts, en:soybeans', ''),
        ('7890800000002', 'Creme de Avelã Nutella Biscuit', 'Farinha de trigo, açúcar, avelãs, cacau.', 'en:gluten, en:milk, en:nuts', ''),
        ('7890800000003', 'Pasta de Amendoim Integral', 'Amendoim torrado.', 'en:peanuts', ''),
        ('7890800000004', 'Pasta de Amendoim Crocante', 'Amendoim torrado.', 'en:peanuts', ''),
        ('7890800000005', 'Pasta de Amendoim Cremosa', 'Amendoim torrado.', 'en:peanuts', ''),
        ('7890800000006', 'Geleia de Jabuticaba', 'Jabuticaba, açúcar, pectina.', '', ''),
        ('7890800000007', 'Geleia de Frutas Vermelhas', 'Frutas vermelhas, açúcar, pectina.', '', ''),
        ('7890800000008', 'Geleia de Laranja', 'Laranja, açúcar, pectina.', '', ''),
        ('7890800000009', 'Doce de Banana', 'Banana, açúcar.', '', ''),
        ('7890800000010', 'Creme de Ricota', 'Soro de leite, creme de leite, sal.', 'en:milk', ''),
        ('7890800000011', 'Tahine', 'Sementes de gergelim torradas e moídas.', 'en:sesame', ''),

        # ==========================================
        # 🍿 SNACKS E PETISCOS
        # ==========================================
        ('7890900000001', 'Amendoim Japonês', 'Amendoim, farinha de trigo, molho de soja, sal.', 'en:gluten, en:peanuts, en:soybeans', ''),
        ('7890900000002', 'Amendoim Torrado com Sal', 'Amendoim, óleo vegetal, sal.', 'en:peanuts', ''),
        ('7890900000003', 'Amendoim Crocante', 'Amendoim, farinha de trigo, amido, sal.', 'en:gluten, en:peanuts', ''),
        ('7890900000004', 'Castanha de Caju Torrada', 'Castanha de caju, sal.', 'en:nuts', ''),
        ('7890900000005', 'Mix de Nuts', 'Amendoim, castanha de caju, castanha do pará, uva passa.', 'en:peanuts, en:nuts', ''),
        ('7890900000006', 'Nozes', 'Nozes sem casca.', 'en:nuts', ''),
        ('7890900000007', 'Uva Passa Sultana', 'Uvas passas brancas.', '', ''),
        ('7890900000008', 'Damasco Seco', 'Damasco desidratado.', '', ''),
        ('7890900000009', 'Banana Passa', 'Banana desidratada.', '', ''),
        ('7890900000010', 'Coco Ralado', 'Coco desidratado.', '', ''),
        ('7890900000011', 'Pipoca Pronta de Queijo', 'Milho, óleo vegetal, queijo em pó.', 'en:milk, en:soybeans', ''),
        ('7890900000012', 'Snack de Arroz Integral', 'Arroz integral, sal.', '', ''),
        ('7890900000013', 'Batatinha Frita Pringles', 'Batata, óleo vegetal, farinha de milho, amido.', 'en:soybeans', ''),
        ('7890900000014', 'Pretzel Salgado', 'Farinha de trigo, óleo vegetal, sal.', 'en:gluten', ''),
        ('7890900000015', 'Torrada Italiana', 'Farinha de trigo, azeite, sal.', 'en:gluten', ''),
        ('7890900000016', 'Coxinha Congelada', 'Farinha de trigo, frango, caldo de galinha, óleo.', 'en:gluten, en:soybeans', ''),
        ('7890900000017', 'Empanado de Frango Congelado', 'Carne de frango, farinha de trigo, água.', 'en:gluten, en:soybeans', ''),
        ('7890900000018', 'Kibe Congelado', 'Carne bovina, trigo para kibe, hortelã, cebola.', 'en:gluten', ''),
        ('7890900000019', 'Pastel Congelado', 'Farinha de trigo, água, sal.', 'en:gluten', ''),
        ('7890900000020', 'Mini Pizza Congelada', 'Farinha de trigo, queijo, molho de tomate.', 'en:gluten, en:milk', ''),
        ('7890900000021', 'Croissant Congelado', 'Farinha de trigo, manteiga, água, fermento.', 'en:gluten, en:milk', ''),
        ('7890900000022', 'Pão de Queijo Congelado', 'Polvilho, queijo, ovos, óleo vegetal.', 'en:eggs, en:milk', ''),

        # ==========================================
        # 🍲 REFEIÇÕES PRONTAS E MASSAS
        # ==========================================
        ('7891100000001', 'Lasanha Bolonhesa Congelada', 'Massa para lasanha, carne moída, queijo, molho.', 'en:gluten, en:milk', ''),
        ('7891100000002', 'Lasanha 4 Queijos Congelada', 'Massa, queijo mussarela, parmesão, provolone, gorgonzola.', 'en:gluten, en:milk', ''),
        ('7891100000003', 'Frango Grelhado Congelado', 'Peito de frango, temperos.', '', ''),
        ('7891100000004', 'Peixe Empanado Congelado', 'Filé de peixe, farinha de rosca, óleo vegetal.', 'en:fish, en:gluten', ''),
        ('7891100000005', 'Estrogonofe de Frango Pronto', 'Frango, creme de leite, champignon, ketchup.', 'en:milk', ''),
        ('7891100000006', 'Arroz Integral Cozido Vapor', 'Arroz integral cozido.', '', ''),
        ('7891100000007', 'Feijão Cozido em Lata', 'Feijão, água, sal.', '', ''),
        ('7891100000008', 'Lentilha Cozida em Lata', 'Lentilha, água, sal.', '', ''),
        ('7891100000009', 'Sopão Carne e Legumes', 'Macarrão, carne desidratada, legumes desidratados.', 'en:gluten, en:soybeans', ''),
        ('7891100000010', 'Caldo de Feijão Knorr', 'Sal, gordura vegetal, extrato de feijão.', 'en:soybeans', ''),
        ('7891100000011', 'Purê de Batata Instantâneo', 'Flocos de batata desidratada.', 'en:milk', ''),
        ('7891100000012', 'Macarrão ao Molho Sugo', 'Macarrão cozido, molho de tomate.', 'en:gluten', ''),

        # ==========================================
        # 🍅 MOLHOS PRONTOS
        # ==========================================
        ('7891200000001', 'Molho Barbecue', 'Polpa de tomate, açúcar, vinagre, aroma de fumaça.', '', ''),
        ('7891200000002', 'Molho Caesar', 'Água, óleo vegetal, queijo, alho, vinagre.', 'en:milk, en:eggs', ''),
        ('7891200000003', 'Molho Ranch', 'Óleo vegetal, água, soro de leite, alho, cebola.', 'en:milk', ''),
        ('7891200000004', 'Molho Pesto', 'Manjericão, óleo de girassol, queijo, castanhas.', 'en:milk, en:nuts', ''),
        ('7891200000005', 'Molho Bolonhesa Pronto', 'Tomate, carne bovina, cenoura, cebola.', '', ''),
        ('7891200000006', 'Molho Carbonara Pronto', 'Creme de leite, bacon, queijo parmesão, gema de ovo.', 'en:milk, en:eggs', ''),
        ('7891200000007', 'Molho de Tomate com Manjericão', 'Tomate, manjericão, sal, óleo.', '', ''),
        ('7891200000008', 'Molho de Tomate com Alho', 'Tomate, alho, sal, azeite.', '', ''),
        ('7891200000009', 'Molho de Pimenta Sriracha', 'Pimenta jalapeño, açúcar, sal, alho.', '', ''),
        ('7891200000010', 'Molho Teriyaki', 'Molho de soja, açúcar, vinho, especiarias.', 'en:soybeans, en:gluten', ''),
        ('7891200000011', 'Molho Inglês', 'Vinagre, melaço, açúcar, anchovas, especiarias.', 'en:fish', ''),
        ('7891200000012', 'Molho de Ostras', 'Água, açúcar, sal, extrato de ostra.', 'en:molluscs', ''),

        # ==========================================
        # 🧃 BEBIDAS ESPECIAIS E FUNCIONAIS
        # ==========================================
        ('7891300000001', 'Suco Cold Press Laranja', 'Laranja prensada a frio.', '', ''),
        ('7891300000002', 'Kombucha Original', 'Água, cultura kombucha, chá verde, açúcar.', '', ''),
        ('7891300000003', 'Água de Coco com Polpa', 'Água de coco, polpa de coco.', '', ''),
        ('7891300000004', 'Leite de Aveia', 'Água, aveia.', 'en:gluten', ''),
        ('7891300000005', 'Leite de Amêndoas', 'Água, pasta de amêndoas.', 'en:nuts', ''),
        ('7891300000006', 'Leite de Coco', 'Leite de coco, água.', '', ''),
        ('7891300000007', 'Leite de Soja', 'Água, grãos de soja.', 'en:soybeans', ''),
        ('7891300000008', 'Bebida de Soja Baunilha', 'Água, grãos de soja, açúcar, aroma de baunilha.', 'en:soybeans', ''),
        ('7891300000009', 'Bebida Láctea de Morango', 'Soro de leite, leite, preparado de morango.', 'en:milk', ''),
        ('7891300000010', 'Achocolatado Toddynho', 'Soro de leite, leite integral, cacau, açúcar.', 'en:milk', ''),
        ('7891300000011', 'Iogurte para Beber Danone', 'Leite reconstituído, açúcar, fermento.', 'en:milk', ''),
        ('7891300000012', 'Bebida de Iogurte Grego', 'Leite, fermento lácteo, preparado de frutas.', 'en:milk', ''),

        # ==========================================
        # 🌾 CEREALISTAS E FUNCIONAIS
        # ==========================================
        ('7891400000001', 'Chia', 'Sementes de chia.', '', ''),
        ('7891400000002', 'Linhaça Dourada', 'Sementes de linhaça dourada.', '', ''),
        ('7891400000003', 'Quinoa em Grão', 'Grãos de quinoa.', '', ''),
        ('7891400000004', 'Amaranto', 'Grãos de amaranto.', '', ''),
        ('7891400000005', 'Gérmen de Trigo', 'Gérmen de trigo tostado.', 'en:gluten', ''),
        ('7891400000006', 'Farelo de Aveia', 'Farelo de aveia.', 'en:gluten', ''),
        ('7891400000007', 'Biomassa de Banana Verde', 'Polpa de banana verde cozida.', '', ''),
        ('7891400000008', 'Proteína de Soja Texturizada', 'Proteína isolada de soja.', 'en:soybeans', ''),
        ('7891400000009', 'Arroz Negro', 'Arroz negro em grãos.', '', ''),
        ('7891400000010', 'Arroz Vermelho', 'Arroz vermelho em grãos.', '', ''),
        ('7891400000011', 'Whey Protein Chocolate', 'Proteína do soro do leite, cacau, edulcorantes.', 'en:milk, en:soybeans', ''),
        ('7891400000012', 'Whey Protein Baunilha', 'Proteína do soro do leite, aroma de baunilha.', 'en:milk, en:soybeans', ''),
        ('7891400000013', 'Barra Proteica', 'Proteína do leite, cobertura de chocolate, amendoim.', 'en:milk, en:peanuts, en:soybeans', ''),
        ('7891400000014', 'Granola Proteica', 'Aveia, flocos de soja, castanhas, proteína do soro do leite.', 'en:gluten, en:soybeans, en:nuts, en:milk', ''),

        # ==========================================
        # 🧁 PANIFICAÇÃO E CONFEITARIA
        # ==========================================
        ('7891500000001', 'Fermento Biológico Fleischmann', 'Saccharomyces cerevisiae.', '', ''),
        ('7891500000002', 'Cacau em Pó Sicao', 'Cacau em pó.', '', ''),
        ('7891500000003', 'Chocolate em Pó Nestlé', 'Cacau em pó, açúcar.', '', ''),
        ('7891500000004', 'Cobertura de Chocolate Harald', 'Açúcar, gordura vegetal, cacau em pó.', 'en:soybeans', ''),
        ('7891500000005', 'Granulado de Chocolate', 'Açúcar, gordura vegetal, cacau, amido.', 'en:soybeans', ''),
        ('7891500000006', 'Creme de Confeiteiro', 'Amido de milho, açúcar, corantes, aroma de baunilha.', 'en:milk', ''),
        ('7891500000007', 'Leite de Coco para Culinária', 'Extrato de coco, água.', '', ''),
        ('7891500000008', 'Essência de Baunilha', 'Água, álcool, aroma artificial de baunilha.', '', ''),
        ('7891500000009', 'Corante Alimentício', 'Água, corantes artificiais.', '', ''),
        ('7891500000010', 'Gelatina sem Sabor', 'Gelatina em pó de origem animal.', '', ''),
        ('7891500000011', 'Agar Agar', 'Extrato de algas marinhas (agar-agar).', '', ''),
        ('7891500000012', 'Waffle Congelado', 'Farinha de trigo, água, óleo vegetal, ovos.', 'en:gluten, en:eggs', ''),
        ('7891500000013', 'Massa de Pizza Congelada', 'Farinha de trigo, água, fermento, sal.', 'en:gluten', ''),
        ('7891500000014', 'Massa Folhada Congelada', 'Farinha de trigo, margarina, água, sal.', 'en:gluten, en:soybeans', ''),
        ('7891500000015', 'Pão Sírio', 'Farinha de trigo, água, fermento.', 'en:gluten', ''),
        ('7891500000016', 'Wrap de Trigo', 'Farinha de trigo, água, óleo, sal.', 'en:gluten', ''),
        ('7891500000017', 'Bisnaguinha', 'Farinha de trigo, açúcar, leite, ovos.', 'en:gluten, en:milk, en:eggs', ''),

        # ==========================================
        # 🥢 PRODUTOS ORIENTAIS E ÉTNICOS
        # ==========================================
        ('7891600000001', 'Shoyu Kikkoman', 'Água, soja, trigo, sal.', 'en:soybeans, en:gluten', ''),
        ('7891600000002', 'Missô', 'Soja, arroz, sal, fermento.', 'en:soybeans', ''),
        ('7891600000003', 'Alga Nori', 'Alga marinha seca.', '', ''),
        ('7891600000004', 'Arroz para Sushi', 'Arroz de grão curto.', '', ''),
        ('7891600000005', 'Vinagre de Arroz', 'Água, fermentado acético de arroz.', '', ''),
        ('7891600000006', 'Macarrão Soba', 'Farinha de trigo sarraceno, farinha de trigo, água.', 'en:gluten', ''),
        ('7891600000007', 'Macarrão Udon', 'Farinha de trigo, água, sal.', 'en:gluten', ''),
        ('7891600000008', 'Gengibre em Conserva', 'Gengibre, água, vinagre, açúcar.', '', ''),
        ('7891600000009', 'Wasabi em Pasta', 'Raiz forte, mostarda, corantes.', 'en:mustard', ''),
        ('7891600000010', 'Leite de Coco Tailandês', 'Extrato de coco, água.', '', ''),
        ('7891600000011', 'Pasta de Curry Vermelho', 'Pimenta, alho, capim-limão, chalota, sal.', '', ''),
        ('7891600000012', 'Macarrão de Arroz', 'Farinha de arroz, água.', '', ''),
        ('7891600000013', 'Tempurá em Pó', 'Farinha de trigo, amido de milho, fermento.', 'en:gluten', ''),
        ('7891600000014', 'Feijão Azuki', 'Feijão azuki em grãos.', '', ''),

        # ==========================================
        # 🐟 FRUTOS DO MAR E PEIXES
        # ==========================================
        ('7891700000001', 'Camarão Congelado VG', 'Camarão descascado congelado.', 'en:crustaceans', ''),
        ('7891700000002', 'Filé de Tilápia Congelado', 'Filé de tilápia.', 'en:fish', ''),
        ('7891700000003', 'Filé de Salmão Congelado', 'Filé de salmão.', 'en:fish', ''),
        ('7891700000004', 'Bacalhau Salgado Seco', 'Bacalhau, sal.', 'en:fish', ''),
        ('7891700000005', 'Lula em Anéis Congelada', 'Lula em anéis.', 'en:molluscs', ''),
        ('7891700000006', 'Mexilhão Congelado', 'Mexilhão sem concha.', 'en:molluscs', ''),
        ('7891700000007', 'Polvo Congelado', 'Tentáculos de polvo.', 'en:molluscs', ''),
        ('7891700000008', 'Atum Fresco Congelado', 'Postas de atum.', 'en:fish', ''),

        # ==========================================
        # 🥩 CARNES ESPECIAIS E FRIOS
        # ==========================================
        ('7891800000001', 'Peito de Frango sem Osso', 'Cortes de peito de frango.', '', ''),
        ('7891800000002', 'Filé de Frango Temperado', 'Peito de frango, água, sal, condimentos.', '', ''),
        ('7891800000003', 'Contrafilé Bovino', 'Contrafilé bovino in natura.', '', ''),
        ('7891800000004', 'Picanha Bovina', 'Picanha bovina in natura.', '', ''),
        ('7891800000005', 'Costela Bovina', 'Costela bovina in natura.', '', ''),
        ('7891800000006', 'Bisteca Suína', 'Bisteca suína in natura.', '', ''),
        ('7891800000007', 'Lombo Suíno', 'Lombo suíno in natura.', '', ''),
        ('7891800000008', 'Pernil Suíno', 'Pernil suíno in natura.', '', ''),
        ('7891800000009', 'Fraldinha Bovina', 'Fraldinha bovina in natura.', '', ''),
        ('7891800000010', 'Cordeiro Congelado', 'Cortes de cordeiro.', '', ''),
        ('7891800000011', 'Carne de Pato Congelada', 'Cortes de pato.', '', ''),

        # ==========================================
        # 🍩 SOBREMESAS INDUSTRIAIS E CAFÉ
        # ==========================================
        ('7891900000001', 'Brownie Bauducco', 'Açúcar, ovos, farinha de trigo, cacau.', 'en:gluten, en:eggs, en:soybeans', ''),
        ('7891900000002', 'Churros Congelado', 'Farinha de trigo, água, margarina.', 'en:gluten, en:soybeans', ''),
        ('7891900000003', 'Bolo de Rolo', 'Açúcar, farinha de trigo, ovos, manteiga, goiabada.', 'en:gluten, en:eggs, en:milk', ''),
        ('7891900000004', 'Torta de Limão Congelada', 'Farinha, leite condensado, suco de limão, creme de leite.', 'en:gluten, en:milk', ''),
        ('7891900000005', 'Pudim de Leite Pronto', 'Leite, leite condensado, ovos, açúcar.', 'en:milk, en:eggs', ''),
        ('7891900000006', 'Musse de Maracujá', 'Creme de leite, leite condensado, suco de maracujá.', 'en:milk', ''),
        ('7891900000007', 'Danette Chocolate', 'Leite, açúcar, cacau, amido.', 'en:milk', ''),
        ('7891900000008', 'Danoninho', 'Leite, açúcar, queijo petit suisse, morango.', 'en:milk', ''),
        ('7891900000009', 'Palito de Sorvete Cornetto', 'Água, açúcar, gordura vegetal, casquinha de biscoito.', 'en:milk, en:gluten', ''),
        ('7891900000010', 'Sorvete Magnum', 'Leite, açúcar, cobertura de chocolate, amêndoas.', 'en:milk, en:nuts', ''),
        ('7891900000011', 'Sorvete La Frutta', 'Água, açúcar, suco de frutas.', '', ''),
        ('7891900000012', 'Açaí com Granola', 'Polpa de açaí, guaraná, aveia, mel.', 'en:gluten', ''),
        ('7891900000013', 'Brigadeiro Pronto', 'Leite condensado, cacau, margarina.', 'en:milk', ''),
        ('7891900000014', 'Pão de Mel', 'Farinha de trigo, mel, especiarias, cobertura de chocolate.', 'en:gluten, en:milk, en:soybeans', ''),
        ('7891900000015', 'Bolinho Donuts', 'Farinha de trigo, açúcar, óleo, cobertura.', 'en:gluten, en:eggs, en:milk', ''),
        ('7891900000016', 'Bolo Tipo Inglês', 'Farinha de trigo, ovos, açúcar, frutas cristalizadas.', 'en:gluten, en:eggs', ''),
        ('7891900000017', 'Wafer Recheado de Morango', 'Açúcar, farinha de trigo, gordura, aroma de morango.', 'en:gluten, en:milk, en:soybeans', ''),
        ('7891900000018', 'Biscoito Recheado Negresco', 'Farinha de trigo, açúcar, gordura, cacau.', 'en:gluten, en:soybeans', ''),
        ('7622210574044', 'Biscoito Recheado Trakinas', 'Farinha de trigo, açúcar, gordura, leite em pó.', 'en:gluten, en:milk, en:soybeans', ''),
        ('7891900000020', 'Biscoito Amanteigado', 'Farinha de trigo, manteiga, açúcar.', 'en:gluten, en:milk', ''),
        ('7891900000021', 'Biscoito Champagne', 'Farinha de trigo, açúcar, ovos.', 'en:gluten, en:eggs', ''),
        ('7891900000022', 'Rosquinha de Coco', 'Farinha de trigo, açúcar, coco ralado.', 'en:gluten', ''),
        ('7891900000023', 'Bala de Goma Fini', 'Xarope de glicose, açúcar, gelatina.', '', ''),
        ('7891900000024', 'Bala de Goma Trolli', 'Xarope de glicose, açúcar, gelatina, corantes.', '', ''),
        ('7891900000025', 'Bala Mentos', 'Açúcar, xarope de glicose, óleo vegetal.', '', ''),
        ('7891900000026', 'Chiclete Trident', 'Goma base, edulcorantes, aromatizantes.', '', ''),
        ('7891900000027', 'Chiclete Halls', 'Açúcar, xarope de glicose, mentol.', '', ''),
        ('7891900000028', 'Pirulito Chupa Chups', 'Açúcar, xarope de glicose, purê de frutas.', '', ''),

        # ==========================================
        # 🥭 POLPAS E FRUTAS PROCESSADAS
        # ==========================================
        ('7892100000001', 'Polpa de Acerola', 'Polpa de acerola pasteurizada.', '', ''),
        ('7892100000002', 'Polpa de Caju', 'Polpa de caju pasteurizada.', '', ''),
        ('7892100000003', 'Polpa de Goiaba', 'Polpa de goiaba pasteurizada.', '', ''),
        ('7892100000004', 'Polpa de Cupuaçu', 'Polpa de cupuaçu pasteurizada.', '', ''),
        ('7892100000005', 'Polpa de Pitanga', 'Polpa de pitanga pasteurizada.', '', ''),
        ('7892100000006', 'Uva Passa Preta', 'Uva passa escura sem semente.', '', ''),
        ('7892100000007', 'Ameixa Seca', 'Ameixas desidratadas sem caroço.', '', ''),
        ('7892100000008', 'Tâmara', 'Tâmaras secas.', '', ''),
        ('7892100000009', 'Figo Seco', 'Figo desidratado.', '', ''),
        ('7892100000010', 'Abacaxi em Calda', 'Abacaxi, água, açúcar.', '', ''),
        ('7892100000011', 'Pêssego em Calda', 'Pêssegos, água, açúcar.', '', ''),
        ('7892100000012', 'Cocktail de Frutas', 'Frutas mistas, água, açúcar.', '', ''),

        # ==========================================
        # 🥗 DIET, LIGHT E SEM GLÚTEN
        # ==========================================
        ('7892200000001', 'Biscoito sem Glúten', 'Farinha de arroz, fécula de batata, açúcar.', '', ''),
        ('7892200000002', 'Macarrão sem Glúten', 'Farinha de arroz, farinha de milho.', '', ''),
        ('7892200000003', 'Pão sem Glúten', 'Farinha de arroz, fécula de mandioca, óleo vegetal.', '', ''),
        ('7892200000004', 'Farinha de Amêndoas', 'Amêndoas moídas.', 'en:nuts', ''),
        ('7892200000005', 'Farinha de Arroz', 'Grãos de arroz moídos.', '', ''),
        ('7892200000006', 'Cereal de Milho sem Açúcar', 'Flocos de milho.', '', ''),
        ('7892200000007', 'Iogurte Zero Lactose', 'Leite, fermento lácteo, enzima lactase.', 'en:milk', ''),
        ('7892200000008', 'Leite sem Lactose', 'Leite integral, enzima lactase.', 'en:milk', ''),
        ('7892200000009', 'Chocolate Diet', 'Massa de cacau, edulcorantes, leite em pó.', 'en:milk, en:soybeans', ''),
        ('7892200000010', 'Refrigerante Zero Açúcar Coca-Cola', 'Água gaseificada, extrato de noz de cola, edulcorantes.', '', ''),
        ('7892200000011', 'Refrigerante Zero Pepsi', 'Água gaseificada, extrato de cola, edulcorantes.', '', ''),
        ('7892200000012', 'Biscoito Integral', 'Farinha de trigo integral, aveia, açúcar mascavo.', 'en:gluten', '')
    ]

    cursor.executemany('''
        REPLACE INTO alimentos (codigo_barras, nome, ingredientes, alergenicos, imagem_url)
        VALUES (?, ?, ?, ?, ?)
    ''', produtos)

    conexao.commit()
    conexao.close()
    
    print(f"✅ SUCESSO ABSOLUTO! {len(produtos)} produtos do seu catálogo foram injetados no Banco de Dados com códigos EAN-13!")

if __name__ == '__main__':
    abastecer()