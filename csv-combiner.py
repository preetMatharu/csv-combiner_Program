import sys
import csv
import pandas as pd
import os
import os.path


fi = []
wr = []
files_list = []
cols = ['email_hash', 'category', 'filename']
bool_written_to_file = False
some_file_not_found = False


def create_output_file(str_input):
    global fi
    fi = open(str_input, 'w', newline='')
    global wr
    wr = csv.DictWriter(fi, fieldnames=cols)
    wr.writeheader()


def write_to_output_file(str_input):
    str_lst = str_input.split(',')
    global wr
    wr.writerow({cols[0]: '"{}"'.format(str_lst[0]),
                 cols[1]: '"{}"'.format(str_lst[1]),
                 cols[2]: '"{}"'.format(str_lst[2])})
    global bool_written_to_file
    if not bool_written_to_file:
        bool_written_to_file = True


def close_output_file():
    global fi
    fi.close()


def read_write_helper(filename, chunk_size):
    for chunk in pd.read_csv(filename, chunksize=chunk_size):
        chunk = chunk.reset_index()
        clean_file_name = filename[filename.rindex('/') + 1: filename.__len__()]
        for index, row in chunk.iterrows():
            write_to_output_file(row['email_hash'] + ',' + row['category'] + ',' + clean_file_name)


def main():
    print('Use: [csv-combiner.py InputFile_1 InputFile_2 > OutputFile]')
    create_output_file(str(sys.argv[sys.argv.__len__() - 1]))

    for args in sys.argv[1:sys.argv.__len__()-1]:
        if os.path.exists(args) and args[-4:] == '.csv':
            files_list.append(args)
        elif '>' == args:
            continue
        else:
            global some_file_not_found
            some_file_not_found = True
            files_list.append('[**Not Found**]: ' + args)
            sys.stdout.write('Enter valid file name(s): [' + args + '] does not exist\n')

    for file in files_list:
        if '[**Not Found**]' not in file:
            chunk_size = 1000
            read_write_helper(file, chunk_size)

    close_output_file()

    if some_file_not_found and not bool_written_to_file:
        sys.stdout.write('No files found\n')
        sys.stdout.write('No output written')
        os.remove(str(sys.argv[sys.argv.__len__() - 1]))
    elif some_file_not_found and bool_written_to_file:
        sys.stdout.write('Not all files were found\n')
        sys.stdout.write('Output written to ' + str(sys.argv[sys.argv.__len__() - 1]))
    elif not some_file_not_found and bool_written_to_file:
        sys.stdout.write('Success!!\n')
        sys.stdout.write('Output written to: ' + str(sys.argv[sys.argv.__len__() - 1]))


if __name__ == "__main__":
    main()
