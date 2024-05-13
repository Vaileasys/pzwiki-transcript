
from codes_dict import replace_codes
from cat_dict import replace_cat
from calc_datetime import timestamp_to_datetime

# transforms each <BroadcastEntry> block into a translate block, with text from each <LineEntry>
def process_broadcast_entries(entries, output_file, channel_entry, log_file, broadcast_entry_count):
    channel_cat = get_channel_cat(channel_entry)

    for broadcast_entry in entries:
        broadcast_entry_count += 1
        icon = replace_cat(channel_cat)
        timestamp = broadcast_entry.get('timestamp')
        endstamp = broadcast_entry.get('endstamp')
        output_file.write(f"{{{{Transcript\n|icon={icon}")
        log_file.write(f"BroadcastEntry: ID=\"{broadcast_entry.get('ID')}\"\n")

        if timestamp is not None:
            time, date = timestamp_to_datetime(timestamp)
            output_file.write(f"\n|timestamp={timestamp}\n|time_start={time}\n|date={date}") # add timestamp value

            if endstamp is not None:
                time, date = timestamp_to_datetime(endstamp)
                output_file.write(f"\n|endstamp={endstamp}\n|time_end={time}") # add endstamp value
        
        output_file.write("\n|text=") # start transcript
        prev_person = None
        person_map = {}
        for line_entry in broadcast_entry.findall('.//LineEntry'):
            color = {'r': line_entry.get('r'), 'g': line_entry.get('g'), 'b': line_entry.get('b')}
            person = get_person(color, person_map)
            value = line_entry.text.strip() if line_entry.text else ""
            value = value.replace('[img=music]', '♪')
            codes = line_entry.get('codes') # Extract the value of the 'codes' attribute

            # if LineEntry has a moodle code, get the effect and add as a tooltip
            if codes:
                code_parts = []
                for code in codes.split(','):
                    code_part = code[:3] # get the moodle code
                    code_value = code[3:] if len(code) > 3 else "" # get the moodle value
                    code_part = replace_codes(code_part)  
                    code_parts.append(f"{code_part} {{{{mood|{code_value}}}}} ") # add moodle code and value to the list
                code_str = ", ".join(code_parts)

                # check if the person has changed so we know whether to start a new person block
                if person != prev_person: 
                    if prev_person is not None:
                        output_file.write("}}\n") # end previous person block
                    output_file.write(f"{{{{Transcript/row|{person}|{{{{tooltip|{value}|{code_str}}}}}<br>\n") # new person block with tooltip

                else:
                    output_file.write(f"{{{{tooltip|{value}|{code_str}}}}}<br>\n") # continue current person block with tooltip
                prev_person = person

            else:
                # check if the person has changed so we know whether to start a new person block
                if person != prev_person:
                    if prev_person is not None:
                        output_file.write("}}\n") # end previous person block

                    output_file.write(f"{{{{Transcript/row|{person}|{value}<br>\n") # new person block without tooltip

                else:
                    output_file.write(f"{value}<br>\n") # continue current person block without tooltip

                prev_person = person

        if prev_person is not None:
            output_file.write("}}") # close final person block

        output_file.write("}}<br>\n") # close transcript
        output_file.write('\n')

    return broadcast_entry_count

# gets unique person from rgb attributes and assigns an identifier (person1)
def get_person(color, person_map):
    key = tuple(color.values())
    if key in person_map:
        return person_map[key]
    else:
        person = f"person{len(person_map) + 1}"
        person_map[key] = person
        return person

# gets the "cat" attribute for <ChannelEntry>
def get_channel_cat(channel_entry):
    if channel_entry is not None and 'cat' in channel_entry.attrib and channel_entry.get('cat').strip() != "":
        return channel_entry.get('cat')
    else:
        return "Radio"