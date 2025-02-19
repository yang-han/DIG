import json
from dig.ggraph.method import GraphDF
from dig.ggraph.evaluation import Cons_Optim_Evaluator
from dig.ggraph.dataset import ZINC800
from torch_geometric.data import DenseDataLoader

from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--data', type=str, default='graphaf', choices=['graphaf', 'jt'], help='dataset name')
parser.add_argument('--model_path', type=str, default='./saved_ckpts/cons_optim/cons_optim_graphaf.pth', help='The path to the saved model file')
parser.add_argument('--train', action='store_true', default=False, help='specify it to be true if you are running training')

args = parser.parse_args()

if args.data == 'graphaf':
    with open('config/cons_optim_graphaf_config_dict.json') as f:
        conf = json.load(f)
    dataset = ZINC800(method='graphaf', conf_dict=conf['data'], one_shot=False, use_aug=False)
elif args.data == 'jt':
    with open('config/cons_optim_jt_config_dict.json') as f:
        conf = json.load(f)
    dataset = ZINC800(method='jt', conf_dict=conf['data'], one_shot=False, use_aug=False)
else:
    print('Only graphaf and jt datasets are supported!')
    exit()

runner = GraphDF()

if args.train:
    loader = DenseDataLoader(dataset, batch_size=conf['batch_size'], shuffle=True)
    runner.train_cons_optim(loader, conf['lr'], conf['weight_decay'], conf['max_iters'], conf['warm_up'], conf['model'], conf['pretrain_model'], conf['save_interval'], conf['save_dir'])
else:
    mols_0, mols_2, mols_4, mols_6 = runner.run_cons_optim(dataset, conf['model'], args.model_path, conf['repeat_time'], conf['min_optim_time'], conf['num_max_node'], conf['temperature'], conf['atom_list'])
    smiles = [data.smile for data in dataset]
    evaluator = Cons_Optim_Evaluator()
    input_dict = {'mols_0': mols_0, 'mols_2': mols_2, 'mols_4': mols_4, 'mols_6': mols_6, 'inp_smiles':smiles}

    print('Evaluating...')
    results = evaluator.eval(input_dict)