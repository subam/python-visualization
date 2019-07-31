# 
# Copyright (C) University College London, 2007-2014, all rights reserved.
# 
# This file is part of FabSim and is CONFIDENTIAL. You may not work 
# with, install, use, duplicate, modify, redistribute or share this
# file, or any part thereof, other than as allowed by any agreement
# specifically made by you with University College London.
# 
# no batch system


cd /home/hamid/FabSim3/results/mali_localhost_16
echo Running...

if [ -z "/home/hamid/Downloads/Fabsim_template_cleanup/flee" ]
then
	echo "Please set $flee_location in your deploy/machines_user.yml file."
else
	export PYTHONPATH=/home/hamid/Downloads/Fabsim_template_cleanup/flee:$PYTHONPATH
fi

/usr/bin/env > env.log

python3 run.py input_csv source_data 300 simsetting.csv > out.csv
