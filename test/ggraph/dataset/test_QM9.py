from dig.ggraph.dataset import QM9
import shutil

def test_qm9():
    root = './dataset/QM9'
    dataset = QM9(root, prop_name='penalized_logp')

    assert len(dataset) == 133885
    assert dataset.num_features == 4
    assert dataset.__repr__() == 'qm9_property(133885)'

    assert len(dataset[0]) == 6
    assert dataset[0].x.size() == (9, 4)
    assert dataset[0].y.size() == (1,)
    assert dataset[0].adj.size() == (4, 9, 9)
    assert dataset[0].bfs_perm_origin.size() == (9,)
    assert dataset[0].num_atom.size() == (1,)

    shutil.rmtree(root)
