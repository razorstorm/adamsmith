import time
import json
import os
import json


rootdir = 'src/fb/'
NAME_BLACK_LIST = {'facebook user'}
outputdir = 'output/fb/output.json'
mah_name = 'jason jiang'


def combine_messages():
    output_messages = []
    with open(outputdir, 'w') as output_fh:
        num_files = 0
        for _, dirnames, filenames in os.walk(rootdir):
            num_files += len(filenames)

        index = 0
        for subdir, dirs, files in os.walk(rootdir):

            for file in files:
                if file.endswith('.json'):
                    with open(subdir + "/" + file) as fh:
                        contents = fh.read()
                        json_contents = json.loads(contents)
                        participants = json_contents['participants']
                        if len(participants) == 2:
                            messages = json_contents['messages']
                            trimmed_messages = [
                                {'friend_display_name': m['sender_name'], 'time_stamp': m['timestamp_ms']} for m in messages if m['sender_name'].lower() != mah_name
                            ]
                            output_messages += trimmed_messages
                index += 1
                print(index, '/', num_files, end="\r")

        output_dict = {'messages': output_messages}
        output_fh.write(json.dumps(output_dict))


combine_messages()
