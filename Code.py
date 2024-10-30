import networkx as nx
import matplotlib.pyplot as plt

# Dictionary of R genes with corresponding Avr genes and chromosome numbers
rlm_gene_info = {
    "Rlm1": {"Avr_gene": "AvrLm1-L3", "Chromosome": "A07"},
    "Rlm2": {"Avr_gene": "AvrLm2", "Chromosome": "A10"},
    "Rlm3": {"Avr_gene": "AvrLm3", "Chromosome": "A07"},
    "Rlm4": {"Avr_gene": "AvrLm4-7", "Chromosome": "A07"},
    "Rlm5": {"Avr_gene": "AvrLm5-9", "Chromosome": "A10"},
    "Rlm6": {"Avr_gene": "AvrLm6", "Chromosome": "A07"},
    "Rlm7": {"Avr_gene": "AvrLm4-7", "Chromosome": "A07"},
    "Rlm8": {"Avr_gene": "AvrLm8", "Chromosome": "A?"},
    "Rlm9": {"Avr_gene": "AvrLm5-9", "Chromosome": "A07"},
    "Rlm10": {"Avr_gene": ["AvrLm10a", "AvrLm10b"], "Chromosome": "B04"},
    "Rlm11": {"Avr_gene": "AvrLm11", "Chromosome": "A?"},
    "Rlm12": {"Avr_gene": "Avr?", "Chromosome": "A01"},
    "Rlm13": {"Avr_gene": "AvrLm13?", "Chromosome": "C03"},
    "Rlm14": {"Avr_gene": "AvrLm14", "Chromosome": "?"},
    "RlmS": {"Avr_gene": "AvrLmS-Lep2", "Chromosome": "?"},
    "LepR1": {"Avr_gene": "AvrLepR1", "Chromosome": "A02"},
    "LepR2": {"Avr_gene": ["AvrLmS-Lep2", "AvrLep2"], "Chromosome": "A10"},
    "LepR3": {"Avr_gene": "AvrLm1-L3", "Chromosome": "A10"},
    "LepR4a": {"Avr_gene": "AvrLepR4", "Chromosome": "A09"},
    "LepR4b": {"Avr_gene": "AvrLepR4", "Chromosome": "A09"},
    "LMJR1": {"Avr_gene": "Avr?", "Chromosome": "B?"},
    "LMJR2": {"Avr_gene": "Avr?", "Chromosome": "B?"},
    "rjml2": {"Avr_gene": "Avr?", "Chromosome": "B?"}
}

# Function to retrieve Avr gene and chromosome based on input R gene
def get_avr_info(rlm_gene):
    info = rlm_gene_info.get(rlm_gene)
    if info:
        avr_gene = info['Avr_gene']
        avr_str = avr_gene if isinstance(avr_gene, str) else ', '.join(avr_gene)
        return f"{rlm_gene} interacts with {avr_str} on chromosome {info['Chromosome']}."
    else:
        return "R gene not found. Please check the gene name and try again."

# Function to visualize selected R-Avr gene interactions with left-right layout
def visualize_multiple_interactions(selected_genes):
    G = nx.DiGraph()  # Use directed graph to control layout

    # Add only the selected R-Avr gene interactions to the graph
    for rlm_gene in selected_genes:
        info = rlm_gene_info.get(rlm_gene)
        if info:
            avr_gene = info["Avr_gene"]
            if isinstance(avr_gene, list):
                for a_gene in avr_gene:
                    G.add_edge(rlm_gene, a_gene)
            else:
                G.add_edge(rlm_gene, avr_gene)

    # Position R genes on the left and Avr genes on the right
    pos = {}
    left_nodes = [gene for gene in selected_genes]
    right_nodes = set()

    for gene in selected_genes:
        if gene in rlm_gene_info:
            avr_gene = rlm_gene_info[gene]["Avr_gene"]
            if isinstance(avr_gene, list):
                right_nodes.update(avr_gene)
            else:
                right_nodes.add(avr_gene)

    pos.update((node, (0, i)) for i, node in enumerate(left_nodes))  # Left nodes
    pos.update((node, (1, i * 2)) for i, node in enumerate(right_nodes))  # Space out right nodes

    # Define a color map for R genes and Avr genes
    left_colors = plt.cm.tab20.colors  # Use a colormap for R genes
    right_colors = plt.cm.tab20.colors  # Use remaining colors for Avr genes

    # Ensure we have enough colors for right nodes
    if len(right_nodes) > len(right_colors):
        raise ValueError("Not enough colors available for Avr genes.")

    color_map = {}
    for i, gene in enumerate(left_nodes):
        color_map[gene] = left_colors[i % len(left_colors)]  # Cycle through colors for R genes
    for i, gene in enumerate(right_nodes):
        color_map[gene] = right_colors[i % len(right_colors)]  # Cycle through colors for Avr genes

    # Draw the graph with larger circles and specific colors
    plt.figure(figsize=(14, 10))
    node_colors = [color_map[node] for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_size=6000, node_color=node_colors,
            font_size=10, font_weight="bold", edge_color="black", arrows=True)
    plt.title("R-Avr Gene Interactions (Left-Right Layout)")
    plt.axis('off')  # Hide axes for clarity
    plt.show()

# Main program to get user input and visualize results
try:
    num_genes = int(input("How many R genes do you want to check? "))
except ValueError:
    print("Invalid input. Please enter a number.")
    exit()

selected_genes = []
for i in range(num_genes):
    while True:
        rlm_gene = input(f"Enter R gene name {i + 1}/{num_genes} (e.g., Rlm1): ")
        info = get_avr_info(rlm_gene)
        print(info)

        if "not found" not in info:  # Check if the gene was found
            selected_genes.append(rlm_gene)
            break  # Exit the loop if valid gene is entered

# Visualize all selected gene interactions in a single plot
visualize_multiple_interactions(selected_genes)


