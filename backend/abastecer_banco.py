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

    # Catálogo COMPLETO processado a partir dos arquivos do Atacadão
    produtos = [
        # ==========================================
        # 🥤 BEBIDAS NÃO ALCOÓLICAS
        # ==========================================
        ('100001', 'Refrigerante Coca-Cola', 'Água gaseificada, açúcar, extrato de noz de cola, cafeína.', '', ''),
        ('100002', 'Refrigerante Pepsi', 'Água gaseificada, açúcar, extrato de cola, cafeína.', '', ''),
        ('100003', 'Refrigerante Guaraná Antarctica', 'Água gaseificada, açúcar, extrato de guaraná.', '', ''),
        ('100004', 'Refrigerante Fanta Laranja', 'Água gaseificada, açúcar, suco de laranja.', '', ''),
        ('100005', 'Refrigerante Sprite', 'Água gaseificada, açúcar, suco de limão.', '', ''),
        ('100006', 'Refrigerante Schweppes Tônica', 'Água gaseificada, açúcar, quinino.', '', ''),
        ('100007', 'Refrigerante Kuat', 'Água gaseificada, açúcar, extrato de guaraná.', '', ''),
        ('100008', 'Refrigerante H2OH', 'Água gaseificada, suco de limão, edulcorantes.', '', ''),
        ('100009', 'Refrigerante Limão Misteriosa', 'Água gaseificada, açúcar, suco de limão.', '', ''),
        ('100010', 'Refrigerante Sukita', 'Água gaseificada, açúcar, suco de laranja.', '', ''),
        ('100011', 'Suco de Laranja Do Bem', 'Suco de laranja integral.', '', ''),
        ('100012', 'Néctar de Pêssego Maguary', 'Água, suco de pêssego, açúcar.', '', ''),
        ('100013', 'Néctar de Goiaba Maguary', 'Água, suco de goiaba, açúcar.', '', ''),
        ('100014', 'Suco Integral de Uva', 'Suco de uva integral.', '', ''),
        ('100015', 'Suco Kapo Caixinha', 'Água, açúcar, suco de frutas.', '', ''),
        ('100016', 'Suco Tang Pó Laranja', 'Açúcar, maltodextrina, polpa de laranja desidratada.', '', ''),
        ('100017', 'Suco Tang Pó Maracujá', 'Açúcar, maltodextrina, polpa de maracujá desidratada.', '', ''),
        ('100018', 'Refresco em Pó Clight', 'Maltodextrina, polpa de fruta, edulcorantes.', '', ''),
        ('100019', 'Água de Coco Sococo', 'Água de coco.', '', ''),
        ('100020', 'Água de Coco Kero Coco', 'Água de coco integral.', '', ''),
        ('100021', 'Água Mineral Crystal sem Gás', 'Água mineral natural.', '', ''),
        ('100022', 'Água Mineral Bonafont sem Gás', 'Água mineral natural.', '', ''),
        ('100023', 'Água Mineral Minalba com Gás', 'Água mineral gaseificada artificialmente.', '', ''),
        ('100024', 'Isotônico Gatorade', 'Água, sacarose, sais minerais.', '', ''),
        ('100025', 'Energético Red Bull', 'Água gaseificada, taurina, cafeína.', '', ''),
        ('100026', 'Energético Monster', 'Água gaseificada, açúcar, extrato de ginseng, taurina.', '', ''),
        ('100027', 'Energético TNT', 'Água gaseificada, taurina, cafeína.', '', ''),

        # ==========================================
        # 🍺 CERVEJAS E BEBIDAS ALCOÓLICAS
        # ==========================================
        ('200001', 'Cerveja Heineken Lata', 'Água, malte e lúpulo.', 'en:gluten', ''),
        ('200002', 'Cerveja Brahma Lata', 'Água, malte, cereais não maltados, lúpulo.', 'en:gluten', ''),
        ('200003', 'Cerveja Skol Lata', 'Água, malte, milho e lúpulo.', 'en:gluten', ''),
        ('200004', 'Cerveja Antarctica Garrafa', 'Água, malte, cereais não maltados, lúpulo.', 'en:gluten', ''),
        ('200005', 'Cerveja Budweiser Long Neck', 'Água, malte, arroz e lúpulo.', 'en:gluten', ''),
        ('200006', 'Cerveja Itaipava Lata', 'Água, malte, cereais não maltados, lúpulo.', 'en:gluten', ''),
        ('200007', 'Cerveja Bohemia', 'Água, malte e lúpulo.', 'en:gluten', ''),
        ('200008', 'Cerveja Corona Long Neck', 'Água, malte, arroz, lúpulo.', 'en:gluten', ''),
        ('200009', 'Cerveja Original', 'Água, malte, cereais não maltados, lúpulo.', 'en:gluten', ''),
        ('200010', 'Cerveja Stella Artois', 'Água, malte e lúpulo.', 'en:gluten', ''),
        ('200011', 'Cerveja Devassa', 'Água, malte e lúpulo.', 'en:gluten', ''),
        ('200012', 'Cerveja Eisenbahn', 'Água, malte e lúpulo.', 'en:gluten', ''),
        ('200013', 'Cachaça 51', 'Destilado de mosto fermentado de cana-de-açúcar.', '', ''),
        ('200014', 'Cachaça Velho Barreiro', 'Destilado de mosto fermentado de cana.', '', ''),
        ('200015', 'Cachaça Ypióca', 'Destilado de cana-de-açúcar.', '', ''),
        ('200016', 'Vodka Smirnoff', 'Destilado alcoólico retificado.', '', ''),
        ('200017', 'Vodka Absolut', 'Destilado de cereais.', '', ''),
        ('200018', 'Whisky Johnnie Walker Red Label', 'Destilado alcoólico de malte envelhecido.', '', ''),
        ('200019', 'Vinho Tinto Miolo Reserva', 'Fermentado de uvas tintas.', '', ''),
        ('200020', 'Vinho Branco Aurora', 'Fermentado de uvas brancas.', '', ''),
        ('200021', 'Espumante Chandon', 'Fermentado de uvas.', '', ''),
        ('200022', 'Conhaque Dreher', 'Destilado de vinho e extrato de gengibre.', '', ''),
        ('200023', 'Rum Bacardi', 'Destilado de melaço de cana.', '', ''),

        # ==========================================
        # ☕ CAFÉ, CHÁ E ACHOCOLATADO
        # ==========================================
        ('300001', 'Café Torrado e Moído Pilão', 'Café torrado e moído.', '', ''),
        ('300002', 'Café Torrado e Moído 3 Corações', 'Café torrado e moído.', '', ''),
        ('300003', 'Café Torrado e Moído Melitta', 'Café torrado e moído.', '', ''),
        ('300004', 'Café Solúvel Nescafé Gold', 'Café solúvel.', '', ''),
        ('300005', 'Café Solúvel Sanka', 'Café solúvel descafeinado.', '', ''),
        ('300006', 'Cappuccino Solúvel 3 Corações', 'Leite em pó, açúcar, café solúvel, cacau.', 'en:milk', ''),
        ('300007', 'Achocolatado Nescau', 'Açúcar, cacau em pó, minerais, emulsificante lecitina de soja.', 'en:soybeans', ''),
        ('300008', 'Achocolatado Toddy', 'Açúcar, cacau, extrato de malte, emulsificante lecitina de soja.', 'en:gluten, en:soybeans', ''),
        ('300009', 'Chá Mate Leão', 'Folhas de erva-mate tostadas.', '', ''),
        ('300010', 'Chá Verde Leão', 'Folhas de chá verde.', '', ''),
        ('300011', 'Chá de Camomila', 'Capítulos florais de camomila.', '', ''),
        ('300012', 'Achocolatado Ovomaltine Flocos Crocantes', 'Açúcar, extrato de cereal (cevada e malte), glucose, cacau em pó, sal, canela, emulsificante lecitina de soja e aromatizante.', 'en:gluten, en:soybeans', ''),
        ('300013', 'Creme Crocante Ovomaltine', 'Açúcar, óleo vegetal, avelã, extrato de cereal com cacau, leite desnatado em pó, soro de leite em pó, emulsificante lecitina de soja.', 'en:gluten, en:milk, en:soybeans, en:nuts', ''),

        # ==========================================
        # 🧀 LATICÍNIOS
        # ==========================================
        ('400001', 'Leite Integral UHT Italac', 'Leite integral e estabilizantes.', 'en:milk', ''),
        ('400002', 'Leite Integral UHT Piracanjuba', 'Leite integral e estabilizantes.', 'en:milk', ''),
        ('400003', 'Leite Integral UHT Parmalat', 'Leite integral e estabilizantes.', 'en:milk', ''),
        ('400004', 'Leite Desnatado UHT Elegê', 'Leite desnatado e estabilizantes.', 'en:milk', ''),
        ('400005', 'Leite Semidesnatado UHT Seleção', 'Leite semidesnatado e estabilizantes.', 'en:milk', ''),
        ('400006', 'Leite em Pó Integral Ninho', 'Leite integral rico em cálcio.', 'en:milk', ''),
        ('400007', 'Leite em Pó Desnatado Molico', 'Leite desnatado e vitaminas.', 'en:milk', ''),
        ('400008', 'Leite Condensado Moça', 'Leite integral, açúcar e lactose.', 'en:milk', ''),
        ('400009', 'Creme de Leite UHT', 'Creme de leite padronizado.', 'en:milk', ''),
        ('400010', 'Iogurte Natural Danone', 'Leite integral e fermento lácteo.', 'en:milk', ''),
        ('400011', 'Iogurte Grego Batavo', 'Leite concentrado e fermento lácteo.', 'en:milk', ''),
        ('400012', 'Iogurte Líquido Yakult', 'Leite desnatado, açúcar, fermentos vivos.', 'en:milk', ''),
        ('400013', 'Queijo Mussarela Tirolez', 'Leite pasteurizado, cloreto de sódio, coalho.', 'en:milk', ''),
        ('400014', 'Queijo Parmesão Ralado Polenghi', 'Leite pasteurizado, cloreto de sódio, coalho.', 'en:milk', ''),
        ('400015', 'Queijo Prato Vigor', 'Leite, sal, coalho, corante natural.', 'en:milk', ''),
        ('400016', 'Queijo Coalho', 'Leite pasteurizado, sal, coalho.', 'en:milk', ''),
        ('400017', 'Requeijão Cremoso Catupiry', 'Massa coalhada, creme de leite, sal.', 'en:milk', ''),
        ('400018', 'Cream Cheese Philadelphia', 'Leite, creme de leite, sal, fermento lácteo.', 'en:milk', ''),
        ('400019', 'Manteiga com Sal Aviação', 'Creme de leite pasteurizado e sal.', 'en:milk', ''),
        ('400020', 'Manteiga sem Sal President', 'Creme de leite pasteurizado.', 'en:milk', ''),

        # ==========================================
        # 🍚 GRÃOS E LEGUMINOSAS
        # ==========================================
        ('500001', 'Arroz Branco Tipo 1 Camil', 'Arroz agulhinha tipo 1.', '', ''),
        ('500002', 'Arroz Branco Tipo 1 Tio João', 'Arroz agulhinha tipo 1.', '', ''),
        ('500003', 'Arroz Branco Tipo 1 Pérola', 'Arroz agulhinha tipo 1.', '', ''),
        ('500004', 'Arroz Branco Tipo 1 Namorado', 'Arroz agulhinha tipo 1.', '', ''),
        ('500005', 'Arroz Integral Camil', 'Arroz integral.', '', ''),
        ('500006', 'Arroz Parboilizado Urbano', 'Arroz parboilizado tipo 1.', '', ''),
        ('500007', 'Feijão Carioca Tipo 1 Camil', 'Feijão carioca.', '', ''),
        ('500008', 'Feijão Preto Camil', 'Feijão preto.', '', ''),
        ('500009', 'Feijão Fradinho', 'Feijão fradinho.', '', ''),
        ('500010', 'Feijão Jalo', 'Feijão jalo.', '', ''),
        ('500011', 'Lentilha', 'Lentilhas secas.', '', ''),
        ('500012', 'Grão de Bico', 'Grão de bico.', '', ''),
        ('500013', 'Ervilha Seca', 'Ervilhas secas partidas.', '', ''),
        ('500014', 'Milho de Pipoca', 'Grãos de milho para pipoca.', '', ''),
        ('500015', 'Aveia em Flocos Finos', 'Flocos de aveia.', 'en:gluten', ''),
        ('500016', 'Aveia em Flocos Grossos', 'Flocos de aveia inteiros.', 'en:gluten', ''),

        # ==========================================
        # 🌾 FARINHAS E AMIDOS
        # ==========================================
        ('600001', 'Farinha de Trigo Tipo 1 Dona Benta', 'Farinha de trigo enriquecida com ferro e ácido fólico.', 'en:gluten', ''),
        ('600002', 'Farinha de Trigo Tipo 1 Anaconda', 'Farinha de trigo enriquecida com ferro e ácido fólico.', 'en:gluten', ''),
        ('600003', 'Farinha de Trigo Integral', 'Farinha de trigo integral.', 'en:gluten', ''),
        ('600004', 'Farinha de Mandioca Torrada', 'Farinha de mandioca.', '', ''),
        ('600005', 'Fubá de Milho', 'Farinha de milho.', '', ''),
        ('600006', 'Fubá Mimoso', 'Farinha de milho fina.', '', ''),
        ('600007', 'Amido de Milho Maizena', 'Amido de milho.', '', ''),
        ('600008', 'Farinha de Rosca', 'Pão torrado e moído (farinha de trigo).', 'en:gluten', ''),
        ('600009', 'Polvilho Doce', 'Amido de mandioca.', '', ''),
        ('600010', 'Tapioca Granulada', 'Amido de mandioca granulado.', '', ''),
        ('600011', 'Mistura para Bolo Chocolate', 'Farinha de trigo, açúcar, cacau em pó, soro de leite.', 'en:gluten, en:milk, en:soybeans', ''),
        ('600012', 'Mistura para Bolo Laranja', 'Farinha de trigo, açúcar, aromatizantes.', 'en:gluten, en:soybeans', ''),
        ('600013', 'Fermento em Pó Royal', 'Amido de milho, bicarbonato de sódio.', '', ''),

        # ==========================================
        # 🍝 MASSAS E INSTANTÂNEOS
        # ==========================================
        ('700001', 'Macarrão Espaguete n°8', 'Sêmola de trigo durum, água.', 'en:gluten', ''),
        ('700002', 'Macarrão Espaguete', 'Farinha de trigo, água.', 'en:gluten', ''),
        ('700003', 'Macarrão Parafuso', 'Sêmola de trigo durum, água.', 'en:gluten', ''),
        ('700004', 'Macarrão Penne', 'Sêmola de trigo durum, água.', 'en:gluten', ''),
        ('700005', 'Macarrão Fusilli', 'Sêmola de trigo durum, água.', 'en:gluten', ''),
        ('700006', 'Macarrão Farfalle', 'Sêmola de trigo durum, água.', 'en:gluten', ''),
        ('700007', 'Macarrão Lasanha', 'Farinha de trigo, ovos, água.', 'en:gluten, en:eggs', ''),
        ('700008', 'Macarrão Cabelo de Anjo', 'Farinha de trigo, água.', 'en:gluten', ''),
        ('700009', 'Macarrão Instantâneo Miojo Galinha', 'Farinha de trigo, gordura vegetal, tempero.', 'en:gluten, en:soybeans', ''),
        ('700010', 'Macarrão Instantâneo Cup Noodles', 'Farinha de trigo, gordura, temperos, proteína de soja.', 'en:gluten, en:soybeans', ''),
        ('700011', 'Macarrão Instantâneo Turma da Mônica', 'Farinha de trigo, gordura vegetal, tempero.', 'en:gluten, en:soybeans', ''),
        ('700012', 'Miojo Galinha Caipira', 'Farinha de trigo, gordura vegetal, tempero sabor galinha caipira.', 'en:gluten, en:soybeans', ''),
        ('700013', 'Miojo Carne', 'Farinha de trigo, gordura vegetal, tempero sabor carne.', 'en:gluten, en:soybeans', ''),
        ('700014', 'Miojo Frango', 'Farinha de trigo, gordura vegetal, tempero sabor frango.', 'en:gluten, en:soybeans', ''),
        ('700015', 'Miojo Camarão', 'Farinha de trigo, gordura vegetal, tempero sabor camarão.', 'en:crustaceans, en:gluten', ''),
        ('700016', 'Miojo Queijo', 'Farinha de trigo, gordura vegetal, tempero sabor queijo.', 'en:milk, en:gluten', ''),
        ('700017', 'Cup Noodles Frango', 'Farinha de trigo, gordura vegetal, tempero de frango desidratado.', 'en:gluten, en:soybeans', ''),
        ('700018', 'Cup Noodles Carne', 'Farinha de trigo, gordura vegetal, tempero de carne desidratada.', 'en:gluten, en:soybeans', ''),
        ('700019', 'Cup Noodles Camarão', 'Farinha de trigo, gordura vegetal, camarão desidratado.', 'en:crustaceans, en:gluten', ''),
        ('700020', 'Macarrão Lámen Gourmet', 'Farinha de trigo, temperos especiais.', 'en:gluten, en:soybeans', ''),
        ('700021', 'Macarrão Instantâneo Sakura', 'Farinha de trigo, tempero à base de shoyu.', 'en:gluten, en:soybeans', ''),
        ('700022', 'Yakissoba Instantâneo', 'Farinha de trigo, molho de soja desidratado.', 'en:gluten, en:soybeans', ''),

        # ==========================================
        # 🧈 ÓLEOS, GORDURAS E AÇÚCAR
        # ==========================================
        ('800001', 'Óleo de Soja Liza', 'Óleo de soja refinado.', 'en:soybeans', ''),
        ('800002', 'Óleo de Soja Soya', 'Óleo de soja refinado.', 'en:soybeans', ''),
        ('800003', 'Óleo de Girassol Liza', 'Óleo de girassol refinado.', '', ''),
        ('800004', 'Óleo de Milho Mazola', 'Óleo de milho refinado.', '', ''),
        ('800005', 'Óleo de Coco Copra', 'Óleo de coco extravirgem.', '', ''),
        ('800006', 'Azeite Extra Virgem Gallo', 'Azeite de oliva extravirgem.', '', ''),
        ('800007', 'Azeite Extra Virgem Borges', 'Azeite de oliva extravirgem.', '', ''),
        ('800008', 'Margarina Qualy', 'Óleos vegetais, leite desnatado, emulsificantes.', 'en:milk, en:soybeans', ''),
        ('800009', 'Margarina Becel', 'Óleos vegetais líquidos e interesterificados.', 'en:soybeans', ''),
        ('800010', 'Açúcar Cristal Caravelas', 'Açúcar cristal.', '', ''),
        ('800011', 'Açúcar Refinado União', 'Açúcar refinado.', '', ''),
        ('800012', 'Açúcar Mascavo Native', 'Açúcar mascavo.', '', ''),
        ('800013', 'Açúcar Demerara', 'Açúcar demerara.', '', ''),
        ('800014', 'Adoçante Sucralose Zero-Cal', 'Água, sorbitol, sucralose.', '', ''),
        ('800015', 'Adoçante Stevia Doce Menos', 'Água, glicosídeos de esteviol.', '', ''),
        ('800016', 'Sal Refinado Cisne', 'Sal, iodo.', '', ''),

        # ==========================================
        # 🧂 TEMPEROS, CONDIMENTOS E CALDOS
        # ==========================================
        ('900001', 'Maionese Hellmann\'s', 'Água, óleo vegetal, ovos, vinagre, sal.', 'en:eggs, en:soybeans', ''),
        ('900002', 'Ketchup Heinz', 'Tomate, açúcar, vinagre, sal.', '', ''),
        ('900003', 'Mostarda Hemmer', 'Água, semente de mostarda, vinagre, sal.', 'en:mustard', ''),
        ('900004', 'Molho de Tomate Heinz', 'Tomate, cebola, alho, azeite.', '', ''),
        ('900005', 'Molho de Tomate Pomarola', 'Tomate, açúcar, sal, cebola.', '', ''),
        ('900006', 'Extrato de Tomate Elefante', 'Tomate, açúcar.', '', ''),
        ('900007', 'Molho de Pimenta Tabasco', 'Pimenta, vinagre, sal.', '', ''),
        ('900008', 'Molho Shoyu Sakura', 'Água, soja, milho, sal.', 'en:soybeans', ''),
        ('900009', 'Vinagre de Álcool Castelo', 'Fermentado acético de álcool.', '', ''),
        ('900010', 'Vinagre de Maçã Mãe Terra', 'Fermentado acético de maçã.', '', ''),
        ('900011', 'Caldo de Carne Knorr', 'Sal, gordura vegetal, amido, extrato de carne, soja.', 'en:soybeans, en:gluten', ''),
        ('900012', 'Caldo de Frango Maggi', 'Sal, gordura vegetal, amido, soja.', 'en:soybeans, en:gluten', ''),
        ('900013', 'Tempero Completo Fondor Maggi', 'Sal, farinha de milho, condimentos.', '', ''),
        ('900014', 'Tempero Frango Assado Kitano', 'Sal, páprica, alho, cebola.', '', ''),
        ('900015', 'Colorau Urucum', 'Semente de urucum moída.', '', ''),
        ('900016', 'Orégano', 'Folhas de orégano.', '', ''),
        ('900017', 'Pimenta do Reino Moída', 'Pimenta do reino.', '', ''),
        ('900018', 'Alho Granulado', 'Alho desidratado.', '', ''),
        ('900019', 'Canela em Pó', 'Canela moída.', '', ''),
        ('900020', 'Cravo da Índia', 'Cravos secos.', '', ''),
        ('900021', 'Louro em Folha', 'Folhas de louro secas.', '', ''),
        ('900022', 'Caldo de Legumes Knorr', 'Sal, gordura vegetal, amido, extrato de legumes.', 'en:soybeans, en:gluten', ''),
        ('900023', 'Caldo de Peixe Maggi', 'Sal, gordura vegetal, amido, extrato de peixe.', 'en:fish, en:soybeans', ''),
        ('900024', 'Caldo de Costela Knorr', 'Sal, gordura vegetal, amido, extrato de carne.', 'en:soybeans, en:gluten', ''),
        ('900025', 'Tempero Baiano', 'Cominho, coentro, pimenta, orégano.', '', ''),
        ('900026', 'Chimichurri', 'Ervas desidratadas, alho, pimenta.', '', ''),
        ('900027', 'Ervas Finas', 'Mix de ervas desidratadas.', '', ''),
        ('900028', 'Noz Moscada', 'Noz moscada moída.', '', ''),
        ('900029', 'Cominho em Pó', 'Cominho moído.', '', ''),
        ('900030', 'Páprica Defumada', 'Pimentão vermelho seco e defumado.', '', ''),
        ('900031', 'Curry em Pó', 'Cúrcuma, coentro, cominho, pimenta.', '', ''),
        ('900032', 'Açafrão da Terra (Cúrcuma)', 'Cúrcuma moída.', '', ''),
        ('900033', 'Alecrim Desidratado', 'Folhas de alecrim secas.', '', ''),
        ('900034', 'Manjericão Desidratado', 'Folhas de manjericão secas.', '', ''),
        ('900035', 'Sal Rosa do Himalaia', 'Sal do Himalaia.', '', ''),
        ('900036', 'Pimenta Calabresa Seca', 'Pimenta calabresa em flocos.', '', ''),
        ('900037', 'Mix de Tempero Churrasco', 'Sal grosso, alho, especiarias.', '', ''),

        # ==========================================
        # 🥫 ENLATADOS E CONSERVAS
        # ==========================================
        ('110001', 'Atum em Óleo Gomes da Costa', 'Atum, óleo de soja, sal.', 'en:fish, en:soybeans', ''),
        ('110002', 'Atum Light Coqueiro', 'Atum, água, sal.', 'en:fish', ''),
        ('110003', 'Sardinha em Molho de Tomate Gomes da Costa', 'Sardinha, polpa de tomate, óleo de soja, sal.', 'en:fish, en:soybeans', ''),
        ('110004', 'Ervilha em Lata Bonduelle', 'Ervilhas, água, sal.', '', ''),
        ('110005', 'Milho Verde em Lata Bonduelle', 'Milho verde, água, sal.', '', ''),
        ('110006', 'Palmito em Conserva Hemmer', 'Palmito, água, sal, ácido cítrico.', '', ''),
        ('110007', 'Cogumelo Paris em Conserva', 'Cogumelos, água, sal.', '', ''),
        ('110008', 'Azeitona Preta Goya', 'Azeitonas, água, sal.', '', ''),
        ('110009', 'Azeitona Verde Hemmer', 'Azeitonas, água, sal.', '', ''),
        ('110010', 'Creme de Milho Verde', 'Milho, creme de leite, sal.', 'en:milk', ''),
        ('110011', 'Tomate Pelado', 'Tomates sem pele, suco de tomate.', '', ''),
        ('110012', 'Patê de Presunto Sadia', 'Carne suína, água, amido, proteína de soja.', 'en:soybeans', ''),
        ('110013', 'Picles em Conserva', 'Pepino, vinagre, sal.', '', ''),

        # ==========================================
        # 🥓 FRIOS, EMBUTIDOS E LATICÍNIOS EXTRAS
        # ==========================================
        ('120001', 'Presunto Cozido Sadia', 'Carne suína, água, sal, proteína de soja.', 'en:soybeans', ''),
        ('120002', 'Mortadela Bologna Perdigão', 'Carnes, gordura suína, água, proteína de soja.', 'en:soybeans', ''),
        ('120003', 'Salsicha Hot Dog Sadia', 'Carne de ave, carne suína, proteína de soja.', 'en:soybeans', ''),
        ('120004', 'Linguiça Calabresa Perdigão', 'Carne suína, carne mecanicamente separada, soja.', 'en:soybeans', ''),
        ('120005', 'Linguiça Toscana Seara', 'Carne suína, água, sal, especiarias.', '', ''),
        ('120006', 'Peito de Peru Defumado Sadia', 'Peito de peru, água, sal, proteína de soja.', 'en:soybeans', ''),
        ('120007', 'Salame Milano Sadia', 'Carne suína, toucinho, sal, leite em pó.', 'en:milk', ''),
        ('120008', 'Pepperoni Seara', 'Carne suína, carne bovina, especiarias.', '', ''),
        ('120009', 'Bacon em Fatias Sadia', 'Barriga suína, sal, conservantes.', '', ''),
        ('120010', 'Frango Inteiro Congelado Sadia', 'Cortes de frango.', '', ''),
        ('120011', 'Coxa e Sobrecoxa Congelada Perdigão', 'Cortes de frango.', '', ''),
        ('120012', 'Filé de Frango Congelado Seara', 'Peito de frango desossado.', '', ''),
        ('120013', 'Hambúrguer Bovino Friboi', 'Carne bovina, água, gordura, proteína de soja.', 'en:soybeans', ''),
        ('120014', 'Nuggets de Frango Sadia', 'Carne de frango, farinha de trigo, óleo, soja.', 'en:gluten, en:soybeans', ''),
        ('120015', 'Almôndega de Carne Seara', 'Carne bovina, carne de ave, farinha de trigo, soja.', 'en:gluten, en:soybeans', ''),
        ('120016', 'Carne Bovina Moída Congelada', 'Carne bovina.', '', ''),
        ('120017', 'Costela Suína Congelada', 'Costela suína.', '', ''),
        ('120018', 'Queijo Brie', 'Leite pasteurizado, fermento lácteo, mofo branco.', 'en:milk', ''),
        ('120019', 'Queijo Gouda', 'Leite pasteurizado, sal, coalho, corante natural.', 'en:milk', ''),
        ('120020', 'Queijo Cheddar Fatiado', 'Leite pasteurizado, sal, coalho, corante natural.', 'en:milk', ''),
        ('120021', 'Queijo Provolone', 'Leite pasteurizado, sal, coalho, defumação.', 'en:milk', ''),
        ('120022', 'Queijo Ricota', 'Soro de leite, leite pasteurizado.', 'en:milk', ''),
        ('120023', 'Queijo Cottage', 'Leite desnatado pasteurizado, creme de leite, sal.', 'en:milk', ''),
        ('120024', 'Iogurte Grego Zero', 'Leite desnatado, fermento lácteo, edulcorantes.', 'en:milk', ''),
        ('120025', 'Petit Suisse de Morango', 'Leite, açúcar, preparado de morango.', 'en:milk', ''),
        ('120026', 'Bebida Láctea Fermentada Yakult', 'Leite desnatado, açúcar, lactobacilos vivos.', 'en:milk', ''),
        ('120027', 'Manteiga Ghee', 'Manteiga clarificada.', 'en:milk', ''),
        ('120028', 'Nata Fresca', 'Creme de leite pasteurizado.', 'en:milk', ''),
        ('120029', 'Creme Duplo de Leite', 'Creme de leite com alto teor de gordura.', 'en:milk', ''),
        ('120030', 'Muçarela de Búfala', 'Leite de búfala pasteurizado, sal, coalho.', 'en:milk', ''),
        ('120031', 'Iogurte Natural sem Lactose', 'Leite integral, enzima lactase, fermento lácteo.', 'en:milk', ''),

        # ==========================================
        # 🍪 BISCOITOS E SALGADINHOS
        # ==========================================
        ('130001', 'Biscoito Cream Cracker', 'Farinha de trigo, gordura vegetal, sal, extrato de malte.', 'en:gluten, en:soybeans', ''),
        ('130002', 'Biscoito Maria', 'Farinha de trigo, açúcar, gordura vegetal, leite em pó.', 'en:gluten, en:milk, en:soybeans', ''),
        ('130003', 'Biscoito Maizena', 'Farinha de trigo, açúcar, gordura vegetal, amido.', 'en:gluten, en:soybeans', ''),
        ('130004', 'Biscoito Recheado Oreo', 'Farinha de trigo, açúcar, gordura vegetal, cacau.', 'en:gluten, en:soybeans', ''),
        ('130005', 'Biscoito Recheado Bono', 'Farinha de trigo, açúcar, gordura vegetal, soro de leite.', 'en:gluten, en:milk, en:soybeans', ''),
        ('130006', 'Biscoito Recheado Passatempo', 'Farinha de trigo, açúcar, gordura, leite em pó.', 'en:gluten, en:milk, en:soybeans', ''),
        ('130007', 'Biscoito Wafer Baunilha', 'Açúcar, farinha de trigo, gordura vegetal, leite.', 'en:gluten, en:milk, en:soybeans', ''),
        ('130008', 'Biscoito Wafer Chocolate', 'Açúcar, farinha de trigo, gordura vegetal, cacau.', 'en:gluten, en:soybeans', ''),
        ('130009', 'Biscoito de Polvilho Yoki', 'Polvilho, óleo vegetal, ovos, leite.', 'en:eggs, en:milk', ''),
        ('130010', 'Biscoito Triunfo Água e Sal', 'Farinha de trigo, gordura, extrato de malte.', 'en:gluten, en:soybeans', ''),
        ('130011', 'Salgadinho Cheetos', 'Sêmola de milho, óleo vegetal, queijo em pó.', 'en:milk, en:soybeans', ''),
        ('130012', 'Salgadinho Ruffles Original', 'Batata, óleo vegetal, sal.', 'en:soybeans', ''),
        ('130013', 'Salgadinho Doritos Nacho', 'Milho, óleo vegetal, preparado sabor queijo.', 'en:milk, en:soybeans', ''),
        ('130014', 'Salgadinho Fandangos', 'Farinha de milho, óleo vegetal, preparado sabor queijo.', 'en:milk, en:soybeans', ''),
        ('130015', 'Pipoca de Micro-ondas Manteiga', 'Milho, gordura vegetal, sal, aroma de manteiga.', 'en:milk', ''),
        ('130016', 'Pipoca de Micro-ondas Natural', 'Milho para pipoca, sal.', '', ''),
        ('130017', 'Barra de Cereal', 'Aveia, xarope de glicose, flocos de arroz, castanhas.', 'en:gluten, en:nuts', ''),
        ('130018', 'Torrada Integral', 'Farinha de trigo integral, farinha de trigo enriquecida, gordura vegetal.', 'en:gluten, en:soybeans', ''),

        # ==========================================
        # 🍫 CHOCOLATES E DOCES
        # ==========================================
        ('140001', 'Chocolate ao Leite Lacta', 'Açúcar, leite em pó integral, massa de cacau, manteiga de cacau.', 'en:milk, en:soybeans', ''),
        ('140002', 'Chocolate Charge', 'Açúcar, xarope de glicose, amendoim, leite condensado, massa de cacau.', 'en:milk, en:peanuts, en:soybeans', ''),
        ('140003', 'Chocolate Bis', 'Açúcar, farinha de trigo, cacau, amendoim, leite em pó.', 'en:gluten, en:peanuts, en:milk, en:soybeans', ''),
        ('140004', 'Chocolate Diamante Negro', 'Açúcar, massa de cacau, manteiga de cacau, leite em pó, mel, castanha-de-caju.', 'en:milk, en:nuts, en:soybeans', ''),
        ('140005', 'Chocolate Laka', 'Açúcar, manteiga de cacau, leite em pó integral.', 'en:milk, en:soybeans', ''),
        ('140006', 'Chocolate Suflair', 'Açúcar, leite em pó, manteiga de cacau, liquor de cacau.', 'en:milk, en:soybeans', ''),
        ('140007', 'Chocolate Kit Kat', 'Açúcar, leite em pó, manteiga de cacau, farinha de trigo.', 'en:gluten, en:milk, en:soybeans', ''),
        ('140008', 'Chocolate Alpino', 'Açúcar, leite em pó integral, massa de cacau, manteiga de cacau.', 'en:milk, en:soybeans', ''),
        ('140009', 'Chocolate Twix', 'Açúcar, xarope de glicose, farinha de trigo, leite em pó.', 'en:gluten, en:milk, en:soybeans', ''),
        ('140010', 'Chocolate Snickers', 'Açúcar, amendoim, xarope de glicose, leite em pó.', 'en:peanuts, en:milk, en:soybeans', ''),
        ('140011', 'Chocolate M&Ms', 'Açúcar, massa de cacau, leite em pó integral.', 'en:milk, en:soybeans', ''),
        ('140012', 'Barra de Chocolate 70% Cacau', 'Massa de cacau, açúcar, cacau em pó, emulsificantes.', 'en:soybeans', ''),
        ('140013', 'Doce de Leite', 'Leite integral, açúcar.', 'en:milk', ''),
        ('140014', 'Goiabada', 'Polpa de goiaba, açúcar, acidulante.', '', ''),
        ('140015', 'Geleia de Morango', 'Morango, açúcar, pectina.', '', ''),
        ('140016', 'Mel Silvestre', 'Mel de abelhas.', '', ''),
        ('140017', 'Paçoca', 'Amendoim, açúcar, sal.', 'en:peanuts', ''),
        ('140018', 'Cocada', 'Coco ralado, açúcar.', '', ''),

        # ==========================================
        # 🥐 PADARIA E MATINAIS
        # ==========================================
        ('150001', 'Pão de Forma Integral', 'Farinha de trigo integral, farinha de trigo enriquecida, glúten.', 'en:gluten, en:soybeans', ''),
        ('150002', 'Pão de Forma Tradicional', 'Farinha de trigo enriquecida, açúcar, óleo de soja.', 'en:gluten, en:soybeans', ''),
        ('150003', 'Torrada Tradicional', 'Farinha de trigo, gordura vegetal, sal.', 'en:gluten, en:soybeans', ''),
        ('150004', 'Panetone com Frutas', 'Farinha de trigo, frutas cristalizadas, uvas passas, ovo, leite.', 'en:gluten, en:eggs, en:milk, en:soybeans', ''),
        ('150005', 'Panetone com Gotas de Chocolate', 'Farinha de trigo, gotas de chocolate, ovo, leite.', 'en:gluten, en:eggs, en:milk, en:soybeans', ''),
        ('150006', 'Cereal Matinal Sucrilhos', 'Milho, açúcar, extrato de malte.', 'en:gluten', ''),
        ('150007', 'Cereal Matinal Corn Flakes', 'Milho, açúcar, sal.', '', ''),
        ('150008', 'Granola Tradicional', 'Aveia, flocos de milho, mel, uva passa, castanhas.', 'en:gluten, en:nuts', ''),
        ('150009', 'Granola Original', 'Aveia em flocos, açúcar mascavo, castanhas.', 'en:gluten, en:nuts', ''),
        ('150010', 'Farinha Láctea', 'Farinha de trigo, leite em pó, açúcar.', 'en:gluten, en:milk', ''),
        ('150011', 'Mel de Abelha', 'Mel puro.', '', ''),

        # ==========================================
        # 🍨 SOBREMESAS E GELATINAS
        # ==========================================
        ('160001', 'Gelatina de Morango', 'Açúcar, gelatina, reguladores de acidez.', '', ''),
        ('160002', 'Gelatina de Uva', 'Açúcar, gelatina, aromatizantes.', '', ''),
        ('160003', 'Pudim de Baunilha', 'Açúcar, amido, aromatizante, corantes.', '', ''),
        ('160004', 'Creme para Sobremesa', 'Leite pasteurizado, açúcar, espessantes.', 'en:milk', ''),
        ('160005', 'Sorvete de Creme', 'Água, açúcar, gordura vegetal, soro de leite.', 'en:milk, en:soybeans', ''),
        ('160006', 'Picolé de Chocolate', 'Água, leite em pó, açúcar, cacau.', 'en:milk, en:soybeans', ''),
        ('160007', 'Sorvete de Morango', 'Água, açúcar, gordura vegetal, leite desnatado.', 'en:milk', ''),
        ('160008', 'Açaí em Polpa 1kg', 'Polpa de açaí, água, xarope de guaraná.', '', ''),
        ('160009', 'Polpa de Frutas Maracujá', 'Polpa de maracujá pasteurizada.', '', ''),

        # ==========================================
        # 🥦 HORTIFRÚTI PROCESSADO
        # ==========================================
        ('170001', 'Batata Palha Yoki', 'Batata, óleo vegetal, sal.', 'en:soybeans', ''),
        ('170002', 'Batata Chips', 'Batata, óleo vegetal, sal.', 'en:soybeans', ''),
        ('170003', 'Cenoura Baby em Embalagem', 'Cenouras miniatura.', '', ''),
        ('170004', 'Alho Descascado em Embalagem', 'Dentes de alho frescos.', '', ''),
        ('170005', 'Cebola Desidratada', 'Cebola seca.', '', ''),
        ('170006', 'Tomate Cereja Embalado', 'Tomates cereja in natura.', '', ''),

        # ==========================================
        # 🥜 PASTAS, CREMES E SPREADS
        # ==========================================
        ('180001', 'Creme de Avelã Nutella', 'Açúcar, óleo de palma, avelãs, cacau, leite em pó.', 'en:milk, en:nuts, en:soybeans', ''),
        ('180002', 'Creme de Avelã Nutella Biscuit', 'Farinha de trigo, açúcar, avelãs, cacau.', 'en:gluten, en:milk, en:nuts', ''),
        ('180003', 'Pasta de Amendoim Integral', 'Amendoim torrado.', 'en:peanuts', ''),
        ('180004', 'Pasta de Amendoim Crocante', 'Amendoim torrado.', 'en:peanuts', ''),
        ('180005', 'Pasta de Amendoim Cremosa', 'Amendoim torrado.', 'en:peanuts', ''),
        ('180006', 'Geleia de Jabuticaba', 'Jabuticaba, açúcar, pectina.', '', ''),
        ('180007', 'Geleia de Frutas Vermelhas', 'Frutas vermelhas, açúcar, pectina.', '', ''),
        ('180008', 'Geleia de Laranja', 'Laranja, açúcar, pectina.', '', ''),
        ('180009', 'Doce de Banana', 'Banana, açúcar.', '', ''),
        ('180010', 'Creme de Ricota', 'Soro de leite, creme de leite, sal.', 'en:milk', ''),
        ('180011', 'Tahine', 'Sementes de gergelim torradas e moídas.', 'en:sesame', ''),

        # ==========================================
        # 🍿 SNACKS E PETISCOS
        # ==========================================
        ('190001', 'Amendoim Japonês', 'Amendoim, farinha de trigo, molho de soja, sal.', 'en:gluten, en:peanuts, en:soybeans', ''),
        ('190002', 'Amendoim Torrado com Sal', 'Amendoim, óleo vegetal, sal.', 'en:peanuts', ''),
        ('190003', 'Amendoim Crocante', 'Amendoim, farinha de trigo, amido, sal.', 'en:gluten, en:peanuts', ''),
        ('190004', 'Castanha de Caju Torrada', 'Castanha de caju, sal.', 'en:nuts', ''),
        ('190005', 'Mix de Nuts', 'Amendoim, castanha de caju, castanha do pará, uva passa.', 'en:peanuts, en:nuts', ''),
        ('190006', 'Nozes', 'Nozes sem casca.', 'en:nuts', ''),
        ('190007', 'Uva Passa Sultana', 'Uvas passas brancas.', '', ''),
        ('190008', 'Damasco Seco', 'Damasco desidratado.', '', ''),
        ('190009', 'Banana Passa', 'Banana desidratada.', '', ''),
        ('190010', 'Coco Ralado', 'Coco desidratado.', '', ''),
        ('190011', 'Pipoca Pronta de Queijo', 'Milho, óleo vegetal, queijo em pó.', 'en:milk, en:soybeans', ''),
        ('190012', 'Snack de Arroz Integral', 'Arroz integral, sal.', '', ''),
        ('190013', 'Batatinha Frita Pringles', 'Batata, óleo vegetal, farinha de milho, amido.', 'en:soybeans', ''),
        ('190014', 'Pretzel Salgado', 'Farinha de trigo, óleo vegetal, sal.', 'en:gluten', ''),
        ('190015', 'Torrada Italiana', 'Farinha de trigo, azeite, sal.', 'en:gluten', ''),
        ('190016', 'Coxinha Congelada', 'Farinha de trigo, frango, caldo de galinha, óleo.', 'en:gluten, en:soybeans', ''),
        ('190017', 'Empanado de Frango Congelado', 'Carne de frango, farinha de trigo, água.', 'en:gluten, en:soybeans', ''),
        ('190018', 'Kibe Congelado', 'Carne bovina, trigo para kibe, hortelã, cebola.', 'en:gluten', ''),
        ('190019', 'Pastel Congelado', 'Farinha de trigo, água, sal.', 'en:gluten', ''),
        ('190020', 'Mini Pizza Congelada', 'Farinha de trigo, queijo, molho de tomate.', 'en:gluten, en:milk', ''),
        ('190021', 'Croissant Congelado', 'Farinha de trigo, manteiga, água, fermento.', 'en:gluten, en:milk', ''),
        ('190022', 'Pão de Queijo Congelado', 'Polvilho, queijo, ovos, óleo vegetal.', 'en:eggs, en:milk', ''),

        # ==========================================
        # 🍲 REFEIÇÕES PRONTAS E MASSAS
        # ==========================================
        ('200001', 'Lasanha Bolonhesa Congelada', 'Massa para lasanha, carne moída, queijo, molho.', 'en:gluten, en:milk', ''),
        ('200002', 'Lasanha 4 Queijos Congelada', 'Massa, queijo mussarela, parmesão, provolone, gorgonzola.', 'en:gluten, en:milk', ''),
        ('200003', 'Frango Grelhado Congelado', 'Peito de frango, temperos.', '', ''),
        ('200004', 'Peixe Empanado Congelado', 'Filé de peixe, farinha de rosca, óleo vegetal.', 'en:fish, en:gluten', ''),
        ('200005', 'Estrogonofe de Frango Pronto', 'Frango, creme de leite, champignon, ketchup.', 'en:milk', ''),
        ('200006', 'Arroz Integral Cozido Vapor', 'Arroz integral cozido.', '', ''),
        ('200007', 'Feijão Cozido em Lata', 'Feijão, água, sal.', '', ''),
        ('200008', 'Lentilha Cozida em Lata', 'Lentilha, água, sal.', '', ''),
        ('200009', 'Sopão Carne e Legumes', 'Macarrão, carne desidratada, legumes desidratados.', 'en:gluten, en:soybeans', ''),
        ('200010', 'Caldo de Feijão Knorr', 'Sal, gordura vegetal, extrato de feijão.', 'en:soybeans', ''),
        ('200011', 'Purê de Batata Instantâneo', 'Flocos de batata desidratada.', 'en:milk', ''),
        ('200012', 'Macarrão ao Molho Sugo', 'Macarrão cozido, molho de tomate.', 'en:gluten', ''),

        # ==========================================
        # 🍅 MOLHOS PRONTOS
        # ==========================================
        ('210001', 'Molho Barbecue', 'Polpa de tomate, açúcar, vinagre, aroma de fumaça.', '', ''),
        ('210002', 'Molho Caesar', 'Água, óleo vegetal, queijo, alho, vinagre.', 'en:milk, en:eggs', ''),
        ('210003', 'Molho Ranch', 'Óleo vegetal, água, soro de leite, alho, cebola.', 'en:milk', ''),
        ('210004', 'Molho Pesto', 'Manjericão, óleo de girassol, queijo, castanhas.', 'en:milk, en:nuts', ''),
        ('210005', 'Molho Bolonhesa Pronto', 'Tomate, carne bovina, cenoura, cebola.', '', ''),
        ('210006', 'Molho Carbonara Pronto', 'Creme de leite, bacon, queijo parmesão, gema de ovo.', 'en:milk, en:eggs', ''),
        ('210007', 'Molho de Tomate com Manjericão', 'Tomate, manjericão, sal, óleo.', '', ''),
        ('210008', 'Molho de Tomate com Alho', 'Tomate, alho, sal, azeite.', '', ''),
        ('210009', 'Molho de Pimenta Sriracha', 'Pimenta jalapeño, açúcar, sal, alho.', '', ''),
        ('210010', 'Molho Teriyaki', 'Molho de soja, açúcar, vinho, especiarias.', 'en:soybeans, en:gluten', ''),
        ('210011', 'Molho Inglês', 'Vinagre, melaço, açúcar, anchovas, especiarias.', 'en:fish', ''),
        ('210012', 'Molho de Ostras', 'Água, açúcar, sal, extrato de ostra.', 'en:molluscs', ''),

        # ==========================================
        # 🧃 BEBIDAS ESPECIAIS E FUNCIONAIS
        # ==========================================
        ('220001', 'Suco Cold Press Laranja', 'Laranja prensada a frio.', '', ''),
        ('220002', 'Kombucha Original', 'Água, cultura kombucha, chá verde, açúcar.', '', ''),
        ('220003', 'Água de Coco com Polpa', 'Água de coco, polpa de coco.', '', ''),
        ('220004', 'Leite de Aveia', 'Água, aveia.', 'en:gluten', ''),
        ('220005', 'Leite de Amêndoas', 'Água, pasta de amêndoas.', 'en:nuts', ''),
        ('220006', 'Leite de Coco', 'Leite de coco, água.', '', ''),
        ('220007', 'Leite de Soja', 'Água, grãos de soja.', 'en:soybeans', ''),
        ('220008', 'Bebida de Soja Baunilha', 'Água, grãos de soja, açúcar, aroma de baunilha.', 'en:soybeans', ''),
        ('220009', 'Bebida Láctea de Morango', 'Soro de leite, leite, preparado de morango.', 'en:milk', ''),
        ('220010', 'Achocolatado Toddynho', 'Soro de leite, leite integral, cacau, açúcar.', 'en:milk', ''),
        ('220011', 'Iogurte para Beber Danone', 'Leite reconstituído, açúcar, fermento.', 'en:milk', ''),
        ('220012', 'Bebida de Iogurte Grego', 'Leite, fermento lácteo, preparado de frutas.', 'en:milk', ''),

        # ==========================================
        # 🌾 CEREALISTAS E FUNCIONAIS
        # ==========================================
        ('230001', 'Chia', 'Sementes de chia.', '', ''),
        ('230002', 'Linhaça Dourada', 'Sementes de linhaça dourada.', '', ''),
        ('230003', 'Quinoa em Grão', 'Grãos de quinoa.', '', ''),
        ('230004', 'Amaranto', 'Grãos de amaranto.', '', ''),
        ('230005', 'Gérmen de Trigo', 'Gérmen de trigo tostado.', 'en:gluten', ''),
        ('230006', 'Farelo de Aveia', 'Farelo de aveia.', 'en:gluten', ''),
        ('230007', 'Biomassa de Banana Verde', 'Polpa de banana verde cozida.', '', ''),
        ('230008', 'Proteína de Soja Texturizada', 'Proteína isolada de soja.', 'en:soybeans', ''),
        ('230009', 'Arroz Negro', 'Arroz negro em grãos.', '', ''),
        ('230010', 'Arroz Vermelho', 'Arroz vermelho em grãos.', '', ''),
        ('230011', 'Whey Protein Chocolate', 'Proteína do soro do leite, cacau, edulcorantes.', 'en:milk, en:soybeans', ''),
        ('230012', 'Whey Protein Baunilha', 'Proteína do soro do leite, aroma de baunilha.', 'en:milk, en:soybeans', ''),
        ('230013', 'Barra Proteica', 'Proteína do leite, cobertura de chocolate, amendoim.', 'en:milk, en:peanuts, en:soybeans', ''),
        ('230014', 'Granola Proteica', 'Aveia, flocos de soja, castanhas, proteína do soro do leite.', 'en:gluten, en:soybeans, en:nuts, en:milk', ''),

        # ==========================================
        # 🧁 PANIFICAÇÃO E CONFEITARIA
        # ==========================================
        ('240001', 'Fermento Biológico Fleischmann', 'Saccharomyces cerevisiae.', '', ''),
        ('240002', 'Cacau em Pó Sicao', 'Cacau em pó.', '', ''),
        ('240003', 'Chocolate em Pó Nestlé', 'Cacau em pó, açúcar.', '', ''),
        ('240004', 'Cobertura de Chocolate Harald', 'Açúcar, gordura vegetal, cacau em pó.', 'en:soybeans', ''),
        ('240005', 'Granulado de Chocolate', 'Açúcar, gordura vegetal, cacau, amido.', 'en:soybeans', ''),
        ('240006', 'Creme de Confeiteiro', 'Amido de milho, açúcar, corantes, aroma de baunilha.', 'en:milk', ''),
        ('240007', 'Leite de Coco para Culinária', 'Extrato de coco, água.', '', ''),
        ('240008', 'Essência de Baunilha', 'Água, álcool, aroma artificial de baunilha.', '', ''),
        ('240009', 'Corante Alimentício', 'Água, corantes artificiais.', '', ''),
        ('240010', 'Gelatina sem Sabor', 'Gelatina em pó de origem animal.', '', ''),
        ('240011', 'Agar Agar', 'Extrato de algas marinhas (agar-agar).', '', ''),
        ('240012', 'Waffle Congelado', 'Farinha de trigo, água, óleo vegetal, ovos.', 'en:gluten, en:eggs', ''),
        ('240013', 'Massa de Pizza Congelada', 'Farinha de trigo, água, fermento, sal.', 'en:gluten', ''),
        ('240014', 'Massa Folhada Congelada', 'Farinha de trigo, margarina, água, sal.', 'en:gluten, en:soybeans', ''),
        ('240015', 'Pão Sírio', 'Farinha de trigo, água, fermento.', 'en:gluten', ''),
        ('240016', 'Wrap de Trigo', 'Farinha de trigo, água, óleo, sal.', 'en:gluten', ''),
        ('240017', 'Bisnaguinha', 'Farinha de trigo, açúcar, leite, ovos.', 'en:gluten, en:milk, en:eggs', ''),

        # ==========================================
        # 🥢 PRODUTOS ORIENTAIS E ÉTNICOS
        # ==========================================
        ('250001', 'Shoyu Kikkoman', 'Água, soja, trigo, sal.', 'en:soybeans, en:gluten', ''),
        ('250002', 'Missô', 'Soja, arroz, sal, fermento.', 'en:soybeans', ''),
        ('250003', 'Alga Nori', 'Alga marinha seca.', '', ''),
        ('250004', 'Arroz para Sushi', 'Arroz de grão curto.', '', ''),
        ('250005', 'Vinagre de Arroz', 'Água, fermentado acético de arroz.', '', ''),
        ('250006', 'Macarrão Soba', 'Farinha de trigo sarraceno, farinha de trigo, água.', 'en:gluten', ''),
        ('250007', 'Macarrão Udon', 'Farinha de trigo, água, sal.', 'en:gluten', ''),
        ('250008', 'Gengibre em Conserva', 'Gengibre, água, vinagre, açúcar.', '', ''),
        ('250009', 'Wasabi em Pasta', 'Raiz forte, mostarda, corantes.', 'en:mustard', ''),
        ('250010', 'Leite de Coco Tailandês', 'Extrato de coco, água.', '', ''),
        ('250011', 'Pasta de Curry Vermelho', 'Pimenta, alho, capim-limão, chalota, sal.', '', ''),
        ('250012', 'Macarrão de Arroz', 'Farinha de arroz, água.', '', ''),
        ('250013', 'Tempurá em Pó', 'Farinha de trigo, amido de milho, fermento.', 'en:gluten', ''),
        ('250014', 'Feijão Azuki', 'Feijão azuki em grãos.', '', ''),

        # ==========================================
        # 🐟 FRUTOS DO MAR E PEIXES
        # ==========================================
        ('260001', 'Camarão Congelado VG', 'Camarão descascado congelado.', 'en:crustaceans', ''),
        ('260002', 'Filé de Tilápia Congelado', 'Filé de tilápia.', 'en:fish', ''),
        ('260003', 'Filé de Salmão Congelado', 'Filé de salmão.', 'en:fish', ''),
        ('260004', 'Bacalhau Salgado Seco', 'Bacalhau, sal.', 'en:fish', ''),
        ('260005', 'Lula em Anéis Congelada', 'Lula em anéis.', 'en:molluscs', ''),
        ('260006', 'Mexilhão Congelado', 'Mexilhão sem concha.', 'en:molluscs', ''),
        ('260007', 'Polvo Congelado', 'Tentáculos de polvo.', 'en:molluscs', ''),
        ('260008', 'Atum Fresco Congelado', 'Postas de atum.', 'en:fish', ''),

        # ==========================================
        # 🥩 CARNES ESPECIAIS E FRIOS
        # ==========================================
        ('270001', 'Peito de Frango sem Osso', 'Cortes de peito de frango.', '', ''),
        ('270002', 'Filé de Frango Temperado', 'Peito de frango, água, sal, condimentos.', '', ''),
        ('270003', 'Contrafilé Bovino', 'Contrafilé bovino in natura.', '', ''),
        ('270004', 'Picanha Bovina', 'Picanha bovina in natura.', '', ''),
        ('270005', 'Costela Bovina', 'Costela bovina in natura.', '', ''),
        ('270006', 'Bisteca Suína', 'Bisteca suína in natura.', '', ''),
        ('270007', 'Lombo Suíno', 'Lombo suíno in natura.', '', ''),
        ('270008', 'Pernil Suíno', 'Pernil suíno in natura.', '', ''),
        ('270009', 'Fraldinha Bovina', 'Fraldinha bovina in natura.', '', ''),
        ('270010', 'Cordeiro Congelado', 'Cortes de cordeiro.', '', ''),
        ('270011', 'Carne de Pato Congelada', 'Cortes de pato.', '', ''),

        # ==========================================
        # 🍩 SOBREMESAS INDUSTRIAIS E CAFÉ
        # ==========================================
        ('280001', 'Brownie Bauducco', 'Açúcar, ovos, farinha de trigo, cacau.', 'en:gluten, en:eggs, en:soybeans', ''),
        ('280002', 'Churros Congelado', 'Farinha de trigo, água, margarina.', 'en:gluten, en:soybeans', ''),
        ('280003', 'Bolo de Rolo', 'Açúcar, farinha de trigo, ovos, manteiga, goiabada.', 'en:gluten, en:eggs, en:milk', ''),
        ('280004', 'Torta de Limão Congelada', 'Farinha, leite condensado, suco de limão, creme de leite.', 'en:gluten, en:milk', ''),
        ('280005', 'Pudim de Leite Pronto', 'Leite, leite condensado, ovos, açúcar.', 'en:milk, en:eggs', ''),
        ('280006', 'Musse de Maracujá', 'Creme de leite, leite condensado, suco de maracujá.', 'en:milk', ''),
        ('280007', 'Danette Chocolate', 'Leite, açúcar, cacau, amido.', 'en:milk', ''),
        ('280008', 'Danoninho', 'Leite, açúcar, queijo petit suisse, morango.', 'en:milk', ''),
        ('280009', 'Palito de Sorvete Cornetto', 'Água, açúcar, gordura vegetal, casquinha de biscoito.', 'en:milk, en:gluten', ''),
        ('280010', 'Sorvete Magnum', 'Leite, açúcar, cobertura de chocolate, amêndoas.', 'en:milk, en:nuts', ''),
        ('280011', 'Sorvete La Frutta', 'Água, açúcar, suco de frutas.', '', ''),
        ('280012', 'Açaí com Granola', 'Polpa de açaí, guaraná, aveia, mel.', 'en:gluten', ''),
        ('280013', 'Brigadeiro Pronto', 'Leite condensado, cacau, margarina.', 'en:milk', ''),
        ('280014', 'Pão de Mel', 'Farinha de trigo, mel, especiarias, cobertura de chocolate.', 'en:gluten, en:milk, en:soybeans', ''),
        ('280015', 'Bolinho Donuts', 'Farinha de trigo, açúcar, óleo, cobertura.', 'en:gluten, en:eggs, en:milk', ''),
        ('280016', 'Bolo Tipo Inglês', 'Farinha de trigo, ovos, açúcar, frutas cristalizadas.', 'en:gluten, en:eggs', ''),
        ('280017', 'Wafer Recheado de Morango', 'Açúcar, farinha de trigo, gordura, aroma de morango.', 'en:gluten, en:milk, en:soybeans', ''),
        ('280018', 'Biscoito Recheado Negresco', 'Farinha de trigo, açúcar, gordura, cacau.', 'en:gluten, en:soybeans', ''),
        ('280019', 'Biscoito Recheado Trakinas', 'Farinha de trigo, açúcar, gordura, leite em pó.', 'en:gluten, en:milk, en:soybeans', ''),
        ('280020', 'Biscoito Amanteigado', 'Farinha de trigo, manteiga, açúcar.', 'en:gluten, en:milk', ''),
        ('280021', 'Biscoito Champagne', 'Farinha de trigo, açúcar, ovos.', 'en:gluten, en:eggs', ''),
        ('280022', 'Rosquinha de Coco', 'Farinha de trigo, açúcar, coco ralado.', 'en:gluten', ''),
        ('280023', 'Bala de Goma Fini', 'Xarope de glicose, açúcar, gelatina.', '', ''),
        ('280024', 'Bala de Goma Trolli', 'Xarope de glicose, açúcar, gelatina, corantes.', '', ''),
        ('280025', 'Bala Mentos', 'Açúcar, xarope de glicose, óleo vegetal.', '', ''),
        ('280026', 'Chiclete Trident', 'Goma base, edulcorantes, aromatizantes.', '', ''),
        ('280027', 'Chiclete Halls', 'Açúcar, xarope de glicose, mentol.', '', ''),
        ('280028', 'Pirulito Chupa Chups', 'Açúcar, xarope de glicose, purê de frutas.', '', ''),

        # ==========================================
        # 🥭 POLPAS E FRUTAS PROCESSADAS
        # ==========================================
        ('290001', 'Polpa de Acerola', 'Polpa de acerola pasteurizada.', '', ''),
        ('290002', 'Polpa de Caju', 'Polpa de caju pasteurizada.', '', ''),
        ('290003', 'Polpa de Goiaba', 'Polpa de goiaba pasteurizada.', '', ''),
        ('290004', 'Polpa de Cupuaçu', 'Polpa de cupuaçu pasteurizada.', '', ''),
        ('290005', 'Polpa de Pitanga', 'Polpa de pitanga pasteurizada.', '', ''),
        ('290006', 'Uva Passa Preta', 'Uva passa escura sem semente.', '', ''),
        ('290007', 'Ameixa Seca', 'Ameixas desidratadas sem caroço.', '', ''),
        ('290008', 'Tâmara', 'Tâmaras secas.', '', ''),
        ('290009', 'Figo Seco', 'Figo desidratado.', '', ''),
        ('290010', 'Abacaxi em Calda', 'Abacaxi, água, açúcar.', '', ''),
        ('290011', 'Pêssego em Calda', 'Pêssegos, água, açúcar.', '', ''),
        ('290012', 'Cocktail de Frutas', 'Frutas mistas, água, açúcar.', '', ''),

        # ==========================================
        # 🥗 DIET, LIGHT E SEM GLÚTEN
        # ==========================================
        ('300001', 'Biscoito sem Glúten', 'Farinha de arroz, fécula de batata, açúcar.', '', ''),
        ('300002', 'Macarrão sem Glúten', 'Farinha de arroz, farinha de milho.', '', ''),
        ('300003', 'Pão sem Glúten', 'Farinha de arroz, fécula de mandioca, óleo vegetal.', '', ''),
        ('300004', 'Farinha de Amêndoas', 'Amêndoas moídas.', 'en:nuts', ''),
        ('300005', 'Farinha de Arroz', 'Grãos de arroz moídos.', '', ''),
        ('300006', 'Cereal de Milho sem Açúcar', 'Flocos de milho.', '', ''),
        ('300007', 'Iogurte Zero Lactose', 'Leite, fermento lácteo, enzima lactase.', 'en:milk', ''),
        ('300008', 'Leite sem Lactose', 'Leite integral, enzima lactase.', 'en:milk', ''),
        ('300009', 'Chocolate Diet', 'Massa de cacau, edulcorantes, leite em pó.', 'en:milk, en:soybeans', ''),
        ('300010', 'Refrigerante Zero Açúcar Coca-Cola', 'Água gaseificada, extrato de noz de cola, edulcorantes.', '', ''),
        ('300011', 'Refrigerante Zero Pepsi', 'Água gaseificada, extrato de cola, edulcorantes.', '', ''),
        ('300012', 'Biscoito Integral', 'Farinha de trigo integral, aveia, açúcar mascavo.', 'en:gluten', '')
    ]

    # Usamos REPLACE para evitar erros de duplicação caso você rode o script mais de uma vez
    cursor.executemany('''
        REPLACE INTO alimentos (codigo_barras, nome, ingredientes, alergenicos, imagem_url)
        VALUES (?, ?, ?, ?, ?)
    ''', produtos)

    conexao.commit()
    conexao.close()
    
    print(f"✅ SUCESSO ABSOLUTO! {len(produtos)} produtos do seu catálogo foram injetados no Banco de Dados.")
    print("🚀 O seu NutriCheck agora está pronto para filtrar com segurança o supermercado inteiro!")

if __name__ == '__main__':
    abastecer()