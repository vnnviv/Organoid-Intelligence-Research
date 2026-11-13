# PubMed string test (2026-11-12)

Recall is measured on the 19 known Includes that PubMed indexes. Rev C's extra terms were chosen after seeing which known papers S1 missed, so its 19/19 is optimistic; check it on new Includes found during screening.

| String | Records | Known Includes found | Missed PMIDs |
|---|---|---|---|
| S1 as planned | 1723 | 17/19 | 37307467, 40819006 |
| Rev A: OI terms OR (neural AND interface AND claim) | 501 | 16/19 | 32327697, 40819006, 42780126 |
| Rev B: OI terms OR (neural AND claim) | 2747 | 19/19 | - |
| Rev C: OI OR (N AND I AND C) OR (N AND strong claim) | 1246 | 19/19 | - |
| Rev D: as C, interface includes stimulat* | 1367 | 19/19 | - |

## Full strings

### S1 as planned

```
("organoid intelligence"[tiab] OR "synthetic biological intelligence"[tiab] OR wetware[tiab] OR biocomput*[tiab] OR ((organoid*[tiab] OR "neural culture*"[tiab] OR "neuronal culture*"[tiab] OR "cortical culture*"[tiab] OR "biological neural network*"[tiab] OR "multielectrode array*"[tiab] OR "microelectrode array*"[tiab]) AND ("reservoir comput*"[tiab] OR "reinforcement learning"[tiab] OR "closed-loop"[tiab] OR "goal-directed"[tiab] OR "sample efficien*"[tiab] OR "energy efficien*"[tiab] OR "machine learning"[tiab] OR classif*[tiab] OR "information processing"[tiab]))) AND 2020/01/01:3000/12/31[dp]
```

### Rev A: OI terms OR (neural AND interface AND claim)

```
(("organoid intelligence"[tiab] OR "synthetic biological intelligence"[tiab] OR wetware[tiab] OR "biological computing"[tiab] OR "biocomputer*"[tiab]) OR (("brain organoid*"[tiab] OR "cerebral organoid*"[tiab] OR "cortical organoid*"[tiab] OR "neural organoid*"[tiab] OR "forebrain organoid*"[tiab] OR assembloid*[tiab] OR "neural culture*"[tiab] OR "neuronal culture*"[tiab] OR "cortical culture*"[tiab] OR "cultured neuron*"[tiab] OR "cultured cortical"[tiab] OR "neuronal network*"[tiab] OR "biological neural network*"[tiab] OR "biological neuronal network*"[tiab] OR "in vitro neur*"[tiab] OR "dissociated"[tiab]) AND ("multielectrode*"[tiab] OR "multi-electrode*"[tiab] OR "microelectrode*"[tiab] OR MEA[tiab] OR MEAs[tiab] OR electrophysiolog*[tiab] OR "electrical stimulation"[tiab] OR optogenet*[tiab] OR "calcium imaging"[tiab]) AND ("reservoir comput*"[tiab] OR "reinforcement learning"[tiab] OR "closed-loop"[tiab] OR "closed loop"[tiab] OR "goal-directed"[tiab] OR "sample efficien*"[tiab] OR "energy efficien*"[tiab] OR "machine learning"[tiab] OR "information processing"[tiab] OR comput*[tiab] OR learning[tiab] OR memory[tiab] OR classif*[tiab] OR "pattern recognition"[tiab] OR "logic gate*"[tiab] OR boolean[tiab] OR "artificial intelligence"[tiab]))) AND 2020/01/01:3000/12/31[dp]
```

### Rev B: OI terms OR (neural AND claim)

```
(("organoid intelligence"[tiab] OR "synthetic biological intelligence"[tiab] OR wetware[tiab] OR "biological computing"[tiab] OR "biocomputer*"[tiab]) OR (("brain organoid*"[tiab] OR "cerebral organoid*"[tiab] OR "cortical organoid*"[tiab] OR "neural organoid*"[tiab] OR "forebrain organoid*"[tiab] OR assembloid*[tiab] OR "neural culture*"[tiab] OR "neuronal culture*"[tiab] OR "cortical culture*"[tiab] OR "cultured neuron*"[tiab] OR "cultured cortical"[tiab] OR "neuronal network*"[tiab] OR "biological neural network*"[tiab] OR "biological neuronal network*"[tiab] OR "in vitro neur*"[tiab] OR "dissociated"[tiab]) AND ("reservoir comput*"[tiab] OR "reinforcement learning"[tiab] OR "closed-loop"[tiab] OR "closed loop"[tiab] OR "goal-directed"[tiab] OR "sample efficien*"[tiab] OR "energy efficien*"[tiab] OR "machine learning"[tiab] OR "information processing"[tiab] OR comput*[tiab] OR learning[tiab] OR memory[tiab] OR classif*[tiab] OR "pattern recognition"[tiab] OR "logic gate*"[tiab] OR boolean[tiab] OR "artificial intelligence"[tiab]))) AND 2020/01/01:3000/12/31[dp]
```

### Rev C: OI OR (N AND I AND C) OR (N AND strong claim)

