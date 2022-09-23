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
    #Salvar alterações
    tree.write(file)


def sitemap_delete(file,url_delete):
    #Leitura do arquivo xml
    tree = ET.parse(file)
    root = tree.getroot()
    #Remover item do xml
    for url in root.findall('url'):
        # using root.findall() to avoid removal during traversal
        loc = url.find('loc').text    
        if loc == url_delete:
            root.remove(url)
    tree.write(file)

def merge_xml(file1, file2, output):
    #leitura dos arquivos a serem mesclados
    tree1 = ET.parse(file1)
    tree2 = ET.parse(file2)
    root1 = tree1.getroot()
    root2 = tree2.getroot()
    # mesclagem do file2 em file1
    root1.extend(root2)
    # salvando os arquivos mesclados
    tree1.write(output)
