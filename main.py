# #!/usr/bin/python3

# for Windows App Packaging
import os, sys
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from kivy.resources import resource_add_path, resource_find
from kivy_deps import sdl2, glew

from textwrap import dedent

from plyer import filechooser

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout

from datetime import datetime

# for csv
import csv

# required for working with csv files globally
csv_files = []
master_fields = []
all_spreadsheets = []

sorting_dict = {}

desktop = os.path.expanduser("~/Desktop")
output_dir = "CSV_Manipulator"
custom_dir = ''

def merge_data(fields, rows):

    row_count = len(rows) # get total rows in current sheet
    # for every column in master sheet
    for m_field_num in range(len(master_fields)):
        m_field = master_fields[m_field_num]
        col_num = -1 # column translation between master_fields and fields from current sheet. Set to -1 to indicate no field was found.
        # Match column in master with column in current sheet
        for field_num in range(len(fields)):
            if m_field == fields[field_num]:
                col_num = field_num # assign correct translation column
                break
        # if match was found, append all rows in column.
        if col_num >= 0:
            for row in rows:
                all_spreadsheets[m_field_num].append(row[col_num])
        # if match was not found, append empty strings.
        elif col_num < 0:
            for _ in range(row_count): # As no variable is being used _ serves as a stand in.
                all_spreadsheets[m_field_num].append('')

    
    # print(len(all_spreadsheets))

    

def categorize_by_column(name, fallback_name):
    # Determine column number of "column_name" for sorting.
    sort_col = 0
    fallback_sort_col = 0
    for col_num in range(len(master_fields)):
        if name == master_fields[col_num]:
            sort_col = col_num
        elif fallback_name == master_fields[col_num]:
            fallback_sort_col = col_num

    # For all rows, check if primary sort_col contains a key in the dictionary.
    for sort_val_row in range(len(all_spreadsheets[sort_col])):
        sort_val = all_spreadsheets[sort_col][sort_val_row]

        if sort_val_row == 0: # header row
            continue
        if sort_val == '': # empty entry in primary sort column
            sort_val = all_spreadsheets[fallback_sort_col][sort_val_row] # revert to fallback

        # Place new sort_vals in dictionary
        if sort_val not in sorting_dict:
            sorting_dict[sort_val] = []

        # Add row to dictionary under proper key.
        sorting_dict[sort_val].append(sort_val_row)

    # print(sorting_dict)

def ret_lol(row_num_list):
    # print(row_num_list)
    ret_list = []
    for x in row_num_list:
        row = []
        for y in range(len(master_fields)):
            row.append(all_spreadsheets[y][x])
        ret_list.append(row)
    # print(ret_list)
    return ret_list

def write_to_csv(filename, dir_name, rows):
    filepath = os.path.join(dir_name, filename)

    # writing to csv file 
    with open(filepath, 'w', newline='') as csvfile:
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        
        # writing the fields 
        csvwriter.writerow(master_fields) 
        
        # writing the data rows 
        csvwriter.writerows(rows)


def output_csv_by_1stCategory():

    # Make new directory for file
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %Hh%Mm%Ss")
    if custom_dir != '': # if a folder was selected.
        new_dir = os.path.join(custom_dir, dt_string)
    else:
        directory = os.path.join(desktop, output_dir) # Desktop/CSV_Manipulator
        new_dir = os.path.join(directory, dt_string) # Desktop/CSV_Manipulator/datetime

    # if new_dir doesn't exist, make it.
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)

    # List of Lists [[list of rows in city 1], [list of rows in city 2], ... [list of rows in city n]]
    cat_list = []

    # Determine column number of "1stCategory" for sorting.
    firstCat_col = 0
    for col_num in range(len(master_fields)):
        if '1st Category' == master_fields[col_num]:
            firstCat_col = col_num
    
    keys = sorting_dict.keys()
    for key in keys:
        cat_list.append(sorting_dict[key])

    # for all rows in each city
    for city_row in cat_list:
        # Create a dictionary for every city using 1stCat as the key.
        cat_dict = {}
        for every_city in city_row:
            key_val = all_spreadsheets[firstCat_col][every_city] # fetch a profession in cat_list
            # if profession is not in cat_dict, add it.
            if key_val not in cat_dict:
                cat_dict[key_val] = []
            # Add row number to a city's profession dictionary key (e.g. if Detroit has a Carpenter, add which row it can be found on)
            cat_dict[key_val].append(every_city)
        # for all professions in the city
        for keys in cat_dict:
            # print(cat_dict[keys])
            csv_lol = ret_lol(cat_dict[keys]) # fetch row data for each profession, return a list of rows.
            profession = csv_lol[0][firstCat_col]
            profession_count = str(f'{(len(csv_lol)):03d}')
            profession_city = csv_lol[0][4] # Extracts city from State/Region column. magic number - will fix later
            if len(profession_city) < 3:
                profession_city = csv_lol[0][3]

            # print(csv_lol)
            # print(profession)
            # print(profession_count)
            # print(profession_city)
            filename = profession + ' ' + profession_city + ' ' + profession_count + '.csv'
            write_to_csv(filename, new_dir, csv_lol)



