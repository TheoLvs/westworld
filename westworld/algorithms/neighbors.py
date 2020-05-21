import pandas as pd
from scipy.spatial.kdtree import KDTree

class NeighborsFinder:
    def __init__(self,data):
        """Find neigbors
        
        Args:
            data (pd.DataFrame or dict): data with at columns id,pos,and eventually range
        """
        if data is not None:

            self.data = data

            # Safety checks
            assert isinstance(data,pd.DataFrame)
            assert "pos" in data.columns


            # Initialize KDTree finder from scipy
            self.tree = KDTree(self.data["pos"].tolist())


    def find_in_range(self,obj,search_range):

        # TODO 
        # Will not work with double colliders
        # Can be made using colliders in PyGame ?

        # Safety check
        assert hasattr(self,"tree")

        # Get position from dataset
        pos = obj.pos

        # Find neighbors in range
        # We remove the first one which is the identity object
        idx = self.tree.query_ball_point(pos,search_range)
        
        # Return filtered data
        ids = self.data.iloc[idx].index.tolist()
        assert obj.id not in ids
        return ids


    def find_closest(self,obj,k = 1):

        # Safety check
        assert hasattr(self,"tree")

        # Get object position from which we want to find neighbors
        pos = obj.pos

        # Get position from dataset
        distances,idx = self.tree.query(pos,k = k)

        if k == 1:
            distances = [distances]
            idx = [idx]

        # Get ids from dataset
        # Safe check object is not in neighbors, which would mean above we remove another overlapping objects with [1:]
        ids = self.data.iloc[idx].index.tolist()
        assert obj.id not in ids
        return distances,ids
