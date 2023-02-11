import glob
import os
import numpy as np
import pandas as pd
import snap
import argparse

class GraphGenerator:
    def __init__(self,
                 uid,
                 embeddings,
                 data_title,
                 k=5):

        self.data_title = data_title
        self.uid = uid
        self.embeddings = embeddings
        self.path = f'./static/result/{data_title}_{self.uid}'
        self.k = k
        
        self.data = None
        self.graph = None
        self.graph_list = []
        self.dist_matrix = None

    def load_files(self):
        path = self.path + '/*.csv'
        self.csv_files = glob.glob(path)

    def generate_distance_matrix(self): 
        """
        generate distance matrix
        """
        M = self.data.shape[0]
        self.dist_matrix = np.zeros((M,M))
        self.dist_matrix = np.sum(np.square(self.data), axis=1) + (np.sum(np.square(self.data), axis=1)).reshape(-1,1) - 2*np.matmul(self.data, self.data.T)

    def kNN(self): 
        """
        make graph with k neighbors per each point
        """
        self.graph = snap.TUNGraph.New()
        for i in range(self.dist_matrix.shape[0]):
            self.graph.AddNode(i)
        idx = 0
        for row in self.dist_matrix:
            nearest_neighbor = row.argsort()
            for i in range(1, self.k+1):
                self.graph.AddEdge(int(idx), int(nearest_neighbor[i]))
            idx += 1
        
        self.graph_list.append(self.graph)
        

    # def save_graph(self):
    #     """
    #     save graph file using snap lib
    #     """
    #     save_path = self.current_file[:-4]

    #     FOut = snap.TFOut(f'{save_path}_k_{self.k}.graph')
    #     self.graph.Save(FOut)
    #     FOut.Flush()

    def run(self):
        """
        make distant matrix -> clustering -> save graph
        """
        #self.load_files()
        # for csv_file in tqdm(self.csv_files):
        #     self.current_file = csv_file
        #     data = pd.read_csv(self.current_file)
                        
        #     if 'class' in data.columns:
        #         data = data.drop('class', axis=1)

        #     data = data.to_numpy()
        #     self.data = data[:, 1:]
        #     print(self.data)
        #     self.distant_matrix()
        #     self.kNN()
        #     self.save_graph()
        for e in self.embeddings:
            data = e["embedding"]

            if "class" in data.columns:
                data = data.drop('class', axis=1)
            self.data = data.to_numpy()
            self.generate_distance_matrix()
            self.kNN()
            #self.save_graph()
        
        return self.graph_list
        

def argparsing():
    parser = argparse.ArgumentParser(description="Make kNN Graph from MDP data")
    parser.add_argument('--data', '-d', help="MDP data for making graph")
    parser.add_argument('--clustering', '-c', help="clustering method")
    parser.add_argument('--neighbors', '-k', type = int, action = 'store', default = 5, help="Number of neighbor for graph")
    parser.add_argument('--perplexity', '-P', type = int, action = 'store', default = -1, help="Perplexity")
    parser.add_argument('--max_iter', '-I', type = int, action = 'store', default = -1, help="Iteration")
    parser.add_argument('--learning_rate', '-L', type = int, action = 'store', default = -1, help="Learning Rate ('0' for auto)")

    args = parser.parse_args()
    return args

def main():
    args = argparsing()
    print("Data: "+args.data, "\nNeighbors: "+ str(args.neighbors))

    gmaker = GraphGenerator(args.data, perplexity=args.perplexity, iteration=args.max_iter, learning_rate=args.learning_rate , k = args.neighbors)
    gmaker.run()

if __name__== "__main__":
    main()
