import xml.etree.ElementTree as ET

def sitemap_insert(file, nova_url,data):
    #Leitura do arquivo 1
    tree = ET.parse(file)
    root = tree.getroot()

    #Criando nova inserção
    new_url = ET.SubElement(root, 'url')
    new_loc = ET.SubElement(new_url, 'loc')
    new_lastmod = ET.SubElement(new_url, 'lastmod')
    #Dados do texto do subelemento 
    new_loc.text =  nova_url
    new_lastmod.text = data
    # linha de comando abaixo retira os ns0 ("namespace criados pela tag xmls")
    ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9')
    #Salvar alterações
    tree.write(file)

def sitemap_delete(file,url_delete):
    #Leitura do arquivo xml
    xmls = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    tree = ET.parse(file)
    root = tree.getroot()
    #Remover item do xml
    for url in root.findall(xmls+'url'):
        # using root.findall() to avoid removal during traversal
        loc = url.find(xmls+'loc').text    
        if loc == url_delete:
            root.remove(url)
    # linha de comando abaixo retira os ns0 ("namespace criados pela tag xmls")
    ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9')
    #Salvar alterações
    tree.write(file)

def merge_xml(file1, file2, output):
    #leitura dos arquivos a serem mesclados
    xmls = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    tree1 = ET.parse(file1)
    tree2 = ET.parse(file2)
    root1 = tree1.getroot()
    root2 = tree2.getroot()
    # mesclagem do file2 em file1
    root1.extend(root2)
    # linha de comando abaixo retira os ns0 ("namespace criados pela tag xmls")
    ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9')
    # salvando os arquivos mesclados
    tree1.write(output)

def xml_url(file):
    xmls = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    tree = ET.parse(file)
    root = tree.getroot()
    list = []
    for url in root.findall(xmls+'url'):
        # using root.findall() to avoid removal during traversal
        list.append(url.find(xmls+'loc').text)
    return list

def xml_alterar_data(file,url1,data):
    #Leitura do arquivo xml
    xmls = '{http://www.sitemaps.org/schemas/sitemap/0.9}'
    tree = ET.parse(file)
    root = tree.getroot()
    #Remover item do xml
    for url in root.findall(xmls+'url'):
        # using root.findall() to avoid removal during traversal
        if url1 == url.find(xmls+'loc').text:
            url.find(xmls+'lastmod').text = data
            # linha de comando abaixo retira os ns0 ("namespace criados pela tag xmls")
            ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9')
            tree.write(file)
            break

def hoje():
    from datetime import datetime
    data = datetime.now()
    dia=str(data.year)+'-'+str(data.month).zfill(2)+'-'+str(data.day).zfill(2)
    return dia