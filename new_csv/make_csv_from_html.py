#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, re

def main():
    args = sys.argv
    if len(args) != 2:
        print("usage: ./make_csv_from_html.py path/to/dir/with/html")
        sys.exit(1)

    #datum
    re_date = re.compile(r"""
        <\s*h3\s*>\s*(?P<date>[^<]+?)\s*<\s*\/\s*h3\s*>
            """, re.VERBOSE)

    #lokacija
    re_location1 = re.compile(r"""
        <\s*h2\s*>\s*Location\s*<\s*\/h2\s*>(.|\s)*?</div
        """, re.VERBOSE)

    #uza lokacija
    re_location2 = re.compile(r"""
        <\s*span\s*>(?P<address_part>(.|\s)*?)<
        """, re.VERBOSE)

    #ucesnici
    re_participants = re.compile(r"""
        <\s*h2\s*>\s*Participants\s*<\s*\/h2\s*>(.|\s)*?</div
        """, re.VERBOSE)

    #ucesnici, suzen izbor
    re_regex1 = re.compile(r"""
        <\s*ul\s*>(.|\s)*?<\s*\/ul\s*>
        """, re.VERBOSE)

    #type:value
    re_regex_type_value = re.compile(r"""
        <li\s*>(?P<type>(.|\s)*?):(?P<value>(.|\s)*?)<
        """, re.VERBOSE)

    #korisceno oruzje
    re_guns_involved = re.compile(r"""
        <\s*h2\s*>\s*Guns\s*Involved\s*<\s*\/h2\s*>(.|\s)*?</div
        """, re.VERBOSE)


    directory = args[1]
    abs_dir_path = os.path.abspath(directory)
    out_csv_path = abs_dir_path.rsplit('/')[-2]

    #izlazni .csv fajl za pisanje
    with open(out_csv_path + ".csv", "w") as f:

        #zaglavlje fajla, imena atributa
        f.write(("#ID,"
                "\"Incident Date\","
                "State,"
                "City,"
                "Geolocation,"
                "\"Guns Involved\","
                "\"Gun Types\","
                "\"Guns Stolen\","
                "Type,"
                "Name,"
                "Age,"
                "\"Age Group\","
                "Gender,"
                "Status")
                + os.linesep)

        #za mapu
        geo_csv = open(out_csv_path + "_GEOLOCATION.csv", 'w')
        geo_csv.write('name,lat,lon' + os.linesep)

        #obilazak svih html fajlova
        for (dirpath, dirnames, files) in os.walk(abs_dir_path):
            for curr_file in files:
                path = abs_dir_path + '/' + curr_file

                with open(path, "r") as g:
                    html_file = g.read()


                #trazenje datuma
                x = re_date.search(html_file)
                date = x.group('date') if x else "N/A"

                #trazenje lokacije
                State = "N/A"
                City = "N/A"
                Geo_location = "N/A"
                x = re_location1.search(html_file)
                if x != None:
                    location1 = x.group()

                    for y in re_location2.finditer(location1):
                        part = y.group('address_part')
                        if ',' in part and ':' not in part:
                            part1 = part.split(',')
                            City = part1[0].strip()
                            State = part1[1].strip()
                        if ":" in part:
                            Geo_location = part.split(':')[1].strip()


                #koliko je oruzja korisceno, koje je i da li je ukradeno
                Guns_Involved = "N/A"
                Gun_Types = "N/A"
                Guns_Stolen = "N/A"

                #moze biti vise oruzja pa ce biti predstavljeni listom: tipovi i da li je ukradeno
                gun_types = []
                is_guns_stolen = []
                x = re_guns_involved.search(html_file)
                if x != None:
                    guns_involved = x.group()

                    for y in re_regex_type_value.finditer(guns_involved):
                        key = y.group('type').strip()
                        value = y.group('value').strip()

                        if key == 'Type':
                            gun_types.append(value)
                        elif key == 'Stolen':
                            is_guns_stolen.append(value)

                if len(gun_types) != 0:
                    Guns_Involved = len(gun_types)
                    Gun_Types = str(gun_types).replace('[', '').replace(']', '').replace('\'', '').replace('Unknown', 'N/A')
                    Guns_Stolen = str(is_guns_stolen).replace('[', '').replace(']', '').replace('\'', '').replace('Unknown', 'N/A')


                x = re_participants.search(html_file)
                if x != None:
                    participants = x.group()

                    for z in re_regex1.finditer(participants):
                        subject = z.group()

                        Type = "N/A"
                        Name = "N/A"
                        Age = "N/A"
                        Age_group = "N/A"
                        Gender = "N/A"
                        Status = "N/A"

                        for y in re_regex_type_value.finditer(subject):
                            key = y.group('type').strip()
                            value = y.group('value').strip()

                            if key == 'Type':
                                Type = value
                            elif key == 'Name':
                                Name = value
                            elif key == 'Age':
                                Age = value
                            elif key == 'Age Group':
                                Age_group = value
                            elif key == 'Gender':
                                Gender = value
                            elif key == 'Status':
                                Status = value

                        #za svaku osobu se dodaje novi red u fajlu
                        line = [curr_file, date, State, City, Geo_location, str(Guns_Involved), Gun_Types, Guns_Stolen, Type, Name, Age, Age_group, Gender, Status]
                        str_line = '\"' +  '\",\"'.join(line) + '\"' + os.linesep
                        f.write(str_line)

                        #geo_csv za geolocation visual
                        if Geo_location != "N/A":
                            geo_csv.write('\"' + City + '\"' + ',' + Geo_location.replace(' ', '') + os.linesep)
        geo_csv.close()


if __name__ == "__main__":
    main()
