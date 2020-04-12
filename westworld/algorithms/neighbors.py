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


    def find(self,obj,search_range = None):

        # TODO 
        # Will not work with double colliders
        # Can be made using colliders in PyGame ?

        # Safety check
        assert hasattr(self,"tree")
        obj_data = self.data.loc[obj.id]

        # Get position from dataset
        pos = obj_data["pos"]

        # Get vision_range if not given
        if search_range is None:
            try:
                search_range = obj_data["vision_range"]
            except:
                raise Exception(f"Object '{obj.id}' has no data attribute 'vision_range'")

        # Find neighbors in range
        # We remove the first one which is the identity object
        neighbors = self.tree.query_ball_point(pos,search_range)[1:]
        
        # Return filtered data
        neighbors = self.data.iloc[neighbors]
        return neighbors