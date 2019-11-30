import csv

def save_to_file(jobs):
    # open or create the result CSV file
    file = open("./../published/jobs.csv", mode="w", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(["title", "company", "location", "link"])

    for job in jobs:
        writer.writerow(list(job.values()))
    
    return