```
(("organoid intelligence"[tiab] OR "synthetic biological intelligence"[tiab] OR wetware[tiab] OR "biological computing"[tiab] OR "biocomputer*"[tiab]) OR (("brain organoid*"[tiab] OR "cerebral organoid*"[tiab] OR "cortical organoid*"[tiab] OR "neural organoid*"[tiab] OR "forebrain organoid*"[tiab] OR assembloid*[tiab] OR "neural culture*"[tiab] OR "neuronal culture*"[tiab] OR "cortical culture*"[tiab] OR "cultured neuron*"[tiab] OR "cultured cortical"[tiab] OR "neuronal network*"[tiab] OR "biological neural network*"[tiab] OR "biological neuronal network*"[tiab] OR "in vitro neur*"[tiab] OR "dissociated"[tiab]) AND ("multielectrode*"[tiab] OR "multi-electrode*"[tiab] OR "microelectrode*"[tiab] OR MEA[tiab] OR MEAs[tiab] OR electrophysiolog*[tiab] OR "electrical stimulation"[tiab] OR optogenet*[tiab] OR "calcium imaging"[tiab]) AND ("reservoir comput*"[tiab] OR "reinforcement learning"[tiab] OR "closed-loop"[tiab] OR "closed loop"[tiab] OR "goal-directed"[tiab] OR "sample efficien*"[tiab] OR "energy efficien*"[tiab] OR "machine learning"[tiab] OR "information processing"[tiab] OR comput*[tiab] OR learning[tiab] OR memory[tiab] OR classif*[tiab] OR "pattern recognition"[tiab] OR "logic gate*"[tiab] OR boolean[tiab] OR "artificial intelligence"[tiab])) OR (("brain organoid*"[tiab] OR "cerebral organoid*"[tiab] OR "cortical organoid*"[tiab] OR "neural organoid*"[tiab] OR "forebrain organoid*"[tiab] OR assembloid*[tiab] OR "neural culture*"[tiab] OR "neuronal culture*"[tiab] OR "cortical culture*"[tiab] OR "cultured neuron*"[tiab] OR "cultured cortical"[tiab] OR "neuronal network*"[tiab] OR "biological neural network*"[tiab] OR "biological neuronal network*"[tiab] OR "in vitro neur*"[tiab] OR "dissociated"[tiab]) AND ("reservoir comput*"[tiab] OR "reinforcement learning"[tiab] OR "closed-loop"[tiab] OR "closed loop"[tiab] OR "machine learning"[tiab] OR "artificial intelligence"[tiab] OR "learning algorithm*"[tiab] OR "sample efficien*"[tiab] OR "energy efficien*"[tiab] OR "decision-making"[tiab] OR "learning and memory"[tiab]))) AND 2020/01/01:3000/12/31[dp]
```

### Rev D: as C, interface includes stimulat*

```
(("organoid intelligence"[tiab] OR "synthetic biological intelligence"[tiab] OR wetware[tiab] OR "biological computing"[tiab] OR "biocomputer*"[tiab]) OR (("brain organoid*"[tiab] OR "cerebral organoid*"[tiab] OR "cortical organoid*"[tiab] OR "neural organoid*"[tiab] OR "forebrain organoid*"[tiab] OR assembloid*[tiab] OR "neural culture*"[tiab] OR "neuronal culture*"[tiab] OR "cortical culture*"[tiab] OR "cultured neuron*"[tiab] OR "cultured cortical"[tiab] OR "neuronal network*"[tiab] OR "biological neural network*"[tiab] OR "biological neuronal network*"[tiab] OR "in vitro neur*"[tiab] OR "dissociated"[tiab]) AND ("multielectrode*"[tiab] OR "multi-electrode*"[tiab] OR "microelectrode*"[tiab] OR MEA[tiab] OR MEAs[tiab] OR electrophysiolog*[tiab] OR "electrical stimulation"[tiab] OR optogenet*[tiab] OR "calcium imaging"[tiab] OR stimulat*[tiab]) AND ("reservoir comput*"[tiab] OR "reinforcement learning"[tiab] OR "closed-loop"[tiab] OR "closed loop"[tiab] OR "goal-directed"[tiab] OR "sample efficien*"[tiab] OR "energy efficien*"[tiab] OR "machine learning"[tiab] OR "information processing"[tiab] OR comput*[tiab] OR learning[tiab] OR memory[tiab] OR classif*[tiab] OR "pattern recognition"[tiab] OR "logic gate*"[tiab] OR boolean[tiab] OR "artificial intelligence"[tiab])) OR (("brain organoid*"[tiab] OR "cerebral organoid*"[tiab] OR "cortical organoid*"[tiab] OR "neural organoid*"[tiab] OR "forebrain organoid*"[tiab] OR assembloid*[tiab] OR "neural culture*"[tiab] OR "neuronal culture*"[tiab] OR "cortical culture*"[tiab] OR "cultured neuron*"[tiab] OR "cultured cortical"[tiab] OR "neuronal network*"[tiab] OR "biological neural network*"[tiab] OR "biological neuronal network*"[tiab] OR "in vitro neur*"[tiab] OR "dissociated"[tiab]) AND ("reservoir comput*"[tiab] OR "reinforcement learning"[tiab] OR "closed-loop"[tiab] OR "closed loop"[tiab] OR "machine learning"[tiab] OR "artificial intelligence"[tiab] OR "learning algorithm*"[tiab] OR "sample efficien*"[tiab] OR "energy efficien*"[tiab] OR "decision-making"[tiab] OR "learning and memory"[tiab]))) AND 2020/01/01:3000/12/31[dp]
```

