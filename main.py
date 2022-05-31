# Required imports

import pandas as pd
import os
import datetime

sfx_dfs = list()
rot_loc_dfs = list()

for filename in os.listdir("./data/rotation-location"):
    rot_loc_dfs.append(
        pd.read_csv(f"./data/rotation-location/{filename}")
    )


# SFX df:
# sound_name;sound_type;sound_pos;start_time;end_time;look_start;look_end;look_range

def get_next_sound_data(remaining_lines):
    while remaining_lines and not remaining_lines[0].startswith("[SOUND_START];"):
        remaining_lines.pop(0)

    data = [remaining_lines.pop(0)]

    while remaining_lines and not remaining_lines[0].startswith("[SOUND_STOP];"):
        l = remaining_lines.pop(0)
        if l and not l.startswith("[SOUND_START]"):
            data.append(l)

    if remaining_lines:
        data.append(remaining_lines.pop(0))
    else:
        # Last entry of file does not have STOP timing information, construct it ourselves

        information_parts = data[0].split(';')
        information_parts[0] = "[SOUND_STOP]"

        # Set time to last watch time, this is allowed since application stops logging when last coin is collected
        last_entry_time = data[-1].split(';')[0]
        information_parts[1] = last_entry_time

        data.append(';'.join(information_parts))

    return data


for filename in os.listdir("./data/sfx-info"):
    df_entries = list()
    with open(f"./data/sfx-info/{filename}") as f:
        # Skip first two lines
        lines = f.readlines()[2:]

        # Remove empty lines
        lines = [l for l in lines if l.strip()]
        # lines = list(dict.fromkeys(lines))

        while lines:
            sound_data = get_next_sound_data(lines)
            sound_data = list(dict.fromkeys(sound_data))    # Remove duplicate time entries

            _, start_time, sname, stype, spos = sound_data[0].split(';')
            _, end_time, _, _, _ = sound_data[-1].split(';')

            data_points = sound_data[1:-1]

            sound_info = [sname, stype, spos, start_time, end_time]

            look_start = None
            for i, dp in enumerate(data_points):
                time_entry, dp_range = dp.split(';')
                if not look_start:
                    look_start = time_entry

                if i == 0:
                    continue

                prev_time, prev_range = data_points[i - 1].split(';')

                time_entry_obj = datetime.datetime.strptime(time_entry, "%Y-%m-%dT%H:%M:%SZ")
                prev_time_obj = datetime.datetime.strptime(prev_time, "%Y-%m-%dT%H:%M:%SZ")

                if prev_range != dp_range:
                    df_entries.append(
                        [*sound_info, look_start, prev_time, prev_range]
                    )
                    look_start = time_entry
                    continue

                # Difference greater than 1 second ==> player looked away and then looked back
                diff = prev_time_obj - time_entry_obj
                if (time_entry_obj - prev_time_obj).seconds > 1:
                    df_entries.append(
                        [*sound_info, look_start, prev_time, prev_range]
                    )
                    look_start = time_entry
                    continue

            if len(data_points) > 0:
                last_time, last_range = data_points[-1].split(';')
                df_entries.append(
                    [*sound_info, look_start, last_time, last_range]
                )

    sfx_dfs.append(
        pd.DataFrame(df_entries,
                     columns=["Name", "Type", "Pos", "PlayStart", "PlayEnd", "LookStart", "LookEnd", "RangeType"])
    )

print(sfx_dfs[0].head(20))
