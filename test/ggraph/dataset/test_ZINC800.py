from dig.ggraph.dataset import ZINC800
import shutil

def test_zinc800():
    root = './dataset/ZINC800'
    dataset = ZINC800(root)

    assert len(dataset) == 800
    assert dataset.num_features == 9
    assert dataset.__repr__() == 'zinc_800_jt(800)'
    
    assert len(dataset[0]) == 6
    assert dataset[0].x.size() == (38, 9)
    assert dataset[0].y.size() == (1,)
    assert dataset[0].adj.size() == (4, 38, 38)
    assert dataset[0].bfs_perm_origin.size() == (38,)
    assert dataset[0].num_atom.size() == (1,)

    shutil.rmtree(root)