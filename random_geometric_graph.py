import networkx as nx
import matplotlib.pyplot as plt


plt.close('all')

n = 20
G = nx.random_geometric_graph(200,0.125)
pos=nx.get_node_attributes(G,'pos')
# G = nx.star_graph(n)
# pos = nx.spring_layout(G)
edge_colors = range(n)
nx.draw_networkx_edges(G,pos,alpha=0.8, edge_color=edge_colors, width=5, edge_cmap=plt.cm.BuPu)
nx.draw_networkx_nodes(G,pos,node_size=100)

# nx.draw(G,pos,node_color='#A0CBE2',edge_color=colors,width=4,edge_cmap=plt.cm.Blues,with_labels=False)
# plt.savefig("edge_colormap.png") # save as png
plt.show() # display

#%%

G=nx.random_geometric_graph(200,0.1)
# position is stored as node attribute data for random_geometric_graph
# pos=nx.get_node_attributes(G,'pos')
pos = nx.spring_layout(G)
# find node near center (0.5,0.5)
dmin=1
ncenter=0
for n in pos:
    x,y=pos[n]
    d=(x-0.5)**2+(y-0.5)**2
    if d<dmin:
        ncenter=n
        dmin=d

# color by path length from node near center
p=nx.single_source_shortest_path_length(G,ncenter)

node_colours = list(p.values())

# plt.figure(figsize=(8,8))
nx.draw_networkx_edges(G,pos,nodelist=[ncenter],alpha=0.5, edge_color='Purple', width=5)
nx.draw_networkx_nodes(G,pos,nodelist=p.keys(), node_size=100, node_color=list(p.values()), cmap=plt.cm.Blues)

plt.xlim(-0.05,1.05)
plt.ylim(-0.05,1.05)
plt.axis('off')
plt.savefig('random_geometric_graph.pdf')
plt.show()
