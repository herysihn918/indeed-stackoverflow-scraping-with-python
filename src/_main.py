from indeed import get_jobs as get_indeed_jobs
from stackoverflow import get_jobs as get_stackoverflow_jobs
from save_to_csv import save_to_file

jobs = []

indeed_jobs = get_indeed_jobs()
stackoverflow_jobs = get_stackoverflow_jobs()

# combine two websites' jobs into one list
jobs = indeed_jobs + stackoverflow_jobs

# save jobs as a CSV file
save_to_file(jobs)