class FileChoose(Button):
    '''
    Button that triggers 'filechooser.open_file()' and processes
    the data response from filechooser Activity.
    '''

    selection = ListProperty([])

    def choose(self):
        '''
        Call plyer filechooser API to run a filechooser Activity.
        '''
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        '''
        Callback function for handling the selection response from Activity.
        '''
        self.selection = selection

    def on_selection(self, *a, **k):
        '''
        Update TextInput.text after FileChoose.selection is changed
        via FileChoose.handle_selection.
        '''
        selection_text = self.selection[0]
        # App.get_running_app().root.ids.result.text = str(self.selection)
        App.get_running_app().root.ids.stack_widget.add_widget(Label(text=str(selection_text), size_hint_y=str(0.1), halign='left'))
        csv_files.append(str(self.selection))

class Process(Button):
    '''
    Button that triggers the processing of selected csv files.
    '''

    def process(self):
        # print(csv_files)

        # reading csv file 
        for file in csv_files:
            loc = file[2:-2] # removes the first/last two characters from ['filename.extension'] to filename.extension

            fields = []
            rows = []

            with open(loc, 'r') as csvfile:
                # creating a csv reader object 
                csvreader = csv.reader(csvfile)

                fields = next(csvreader)
            
                # extracting each data row one by one
                for row in csvreader:
                    rows.append(row)

                # Some spreadsheets may have a limited number of columns. Insert specifically.
                merge_data(fields, rows)
        # end of input files loop

        # Separate the data into dictionary based on city (which happens to be in the State/Region column instead of City).
        categorize_by_column("State/Region", "City")

        # Output CSVs
        output_csv_by_1stCategory()
        # ret_lol([200])

        # get total number of rows
        print("Total no. of rows: %d"%(len(all_spreadsheets[0])))

########## add some sort of toast ###############
        sys.exit()

class FolderChoose(Button):
    '''
    Button that triggers 'filechooser.choose_dir()' and changes the save folder accordingly.
    '''

    def selectFolder(self):
        '''
        Call plyer directory chooser
        '''
        filechooser.choose_dir(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        '''
        Callback function for handling the selection response from Activity.
        '''
        global custom_dir # needed to modify global custom_dir
        self.selection = selection
        dir = selection[0]
        self.text = 'Save Folder Selected: ' + dir
        custom_dir = dir


class CSV_ManipulatorApp(App):
    '''
    Application class with root built in KV.
    '''

    def build(self):
        return Builder.load_string(dedent('''
            GridLayout:
                cols: 1
                Label:
                    size_hint_y: 0.1
                    # text: 'First, please select files one at a time, then hit process after selecting all files to be processed.\\nOutput will be stored in Desktop/CSV_Manipulator by default. CVS_Manipulator will exit on completion'
                    text: 'CSV Manipulator'
                    font_size: '48sp'
                    valign: 'middle'
                Process:
                    size_hint_y: 0.1
                    text: 'Process'
                    background_color: 0, 0, 1, 200
                    on_release: self.process()
                GridLayout:
                    cols: 2
                    padding: 5,5
                    size_hint_y: 0.2
                    TextInput:
                        id: merge1
                        text: 'Merge Name 1'
                        multiline: False
                        size_hint_y: 0.3
                    TextInput:
                        id: merge2
                        text: 'Merge Name 2'
                        multiline: False
                        size_hint_y: 0.3
                    GridLayout:
                        cols: 2
                        padding: 10,10
                        size_hint_y: 0.7
                        Label:
                            text: 'Category'
                        Label:
                            text: 'City'
                        CheckBox:
                            group: type
                        CheckBox:
                            group: type
                    Button:
                        text: 'Merge'
                        size_hint_y: 0.7
                FolderChoose:
                    id: folder
                    size_hint_y: 0.1
                    text: 'Save Folder Selected: Desktop/CSV_Manipulator (default)'
                    on_release: self.selectFolder()
                FileChoose:
                    size_hint_y: 0.1
                    on_release: self.choose()
                    text: 'Insert a file'
                Label:
                    text: 'Files inserted:'
                    halign: 'left'
                    valign: 'top'
                    size_hint_y: 0.1
                    text_size: self.size
                StackLayout:
                    id: stack_widget
                    size_hint_y: 0.3
        '''))


if __name__ == '__main__':
    # for bundling data with this kivy app for windows
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))

    path = os.path.join(desktop, output_dir)
    if not os.path.isdir(path):
        os.mkdir(path)

    # set up master_fields to get total fields sample. Assumes master sample is in same directory as executable.
    with open('CSV-All-Columns-Sample.csv', 'r') as csvfile:
        # creating a csv reader object 
        csvreader = csv.reader(csvfile)

        # extracting field names through first row of the master columns sample.
        master_fields = next(csvreader)
        # print('Field names are:' + ', '.join(field for field in master_fields))
        
        for fields in master_fields:
            all_spreadsheets.append([fields])

    # run kivy app
    CSV_ManipulatorApp().run()