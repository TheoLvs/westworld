import random
import numpy as np


class DNA:
    def __init__(self,genes:list):
        self.genes = genes


    def get(self,name):
        return self[name].value

    def __getitem__(self,name):
        return [gene for gene in self.genes if gene.name == name][0]

    def __repr__(self):
        genes_str = ",".join([f"{gene.name}={gene.to_string()}" for gene in self.genes])
        return f"DNA({genes_str})"


    def sample(self):
        new_genes = []
        for gene in self.genes:
            new_genes.append(gene.sample())
        return DNA(new_genes)


    def mate(self,other,mutation_proba = 0):

        new_genes = []
        for i in range(len(self.genes)):
            gene = self.genes[i].mate(other.genes[i],mutation_proba)
            new_genes.append(gene)

        new_dna = DNA(new_genes)
        return new_dna




class Gene:
    def __init__(self,name,value = None,value_range = None,options = None,type="int"):
        
        self.name = name
        self.value = value
        self.value_range = value_range
        self.options = options
        self.type = type

            
        if value is None:
            self.value = self.sample().value
        
        # Assertions
        assert self.type in ["int","float",None]
        assert self.value_range is not None or self.options is not None
        if self.value_range is not None:
            assert self.value >= self.min_value and self.value <= self.max_value
            assert self.type is not None
        if self.options is not None:
            assert self.value in self.options

            
    @property
    def min_value(self):
        return self.value_range[0]
    
    @property
    def max_value(self):
        return self.value_range[1]


    def to_string(self):
        if self.options is not None:
            value_str = self.value
        else:
            value_str = f"{self.value:.3f}" 
        return value_str
        
    def __repr__(self):
        return f"Gene({self.name}={self.to_string()})"
    
    def sample(self):
        if self.options is not None:
            value = random.choice(self.options)
        elif self.type == "int":
            value = np.random.randint(self.min_value,self.max_value + 1)
        elif self.type == "float":
            min_value,max_value = self.value_range
            value = min_value + np.random.random() * (max_value - min_value)
            
        new_gene = Gene(name = self.name,value = value,value_range = self.value_range,options = self.options,type = self.type)
        return new_gene    
    
    def mate(self,other,mutation_proba=0):
        assert self.name == other.name
        assert self.value_range == other.value_range
        assert self.options == other.options
        
        if random.random() < mutation_proba:
            return self.sample()
        else:

            if self.options is not None:
                value = random.choice([self.value,other.value])
            elif self.type == "int":
                min_value,max_value = sorted([self.value,other.value])
                value = np.random.randint(min_value,max_value + 1)
            elif self.type == "float":
                min_value,max_value = sorted([self.value,other.value])
                value = min_value + np.random.random() * (max_value - min_value)
                
        new_gene = Gene(name = self.name,value = value,value_range = self.value_range,options = self.options,type = self.type)
        return new_gene
    
    
    def __add__(self,other):
        return self.mate(other)
