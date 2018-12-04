import re
import aoc
import pendulum
from collections import defaultdict, Counter


@aoc.test({
'''[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up''': 240
})
def part_1(data: aoc.Data):
    guard_ids = {int(x) for x in re.findall(r'#(\d+)', data)}
    slept = Counter()
    minutes = {guard: Counter() for guard in guard_ids}
    for line in sorted(data.splitlines()):
        if 'begins shift' in line:
            ts, guard = re.search(r'\[(.*)\].*?(\d+)', line).groups()
            ts = pendulum.parse(ts)
            guard = int(guard)
        if 'falls asleep' in line:
            ts = pendulum.parse(re.search(r'\[(.*)\]', line).group(1))
        if 'wakes up' in line:
            wake_ts = pendulum.parse(re.search(r'\[(.*)\]', line).group(1))
            slept[guard] += (wake_ts - ts).total_minutes()
            for t in (wake_ts - ts).range('minutes'):
                if t == wake_ts:
                    continue
                minutes[guard][t.minute] += 1

    guard = slept.most_common()[0][0]
    minute = minutes[guard].most_common()[0][0]
    return guard * minute
