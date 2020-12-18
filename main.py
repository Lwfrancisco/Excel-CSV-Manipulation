#!/usr/bin/python3

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

kivy.require('1.10.0')

class RootWidget(BoxLayout):
    '''Create a controller that receives a custom widget from the kv lang file.
    Add an action to be called from a kv file.
    '''

    container = ObjectProperty(None)

class CSV_Manipulation(App):
    '''This is the app itself'''

    def build(self):
        '''This method loads the root.kv file automatically
        :return: none
        '''
        # loading the content of root.kv
        self.root = Builder.load_file('kv_modes/root.kv')

    def screen_select(self, selector):
        '''
        :param selector: character that is dependant on which mode button is toggled.
        :return:
        '''

        filename = selector + '.kv'
        # unload the content of the .kv file
        # reason: may have data from previous calls
        Builder.unload_file('kv_modes/' + filename)
        # clear the container
        self.root.container.clear_widgets()
        # load the .kv file
        selector = Builder.load_file('kv_modes/' + filename)
        # add content of the .kv file to the container
        self.root.container.add_widget(selector)


if __name__ == '__main__':
    '''Start the application'''

    CSV_Manipulation().run()