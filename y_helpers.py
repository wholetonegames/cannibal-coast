MAX_STAGE_LOOP = 10
YELLOW = (1.0, 0.8, 0, 1)
GREEN = (0.1, 0.5, 0.2, 1)


def stringify_time_units(value):
    return str(value).zfill(2)


def pretty_print_time(seconds):
    secondsBase = int(seconds)
    hourFromSeconds = 60 * 60
    minuteFromSeconds = 60
    hours = secondsBase // hourFromSeconds
    minutes = (secondsBase % hourFromSeconds) // minuteFromSeconds
    seconds = secondsBase % minuteFromSeconds

    return "{} h {} m {}s".format(stringify_time_units(hours),
                                  stringify_time_units(minutes),
                                  stringify_time_units(seconds))
