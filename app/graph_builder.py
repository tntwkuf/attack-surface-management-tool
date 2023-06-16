from pyvis.network import Network
import networkx as nx
import os
from .check_ip_is_private import check_ip_is_public


# переопределение настроек визуализации графа - физика, размер шрифтов и т.ж.
def get_graph_options():
    options = {
        "nodes": {
            "font": {
                "size": 50
            }
        },
        "physics": {
            "barnesHut": {
                "gravitationalConstant": -50000,
                "centralGravity": 0.5,
                "springLength": 100,
                "springConstant": 0.005,
                "avoidOverlap": 1
            },
            "minVelocity": 0.75
        },
        "interaction": {
            "navigationButtons": True,
            "selectConnectedEdges": True,
            "hoverConnectedEdges": True

        },
        "edges": {
            "selectionWidth": 7
        }
    }
    return options


# отвязывает проверку библиотек через Интернет, указывает локальные пути к библиотекам
def modify_graph(file):
    path = '../static/lib'
    oldFile = file + "~"
    os.rename(file, oldFile)
    text = ''
    with open(oldFile, 'r') as source:
        for row in source.readlines():
            if 'utils.js' in row:
                text += f'            <script type="text/javascript" src="{path}/bindings/utils.js" ></script>\n'
            elif 'vis-network.min.css' in row:
                text += f'            <link rel="stylesheet" href="{path}/vis-9.1.2/vis-network.min.css" type="text/css" />\n'
            elif 'vis-network.min.js' in row:
                text += f'            <script type="text/javascript" src="{path}/vis-9.1.2/vis-network.min.js" ></script>\n'
            elif 'tom-select.css' in row:
                text += f'                <link href="{path}/tom-select/tom-select.css" rel="stylesheet">\n'
            elif 'tom-select.complete.min.js' in row:
                text += f'                <script src="{path}/tom-select/tom-select.complete.min.js"></script>\n'
            elif 'bootstrap.min.css' in row:
                text += f'		rel="stylesheet" href="{path}/bootstrap/bootstrap.min.css" type="text/css"\n'
            elif 'bootstrap.bundle.min.js' in row:
                text += f'        type="text/javascript" src="{path}/bootstrap/bootstrap.bundle.min.js"\n'
            elif 'rel=' in row or 'integrity' in row or 'crossorigin' in row or '</script>-->' in row:
                continue
            else:
                text += row
    with open(file, 'w') as dest:
        dest.write(text)
    os.remove(oldFile)


# строит граф доменов /поддоменов
def base_graph(total, domains):
    try:
        G = nx.MultiGraph()
        # формирует группы из доменов второго уровня, каждая группа это один домен и его поддомены
        groups = {x.name: y for y, x in enumerate(domains, 1)}
        for group in groups.keys():
            G.add_node(group)
        # проходит по всем найденным поддоменам
        for row in total:
            record = row.object
            domain = row.parent.name
            ip = row.ip
            ports = row.open_ports
            banner = row.banner
            # добавляет вершину на граф
            G.add_node(record, size=75 if record in groups.keys() else 25,
                       title=f'IP: {ip}\nPorts: {ports}\nBanner: {banner}', group=groups[domain])
        # проходит по всем группам
        for group_id in groups.values():
            # проходит по всем вершинам в группе
            group = [x for x, y in G.nodes(data=True) if y.get('group') == group_id]
            for node in group:
                parent = None
                # выстраивает связь между доменами разных уровней (второго и третьего, третьего и четвертого и т.д.)
                for _ in group:
                    if ('.' + _) in node and _ != node:
                        parent = _
                if parent:
                    G.add_edge(node, parent)
        # создает экзампляр графа
        nt = Network(neighborhood_highlight=True, height="1100px", width="100%", bgcolor="#222222", font_color="white",
                     select_menu=True,
                     cdn_resources='local')
        # метод симуляции физики barnes_hut
        nt.barnes_hut()
        # перенос графа из networkx в pyvis
        nt.from_nx(G)
        # переопределение настроек графа
        nt.options = get_graph_options()
        # сохранение графа
        nt.save_graph('app/templates/base_graph.html')
        # отвязка от проверки через Интернет
        modify_graph('app/templates/base_graph.html')
        return False
    except Exception as e:
        return e


# строит граф связей - по какому запросу и каким модулем был найден тот или иной объект
def relations_graph(rels, keywords):
    try:
        G = nx.MultiGraph()
        # сначала представляет ключевые слова в виде вершин с размером 75 и включает их в первую группу
        keywords = [i.keyword for i in keywords]
        for i in keywords:
            G.add_node(i, size=75, group=1)
        # далее проходит по всем связям, добавляет вершины и создает связи
        ### мега костыль чтобы исключить IP адреса из BGP, которые замусорят граф
        for row in [i for i in rels if not check_ip_is_public(i.object)]:
            record = row.object
            key = row.query
            module = row.module.name
            G.add_node(record, size=25, group=2)
            # если такой вершины еще нет, создает ее
            try:
                G[key]
            except:
                G.add_node(key, size=25, group=2)
            # проверка, чтобы не создавалась петля в вершине
            if record != key:
                # проверка, есть ли такое ребро
                current_edge = [e for e in G.edges(record, data=True) if e[1] == key]
                # если есть, добавляет модуль и увеличивает вес ребра
                if current_edge:
                    e = current_edge[0][2]
                    e.update({'title': e.get('title') + ', ' + module, 'value': e.get('value') + 0.5})
                # если нет, создает ребро с модулем и весом 1
                else:
                    G.add_edge(record, key, title=module, value=1, color='green' if key in keywords else None)
        # создает экзампляр графа
        nt = Network(neighborhood_highlight=True, height="1100px", width="100%", bgcolor="#222222", font_color="white",
                     select_menu=True, cdn_resources='local', directed=True)
        # метод симуляции физики barnes_hut
        nt.barnes_hut()
        # перенос графа из networkx в pyvis
        nt.from_nx(G)
        # переопределение настроек графа
        nt.options = get_graph_options()
        # сохранение графа
        nt.save_graph('app/templates/relations_graph.html')
        # отвязка от проверки через Интернет
        modify_graph('app/templates/relations_graph.html')
        return False
    except Exception as e:
        return e
