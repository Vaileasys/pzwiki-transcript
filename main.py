import os
import xml.etree.ElementTree as ET
from broadcast_entries import process_broadcast_entries

def main():
    # for counting the number of lines processed
    channel_entry_lines = 0
    broadcast_entry_count = 0

    while True:
        # prompt user for file path
        file_path = input("Enter the path of the file: ")

        # check if the provided path exists and if it's a file
        if os.path.exists(file_path) and os.path.isfile(file_path):
            break
        else:
            print("Invalid path. Please enter the correct path to the file.")
    
    # extract directory of the script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    tree = ET.parse(file_path)
    root = tree.getroot()

    with open(os.path.join(script_dir, 'output.txt'), 'w', encoding='utf-8') as output_file,\
        open(os.path.join(script_dir, 'Log.txt'), 'w', encoding='utf-8') as log_file:
        for element in root:

            if element.tag == 'Adverts':
                output_file.write("==Adverts==\n")
                log_file.write("Starting Adverts\n")
                process_broadcast_entries(element.findall('.//BroadcastEntry'), output_file, None, log_file, broadcast_entry_count)
                channel_entry_lines += 1 

            elif element.tag == 'Channels':
                output_file.write("==Channels==\n")
                log_file.write("Starting Channels\n")

                for channel_entry in element.findall('ChannelEntry'):
                    channel_id = channel_entry.get('ID')
                    channel_name = channel_entry.get('name')
                    channel_cat = channel_entry.get('cat')
                    channel_freq = channel_entry.get('freq')

                    # write ChannelEntry to log
                    log_file.write(f"ChannelEntry: ID=\"{channel_id}\" name=\"{channel_name}\" cat=\"{channel_cat}\" freq=\"{channel_freq}\"\n")
                    output_file.write(f"==={channel_name}===\n")
                    broadcast_entry_count += process_broadcast_entries(channel_entry.findall('.//BroadcastEntry'), output_file, channel_entry, log_file, broadcast_entry_count)
                    channel_entry_lines += 1 
                    
        log_file.write(f"Total ChannelEntry: {channel_entry_lines}\nTotal BroadcastEntry: {broadcast_entry_count}")
        print(f"ChannelEntry: {channel_entry_lines}")
        print(f"BroadcastEntry: {broadcast_entry_count}")
        print(f"{os.path.basename(output_file.name)} created in {script_dir}")
        print(f"Process completed successfully.")

if __name__ == "__main__":
    main()
