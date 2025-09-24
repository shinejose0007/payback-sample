import os, json, math
from statistics import mean
PRED_LOG = os.environ.get('PRED_LOG', 'logs/predictions.jsonl')

def read_preds(path=PRED_LOG):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            out.append(json.loads(line))
    return out

def summary():
    preds = read_preds()
    if not preds:
        print('No predictions logged yet.')
        return
    values = [p['prediction'] for p in preds]
    m = mean(values)
    std = math.sqrt(sum((x-m)**2 for x in values)/len(values))
    print(f'Count: {len(values)}, Mean: {m:.4f}, Std: {std:.4f}')

if __name__ == '__main__':
    summary()
