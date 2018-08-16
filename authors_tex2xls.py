import re
from collections import defaultdict
import string

import pandas as pd

try:
    import xlwt  # noqa
except ImportError:
    raise ImportError('pandas Excel writer needs xlwt package')

affil_patt0 = re.compile(
    '\\\\newcommand{(\\\\\w+)}{\\\\affiliation{\\\\it{(.+)}}}')
affil_patt1 = re.compile(
    '\\\\newcommand{(\\\\\\w+)}{\\\\affiliation{(.+)}}')
affil_patt2 = re.compile('\\\\affiliation\{(.+)\}')
author_patt = re.compile('\\\\author?.+\{(.+)\}')
email_patt = re.compile('\\\\email\{(.+)\}')


def parse_tex(filename='authors.tex', outfile='Authors_Astroquery.xls',
              debug=False):
    with open(filename) as ftex:
        all_lines = ftex.readlines()

    i = 0
    cmd = {}
    author_info = defaultdict(str)

    pd.set_option('display.max_colwidth', -1)  # Do not truncate
    df = pd.DataFrame(columns=[
        'Is Corresponding Author', 'Author Order', 'Title', 'Given Name/First Name',
        "Middle Initial(s) or Name", 'Family Name/Surname', 'Email',
        'Telephone', 'Institution'])

    def parsename(name):
        components = name.split()
        first = components.pop(0)
        last = components.pop(-1)
        middle = " ".join(components)
        return {"first": first,
                "middle": middle,
                "last": last}
    
    def parseaffil(affil):
        components = [x.strip() for x in affil.split(",")]
        success = False
        for ii,com in enumerate(components):
            if len(com) > 0 and (com[0] in string.digits or com[-1] in string.digits):
                address = components[ii:]
                success = True
                break
        if not success:
            return

        print(address)

        result = {'Address Line 1': address[0],
                  'Address Line 2': "",
                  'City': address[1],
                  'State/Province': address[2].split()[0] if len(address) > 3 else "",
                  'Zip/Postal Code': address[2].split()[1] if len(address) > 3 else "",
                  'Country': address[3] if len(address) > 3 else address[2],
                 }

        return result


    def _insert_df_row(df, author_info):
        namedict = parsename(author_info['name'])
        address = parseaffil(author_info['affil'])
        print(address)
        return df.append({'Is Corresponding Author': author_info['corresp'],
                          'Author Order': author_info['order'],
                          'Title': '',
                          'Given Name/First Name': namedict['first'],
                          'Middle Initial(s) or Name': namedict['middle'],
                          'Family Name/Surname': namedict['last'],
                          'Email': author_info['email'],
                          'Telephone': '',
                          'Institution': author_info['affil'],
                          'Department': '',
                         },
                         ignore_index=True)

    for line in all_lines:
        row = line.strip()

        # Blank line
        if len(row) == 0:
            continue

        # Affil shortcuts
        if 'newcommand' in row:
            m = affil_patt0.match(row)
            if m is None:
                m = affil_patt1.match(row)
            if m is None:
                print('Failed to regex {}'.format(row))
            else:
                cmd[m.group(1)] = m.group(2)

        # Process new author
        elif row.startswith('\\author'):
            # Write out previous author
            if len(author_info['name']) > 0:
                df = _insert_df_row(df, author_info)

            i += 1
            author_info = defaultdict(str)
            author_info['order'] = i
            m = author_patt.match(row)
            if m is None:
                print('Failed to regex {}'.format(row))
            else:
                author_info['name'] = m.group(1)

        # Author affiliation (one to many, only keep first)
        elif row.startswith('\\affiliation'):
            m = affil_patt2.match(row)
            if m is not None:
                if 'affil' in author_info:
                    # author_info['affil'] += '; {}'.format(m.group(1))
                    print('Ignoring extra affil for {}: {}'.format(
                        author_info['name'], m.group(1)))
                else:
                    author_info['affil'] = m.group(1)

        # Author email
        elif row.startswith('\\email'):
            m = email_patt.match(row)
            if m is None:
                print('Failed to regex {}'.format(row))
            else:
                author_info['email'] = m.group(1)

        # Corresponding author
        elif row.startswith('\\correspondingauthor'):
            author_info['corresp'] = 'Yes'

        # Expand author affiliation shortcut
        elif row in cmd:
            if 'affil' in author_info:
                # author_info['affil'] += '; {}'.format(cmd[row])
                print('Ignoring extra affil for {}: {}'.format(
                    author_info['name'], cmd[row]))
            else:
                author_info['affil'] = cmd[row]

        else:
            print('No directive for row {}'.format(row))

    # Write out last author
    df = _insert_df_row(df, author_info)

    if debug:
        print(df)

    # Write to Excel
    writer = pd.ExcelWriter(outfile)
    df.to_excel(writer, 'Contributing Author Information', index=False)
    writer.save()
    print('Wrote', outfile)


if __name__ == '__main__':
    parse_tex()
