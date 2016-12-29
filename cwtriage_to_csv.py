#!/usr/bin/env python3

import json
import ipdb
import csv


def pull_data(csv_str):
    data = json.loads(csv_str)

    csv_data = []
    csv_data += [data['entry']['orig_filename']]
    csv_data += [data['entry']['info']['classification']]
    csv_data += [data['entry']['info']['faulting_insn']['address']]
    csv_data += [data['entry']['info']['faulting_insn']['text']]

    stack_max = 30
    if len(data['entry']['info']['stack']) < 30:
            stack_max = len(data['entry']['info']['stack'])
    for i in range(stack_max):
        csv_data += [data['entry']['info']['stack'][i]['module']]
        csv_data += ["0x%013x" % int(data['entry']['info']['stack'][i]['address'])]
        csv_data += [data['entry']['info']['stack'][i]['symbol']]
    if stack_max < 30:
            for i in range(30-stack_max):
                    csv_data += ['']

    #csv_data += data['entry']['info']['registers']
    for i in range(24):
        csv_data += [data['entry']['info']['registers'][i]['name']]
        csv_data += ["0x%013x" % int(data['entry']['info']['registers'][i]['value'])]
    return csv_data

filename = "output.json"

with open(filename) as data_file:
        content = data_file.readlines()

full_data = []
for line in content:
        full_data += [pull_data(line)]

csv_header = []
csv_header += ["Filename"]
csv_header += ["Classification"]
csv_header += ["FaultingAddr"]
csv_header += ["FaultingTxt"]

csv_header += ["Stack01Module"]
csv_header += ["Stack01Address"]
csv_header += ["Stack01Symbol"]

csv_header += ["Stack02Module"]
csv_header += ["Stack02Address"]
csv_header += ["Stack02Symbol"]

csv_header += ["Stack03Module"]
csv_header += ["Stack03Address"]
csv_header += ["Stack03Symbol"]

csv_header += ["Stack04Module"]
csv_header += ["Stack04Address"]
csv_header += ["Stack04Symbol"]

csv_header += ["Stack05Module"]
csv_header += ["Stack05Address"]
csv_header += ["Stack05Symbol"]

csv_header += ["Stack06Module"]
csv_header += ["Stack06Address"]
csv_header += ["Stack06Symbol"]

csv_header += ["Stack07Module"]
csv_header += ["Stack07Address"]
csv_header += ["Stack07Symbol"]

csv_header += ["Stack08Module"]
csv_header += ["Stack08Address"]
csv_header += ["Stack08Symbol"]

csv_header += ["Stack09Module"]
csv_header += ["Stack09Address"]
csv_header += ["Stack09Symbol"]

csv_header += ["Stack10Module"]
csv_header += ["Stack10Address"]
csv_header += ["Stack10Symbol"]

csv_header += ["Stack11Module"]
csv_header += ["Stack11Address"]
csv_header += ["Stack11Symbol"]

csv_header += ["Stack12Module"]
csv_header += ["Stack12Address"]
csv_header += ["Stack12Symbol"]

csv_header += ["Stack13Module"]
csv_header += ["Stack13Address"]
csv_header += ["Stack13Symbol"]

csv_header += ["Stack14Module"]
csv_header += ["Stack14Address"]
csv_header += ["Stack14Symbol"]

csv_header += ["Stack15Module"]
csv_header += ["Stack15Address"]
csv_header += ["Stack15Symbol"]

csv_header += ["Stack16Module"]
csv_header += ["Stack16Address"]
csv_header += ["Stack16Symbol"]

csv_header += ["Stack17Module"]
csv_header += ["Stack17Address"]
csv_header += ["Stack17Symbol"]

csv_header += ["Stack18Module"]
csv_header += ["Stack18Address"]
csv_header += ["Stack18Symbol"]

csv_header += ["Stack19Module"]
csv_header += ["Stack19Address"]
csv_header += ["Stack19Symbol"]

csv_header += ["Stack20Module"]
csv_header += ["Stack20Address"]
csv_header += ["Stack20Symbol"]

csv_header += ["Stack21Module"]
csv_header += ["Stack21Address"]
csv_header += ["Stack21Symbol"]

csv_header += ["Stack22Module"]
csv_header += ["Stack22Address"]
csv_header += ["Stack22Symbol"]

csv_header += ["Stack23Module"]
csv_header += ["Stack23Address"]
csv_header += ["Stack23Symbol"]

csv_header += ["Stack24Module"]
csv_header += ["Stack24Address"]
csv_header += ["Stack24Symbol"]

csv_header += ["Stack25Module"]
csv_header += ["Stack25Address"]
csv_header += ["Stack25Symbol"]

csv_header += ["Stack26Module"]
csv_header += ["Stack26Address"]
csv_header += ["Stack26Symbol"]

csv_header += ["Stack27Module"]
csv_header += ["Stack27Address"]
csv_header += ["Stack27Symbol"]

csv_header += ["Stack28Module"]
csv_header += ["Stack28Address"]
csv_header += ["Stack28Symbol"]

csv_header += ["Stack29Module"]
csv_header += ["Stack29Address"]
csv_header += ["Stack29Symbol"]

csv_header += ["Stack30Module"]
csv_header += ["Stack30Address"]
csv_header += ["Stack30Symbol"]

with open("output.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
        writer.writerows(full_data)
