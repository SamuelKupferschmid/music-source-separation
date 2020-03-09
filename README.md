## Active Learning
Dataset: data/multitracks_al.txt
Classes: vocal (0), instrument (1), other (2)

used proportional class weights for training. This explains the low train accuracy.

| Iteration | labeled Tracks  | Samples (train/val) | epochs | accuracy (train/val) | binary accuracy (train/val) |
| --------: | --------------: | ------------------: | -----: | -------------------: | --------------------------: |
|   1       | 145/7693 (1.9%) |   6292 / 200        | 8      |   0.53 / 0.72        | 0.68 / 0.67                 |