# #!/usr/bin/python3

from textwrap import dedent

from plyer import filechooser

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.label import Label

csv_files = []


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
                    size_hint_y: 0.2
                    text: 'First, please select the files you wish to process. Then hit the process button.'
                FileChoose:
                    size_hint_y: 0.1
                    on_release: self.choose()
                    text: 'Select a file'
        '''))


if __name__ == '__main__':
    ChooserApp().run()