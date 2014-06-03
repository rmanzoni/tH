#!/bin/bash

ProductionTasks.py -w '*.root' -c -N 5 -q 1nd -t EMuTau_Yuta_Nov24 --batch_user htautau_group --output_wildcard '*.root' --cfg skim_emu_cfg.py `cat samples_skim.txt`
