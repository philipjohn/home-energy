#!/usr/bin/env bash

python3 /Users/philipjohn/projects/fun/home-energy/fox/index.py device_history_query >> /Users/philipjohn/projects/fun/home-energy/cron.log
python3 /Users/philipjohn/projects/fun/home-energy/fox/index.py device_report_query >> /Users/philipjohn/projects/fun/home-energy/cron.log
python3 /Users/philipjohn/projects/fun/home-energy/fox/index.py device_generation >> /Users/philipjohn/projects/fun/home-energy/cron.log
python3 /Users/philipjohn/projects/fun/home-energy/myenergi/index.py >> /Users/philipjohn/projects/fun/home-energy/cron.log
