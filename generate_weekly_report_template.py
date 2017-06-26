import csv
from datetime import date
from datetime import datetime
from datetime import timedelta

TEMPLATE_DIR = 'templates'
OUTPUT_DIR = '/Users/tyson/git/leehosung.github.io/_drafts'
HEALTH_SOURCE_FILE = '/Users/tyson/Downloads/Health Data.csv'
START_DATE = date(2017, 6, 21)
WATER_GOAL = 2
STEPS_GOAL = 10000
CALORIES_GOAL = 1200

today = date.today() - timedelta(1)
this_week_sunday = today + timedelta((6 - today.weekday()) % 7)
this_week_sunday = this_week_sunday
this_week_monday = this_week_sunday + timedelta(-6)
next_week_monday = this_week_sunday + timedelta(1)
next_week_sunday = this_week_sunday + timedelta(7)

def get_health_data():
    with open(HEALTH_SOURCE_FILE) as csvfile:
        datareader = csv.DictReader(csvfile)
        return filter(lambda x:
                      datetime.strptime(x['Start'], '%d-%b-%Y %H:%M').date() >= this_week_monday and
                      datetime.strptime(x['Start'], '%d-%b-%Y %H:%M').date() >= START_DATE and
                      datetime.strptime(x['Finish'], '%d-%b-%Y %H:%M').date() < next_week_monday,
                      datareader)

def get_health_stat():
    data = get_health_data()
    water_success_days = 0
    total_water = 0
    step_success_days = 0
    total_steps = 0
    calory_success_days = 0
    total_calories = 0

    count = 0
    for row in data:
        water = float(row['Dietary Water (L)'])
        if water >= WATER_GOAL:
            water_success_days += 1
        total_water += water

        steps = float(row['Steps (count)'])
        if steps >= STEPS_GOAL:
            step_success_days += 1
        total_steps += steps

        # calory -> killo calory
        calory = float(row['Dietary Calories (cal)']) / 1000
        if calory <= CALORIES_GOAL:
            calory_success_days += 1
        total_calories += calory
        count += 1

    return dict(
        average_water="%.2f" % (total_water/count),
        water_success_days=water_success_days,
        average_steps=int(total_steps/count),
        step_success_days=step_success_days,
        average_calories=int(total_calories/count),
        calory_success_days=calory_success_days,
        count=count
    )

def get_report_from_template():
    contents = file('{}/{}'.format(TEMPLATE_DIR, 'weekly.md')).read()
    values = dict(
        this_week_year=this_week_monday.year,
        this_week_number=this_week_monday.strftime('%W'),
        this_week_monday=this_week_monday,
        this_week_sunday=this_week_sunday,
        next_week_year=next_week_monday.year,
        next_week_number=next_week_monday.strftime('%W'),
        next_week_monday=next_week_monday,
        next_week_sunday=next_week_sunday,
    )
    values.update(get_health_stat())
    return contents.format(**values)

file_name = this_week_sunday.strftime('%Y-%m-%d-%Y-W%W.md')
file_path = '{}/{}'.format(OUTPUT_DIR, file_name)
weekly_report = get_report_from_template()
open(file_path, 'w').write(weekly_report)
