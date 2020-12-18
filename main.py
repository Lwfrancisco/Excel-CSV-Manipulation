# #!/usr/bin/python3

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
master_rows = []

all_spreadsheets = [[]]


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

            with open(loc, 'r') as csvfile:
                # creating a csv reader object 
                csvreader = csv.reader(csvfile)
            
                # extracting each data row one by one
                for row in csvreader:
                    rows.append(row)
            
                # get total number of rows
                print("Total no. of rows: %d"%(csvreader.line_num))
                print('Field names are:' + ', '.join(field for field in master_fields))


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
    # set up master_fields to get total fields sample. Assumes master sample is in same directory as executable.
    with open('CSV-All-Columns-Sample.csv', 'r') as csvfile:
        # creating a csv reader object 
        csvreader = csv.reader(csvfile)

        # extracting field names through first row of the master columns sample.
        master_fields = next(csvreader)
        # print('Field names are:' + ', '.join(field for field in master_fields))

    # run kivy app
    ChooserApp().run()