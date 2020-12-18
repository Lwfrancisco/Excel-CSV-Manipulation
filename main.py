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

# for csv
import csv

# required for working with csv files globally
csv_files = []
master_fields = []
all_spreadsheets = []

sorting_dict = {}

def merge_data(fields, rows):
    # for every column in current spreadsheet
    for field_num in range(len(fields)):
        col_name = fields[field_num]
        col_num = 0
        # iterate across the set of master_columns in master_fields, find which column corresponds to which master column
        for i in range(len(master_fields)):
            if col_name == master_fields[i]:
                col_num = i               
                break
        for row in rows:
            all_spreadsheets[i].append(row[field_num])

def categorize_by_column(name, fallback_name):
    # Determine column number of "column_name" for sorting.
    sort_col = 0
    fallback_sort_col = 0
    for col_num in range(len(master_fields)):
        if name == master_fields[col_num]:
            sort_col = col_num
        elif fallback_name == master_fields[col_num]:
            fallback_sort_col = col_num
    
    # Primary sort columns
    for sort_val in set(all_spreadsheets[sort_col][1:]):
        sorting_dict[sort_val] = []
    
    for row_num in range(len(all_spreadsheets[0]) - 1):
        sort_data = all_spreadsheets[sort_col][row_num]

        if row_num == 0: # skip first row - it only has column names
            continue
        # trigger fallback sort column if no data exists for primary sort column.
        elif sort_data == '':
            fallback_sort_data = all_spreadsheets[fallback_sort_col][row_num]
            # print(fallback_sort_data)
            # if fallback sort column is not yet in the sorting dictionary, add it as a key.
            if(fallback_sort_data not in sorting_dict):
                sorting_dict[fallback_sort_data] = []
            sorting_dict[fallback_sort_data].append(row_num)
            continue

        sorting_dict[sort_data].append(row_num)

    # print(sorting_dict)


    def output_csv_by_1stCategory():
        pass

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
        # App.get_running_app().root.ids.result.text = str(self.selection)
        App.get_running_app().root.add_widget(Label(text=str(self.selection), size_hint_y=str(0.05)))
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

        # get total number of rows
        print("Total no. of rows: %d"%(len(all_spreadsheets[0])))

########## add some sort of toast ###############
        exit()


class ChooserApp(App):
    '''
    Application class with root built in KV.
    '''

    def build(self):
        return Builder.load_string(dedent('''
            <FileChoose>:
            # BoxLayout:
            #     BoxLayout:
            #         orientation: 'vertical'
            BoxLayout:
                orientation: 'vertical'
                Label:
                    size_hint_y: 0.05
                    text: 'First, please select the files you wish to process. Then hit the process button.'
                Process:
                    size_hint_y: 0.1
                    text: 'Process'
                    on_release: self.process()
                FileChoose:
                    size_hint_y: 0.1
                    on_release: self.choose()
                    text: 'Select a file'
        '''))


if __name__ == '__main__':
    # for bundling data with this kivy app for windows
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))

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
    ChooserApp().run()