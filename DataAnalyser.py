def analyse(sstubs):
    sstubs = clean_data(sstubs)
    average = average_overall_time(sstubs)
    build_averages = average_build_time(sstubs)
    output_data(average, build_averages)


def clean_data(sstubs):
    length = len(sstubs)
    new_sstubs = []
    counter = 0
    for sstub in sstubs:
        if sstub.bug_sha is None or sstub.bug_time is None or sstub.fix_time is None:
            counter += 1
            continue
        new_sstubs.append(sstub)
    print("{}/{} SStuBs removed       ".format(counter, length))
    print("Analysing {} SStuBs".format(len(new_sstubs)))
    return new_sstubs


def average_overall_time(sstubs):
    total = 0
    for sstub in sstubs:
        total += sstub.time_difference.total_seconds()

    return total / len(sstubs)


def average_build_time(sstubs):
    project_times = load_times(sstubs)

    for sstub in sstubs:
        for name in project_times.keys():
            if sstub.project_name == name:
                project_times[name] += sstub.time_difference.total_seconds()
                break
    return project_times


def load_times(sstubs):
    project_names_set = set()
    for sstub in sstubs:
        project_names_set.add(sstub.project_name)

    project_names_dict = {}
    for name in project_names_set:
        project_names_dict[name] = 0

    return project_names_dict


def output_data(average, build_averages):
    minutes = average / 60
    hours = minutes / 60
    days = hours / 24
    print("Overall Average Days: {}".format(days))
    print("")
    #for key, value in build_averages.items():
    #    build_avg =
    #    print("{} Average Time: {}".format(key, value))




# Get average time overall
# Get average time for each build system
# Get build system count