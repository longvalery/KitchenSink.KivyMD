# -*- coding: utf-8 -*-
import time
from datetime import datetime, date, timedelta
from platform import platform
from random import randrange
from typing import Union
import os
import re

import kivy
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.modules import keybinding

# This import for normal application
# from kivymd.app import MDApp
# This import need for reload and Change Languages
from kivymd.tools.hotreload.app import MDApp
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDColorPicker, MDDatePicker, MDTimePicker
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem, OneLineListItem
from kivymd.uix.button import MDIconButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.transition import MDFadeSlideTransition, MDSlideTransition, MDSwapTransition
## The following lines are needed for Pyinstaller. Do not delete them if you need to create an exe-file.
from kivymd.uix.navigationdrawer import MDNavigationLayout
from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.slider import MDSlider
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.backdrop import MDBackdrop
from kivymd.uix.banner import MDBanner

##

kivy.require("2.2.1")
# I'll try disabling the log messages
os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["KIVY_NO_FILELOG"] = "1"

# set size of application
Window.size = (400, 600)

define_classes = """
<MDSmartTileForGrid@MDSmartTile>
    radius: 16
    box_radius: [16, 16, 0, 0]
    box_position: "header"
    lines: 1

<DrawerClickableItemColor@DrawerClickableItem>
    text_right_color: app.theme_cls.primary_color
    text_color:       app.theme_cls.primary_color
    icon_color:       app.theme_cls.primary_color 


# Define your background color Template
<BackgroundColor@Widget>
    background_color: 1, 1, 1, 1
    canvas.before:
        Color:
            rgba: root.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.height / 6,]    
# Now you can simply Mix the `BackgroundColor` class with almost
# any other widget... to give it a background.
<BackgroundLabel@MDLabel+BackgroundColor>
    theme_text_color: 'Custom'
    text_color: self.theme_cls.primary_dark if (self.theme_cls.theme_style == 'Dark') else app.theme_cls.primary_light
    background_color: app.theme_cls.opposite_bg_light if (self.theme_cls.theme_style == 'Dark') else app.theme_cls.opposite_bg_dark

<Tab>:
    MDLabel:
        pos_hint: {"center_x": .5, "center_y": 1}

<MyPopup@Popup>
    auto_dismiss: True
    id: idMyPopup
    title: app.messages[app.current_language]["PopupExit"] # "Press <Esc> or Float button for exit"
    FloatLayout:
        MDSmartTile:
            id: popupImage
            mipmap: True
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            source: ''
            on_release: toast.toast("You can't go out like that")
            OneLineListItem:
                id:OneLineListItemCaption
                font_style: 'Caption'
        MDFloatingActionButton:
            icon:               'close-box-outline'
            opposite_colors:    True
            elevation_normal:    5
            id : MDFloatingActionButtonCloseBoxOutline
            pos_hint: {'center_x': 0.95, 'center_y': 0.05}
            on_release: root.dismiss()

<Content>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"
    MDTextField:
        hint_text: "City"
    MDTextField:
        hint_text: "Street"

<ContentPanel>
    orientation: "vertical"
    size_hint_y: None
    height: self.minimum_height

    TwoLineIconListItem:
        id: infopanel
        text: "(050)-123-45-67"
        secondary_text: "Mobile. Press me to call"
        IconLeftWidget:
            icon: 'phone'

<DrawerClickableItem@MDNavigationDrawerItem>
    focus_color: "#e7e4c0"
    text_color: app.theme_cls.primary_dark
    icon_color: app.theme_cls.primary_dark

#    text_color: "#4a4939" if (self.theme_cls.theme_style == 'Light') else "#e6d919"
#    icon_color: "#4a4939" if (self.theme_cls.theme_style == 'Light') else "#e6d919"
    ripple_color: "#c5bdd2"
    selected_color: "#0c6c4d"
    close_on_click: True


<DrawerLabelItem@MDNavigationDrawerItem>
    text_color: app.theme_cls.primary_dark
    icon_color: app.theme_cls.primary_dark
    focus_behavior: False
    selected_color: "#4a4939"
    _no_ripple_effect: True

<ItemBackdropFrontLayer@TwoLineAvatarListItem>
    icon: "android"
    IconLeftWidget:
        icon: root.icon

<MyBackdropFrontLayer@ItemBackdropFrontLayer>
    backdrop: None
    text: "Lower the front layer"
    secondary_text: " by 50 %"
    icon: "transfer-down"
    on_press: root.backdrop.open(-Window.height / 2)
    pos_hint: {"top": 1}
    _no_ripple_effect: True
    FloatLayout:
        orientation: "vertical"
        pos_size_y: 1
        pos_hint: {"top": 0}
        MDLabel:
            halign: "center"
            pos_size_y : 0.2
            pos_hint: {"top": 0.6}
            text : "There could be \\n something useful here"
        MDLabel:
            halign: "center"
            pos_size_y : 0.2
            pos_hint: {"top": 0.0}
            text : "Or here"

<MyBackdropBackLayer@Image>
    size_hint: .8, .8
    source: os.path.join(images_path, "logo", "kivymd-icon-512.png")
    pos_hint: {"center_x": .5, "center_y": .6}

<CardScreenLabel@Label>
    adaptive_height: True
    color: "#1e4974"
    font_style: "Caption"
    theme_text_color: 'Primary'  if app.theme_cls.theme_style == 'Light' else "ContrastParentBackground"
    opposite_colors: False if app.theme_cls.theme_style == 'Light' else True
                            # text_color: "Black"
                            # opposite_text_color: "White"
    text_color: app.theme_cls.primary_light if app.theme_cls.theme_style == 'Light' else app.theme_cls.primary_dark 

"""

main_widget_kv = """
## This export is necessary because some messages will be send from this Kivy file  
#:import toast kivymd.toast 

# Main application screen
MDScreen:
    MDNavigationLayout:
        MDScreenManager:
            id: manager
            orientation: 'vertical'
            MDScreen:
                MDTopAppBar:
                    id: idMainMenuTitle
                    name: "idMainMenuTitle"
                    title: app.messages[app.current_language]["MainMenuTitle"] # "Navigation Drawer"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarNavigationDrawer
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

            Screen:
                name: 'buttons'
                id: buttons
                MDTopAppBar:
                    id: idButtonsMenuTitle
                    name: "idButtonsMenuTitle"
                    title: app.messages[app.current_language]["ButtonsMenuTitle"] # "Some buttons. Please click on all of them"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarButtons
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                BoxLayout:
                    orientation: 'vertical'
                    padding: '50sp'
                    spacing: '20sp'

                    MDLabel:

                    MDIconButton:
                        icon: 'sd'
                        id: MDIconButton
                        pos_hint: {'center_x': 0.5}
                        disabled: disable_the_buttons.active
                        on_release:
                            app.on_click_button(self)
                    MDFlatButton:
                        id: MDFlatButton
                        text: 'MDFlatButton'
                        pos_hint: {'center_x': 0.5}
                        disabled: disable_the_buttons.active
                        on_release:
                            app.on_click_button(self)

                    MDRaisedButton:
                        text: "MDRaisedButton"
                        id: MDRaisedButton
                        elevation_normal: 2
                        opposite_colors: True
                        pos_hint: {'center_x': 0.5}
                        disabled: disable_the_buttons.active
                        on_release:
                            app.on_click_button(self)

                    MDFloatingActionButton:
                        id:                 MDFloatingActionButton
                        icon:               'plus'
                        opposite_colors:    True
                        elevation_normal:    8
                        pos_hint: {'center_x': 0.5}
                        disabled: disable_the_buttons.active
                        on_release:
                            app.on_click_button(self)

                    MDLabel:

                    BoxLayout:
                        padding: '12dp'
                        spacing: '12sp'
                        MDCheckbox:
                            id: disable_the_buttons
                            size_hint_x: 0.4
                            padding: ['300dp', '5dp', '0dp', '5dp']
                            pos_hint: {'x': 1}

                        MDLabel:
                            font_style: 'Body1'
                            theme_text_color: 'Primary'
                            text: "Disable all buttons"
                            size_hint_x:None
                            width: '56dp'
                            text_size: self.size
                            halign: 'left'
                            valign: 'middle'
                            size_hint_x: 0.6

                    MDLabel:


            Screen:
                name: 'bottomsheet'
                id: bottomsheet
                MDTopAppBar:
                    id: idBottomSheetMenuTitle
                    name: "idBottomSheetMenuTitle"
                    title: app.messages[app.current_language]["BottomSheetMenuTitle"]  # "Bottom sheet"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarBottomSheet
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                BoxLayout:
                    orientation: 'vertical'
                    padding: '50sp'
                    spacing: '50sp'

                    MDLabel:                

                    MDRaisedButton:
                        text: "Open list bottom sheet"
                        opposite_colors: True
                        size_hint: None, None
                        size: 4 * dp(48), dp(48)
                        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
                        on_release: app.show_example_bottom_sheet()

                    MDRaisedButton:
                        text: "Open grid bottom sheet"
                        opposite_colors: True
                        size_hint: None, None
                        size: 4 * dp(48), dp(48)
                        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
                        on_release: app.show_example_grid_bottom_sheet()

                    MDLabel:    

            Screen:
                name: 'bottomnavigation'
                id: bottomnavigation
                MDTopAppBar:
                    id: idBottomNavigationMenuTitle
                    name: "idBottomNavigationMenuTitle" 
                    title: app.messages[app.current_language]["BottomNavigationMenuTitle"] # "Bottom Navigation"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarBottomNavigation
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                BoxLayout:
                    orientation: 'vertical'
                    padding: '50sp'
                    spacing: '50sp'

                    MDLabel:

                    MDBottomNavigation:
                        id: bottom_navigation_demo
                        MDBottomNavigationItem:
                            name: 'octagon'
                            text: "Warning"
                            icon: "alert-octagon"
                            MDLabel:
                                font_style: 'Body1'
                                theme_text_color: 'Primary'
                                text: "Warning!"
                                halign: 'center'
                        MDBottomNavigationItem:
                            name: 'banking'
                            text: "Bank"
                            icon: 'bank'
                            BoxLayout:
                                orientation: 'vertical'
                                size_hint_y: None
                                padding: dp(8)
                                spacing: 5
                                MDTextField:
                                    hint_text: "You can enter any bank name here"
                                    helper_text: "Hello :)"
                                    helper_text_mode: "on_focus"
                                    on_text_validate: app.validateInput(self)
                                    on_double_tap : app.twiceTap(self) 
                                    on_triple_tap : app.tripleTap(self) 

                        MDBottomNavigationItem:
                            name: 'bottom_navigation_desktop_1'
                            text: "Hello"
                            icon: 'alert'
                            id: bottom_navigation_desktop_1
                            BoxLayout:
                                orientation: 'vertical'
                                size_hint_y: None
                                padding: dp(8)
                                spacing: 5
                                MDTextField:
                                    hint_text: "Hello again"
                                    on_text_validate: app.validateInput(self)
                                    on_quad_touch : app.fourTap(self)
                        MDBottomNavigationItem:
                            name: 'bottom_navigation_desktop_2'
                            text: "Food"
                            icon: 'food'
                            id: bottom_navigation_desktop_2
                            MDLabel:
                                font_style: 'Body1'
                                theme_text_color: 'Primary'
                                text: "Cheese!"
                                halign: 'center'

            Screen:
                name: 'cards'
                id: cards

                MDTopAppBar:
                    id: idCardsMenuTitle
                    name: "idCardsMenuTitle"
                    title: app.messages[app.current_language]["CardsMenuTitle"] # "Cards"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarCards
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]


                BoxLayout:
                    orientation: 'vertical'
                    padding: '15sp'
                    spacing: '15sp'
                    size_hint_y: 0.9

                    MDLabel:
                        size_hint_y: 0.1

                    BoxLayout:
                        id: boxdatetime
                        size_hint_y: 0.1
                        padding: '5sp'
                        spacing: '30sp'

                        CardScreenLabel:
                            id: currentdate
                            text: app.getCurrentDate()

                        CardScreenLabel:  
                            id: currenttime 
                            text: app.getCurrentTime()


                    MDCard:
                        id: MDCard1 
                        size_hint_y: 0.4 
                        md_bg_color: "#e7e4c0"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
                        radius: 12, 46, 12, 46
                        elevation: 4
                        shadow_softness: 6
                        shadow_offset: (2, -2)
                        color: 'Primary'
                        MDLabel:
                            halign: "center"
                            text: 'Shadow up and left'

                    MDCard:
                        id: MDCard2
                        size_hint_y: 0.4
                        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
                        md_bg_color: "#e7e4c0"
                        color: 'Secondary'
                        elevation: 4
                        shadow_softness: 6
                        shadow_offset: (-2, 2)

                        BoxLayout:
                            orientation:'vertical'
                            padding: dp(8)
                            MDLabel:
                                text: 'Title'
                                theme_text_color: 'Secondary'
                                font_style: "Caption"
                                size_hint_y: None
                                height: dp(36)
                            MDSeparator:
                                height: dp(1)
                            MDLabel:
                                text: 'Body. Shadow down and right'
                                font_style: "Body1"
                                theme_text_color: 'Primary'
                                halign: "center"

            Screen:
                name: 'dialog'
                id: dialog

                MDTopAppBar:
                    id: idDialogsMenuTitle
                    name: "idDialogsMenuTitle"
                    title: app.messages[app.current_language]["DialogsMenuTitle"] # "Dialogs"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarDialogs
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                BoxLayout:
                    orientation: 'vertical'
                    padding: '50sp'
                    spacing: '50sp'

                    MDLabel:

                    MDRaisedButton:
                        text: "Open dialog"
                        size_hint: None, None
                        size: 3 * dp(48), dp(48)
                        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
                        opposite_colors: True
                        on_release: 
                            app.show_example_dialog()
                    MDRaisedButton:
                        text: "Open lengthy dialog"
                        size_hint: None, None
                        size: 3 * dp(48), dp(48)
                        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
                        opposite_colors: True
                        on_release: 
                            app.show_example_long_dialog()

                    MDRaisedButton:
                        text: "Open dialog with input"
                        size_hint: None, None
                        size: 5 * dp(48), dp(48)
                        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
                        opposite_colors: True
                        on_release: 
                            app.show_example_input_dialog()
                    MDLabel:

            Screen:
                name: 'grid'
                id: grid
                MDTopAppBar:
                    id: idGridMenuTitle
                    name: "idGridMenuTitle"
                    title: app.messages[app.current_language]["GridMenuTitle"] # "Grid. You can click on any picture"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarGrid
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                BoxLayout:
                    orientation: 'vertical'
                    padding: '20sp'
                    spacing: '10sp'
                    pos_hint: {"top": 0.88}
                    size_hint_y: 0.86 

                    ScrollView:
                        do_scroll_x: False
                        GridLayout:
                            cols: 2
                            row_default_height: (self.width - self.cols*self.spacing[0])/self.cols
                            row_force_default: True
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(4), dp(4)
                            spacing: dp(4)
                            MDSmartTileForGrid:
                                mipmap: True
                                source: 'https://images.unsplash.com/photo-1683057479776-d57c5f7123a2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80'
                                text: "Rose"
                                on_release:
                                    app.pressPicture(self)
                                OneLineListItem:
                                    font_style: 'Caption'
                                    text: "[color=#ffffff][b]I love roses[/b][/color]"
                                    pos_hint: {"center_y": .5}
                                    _no_ripple_effect: True    
                                MDIconButton:
                                    icon: "heart-outline"
                                    theme_icon_color: "Custom"
                                    icon_color: 1, 0, 0, 1
                                    pos_hint: {"center_y": .5}
                                    on_release: self.icon = "heart" if self.icon == "heart-outline" else "heart-outline"    

                            MDSmartTileForGrid:
                                mipmap: True
                                source: 'https://images.unsplash.com/photo-1683533949121-272be1c73171?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
                                text: "Bratislava"
                                on_release:
                                    app.pressPicture(self)

                            MDSmartTileForGrid:
                                mipmap: True
                                source: 'https://images.unsplash.com/photo-1683055742865-ed0aff8827fc?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
                                text: "Pskov"
                                on_release:
                                    app.pressPicture(self)

                            MDSmartTileForGrid:
                                mipmap: True
                                source: 'https://images.unsplash.com/photo-1683055741535-731f0b3eba8d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
                                text: "Spring"
                                on_release:
                                    app.pressPicture(self)

                            MDSmartTileForGrid:
                                mipmap: True
                                source: 'https://images.unsplash.com/photo-1657544919231-00830d544b9a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
                                text: "Cheetah"
                                on_release:
                                    app.pressPicture(self)

                            MDSmartTileForGrid:
                                mipmap: True
                                source: 'https://images.unsplash.com/photo-1657543811773-061dda5bb8ee?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80'
                                text: "Vienna"
                                on_release:
                                    app.pressPicture(self)

                            MDSmartTileForGrid:
                                mipmap: True
                                source: 'https://images.unsplash.com/photo-1657541115394-ca1c6ee58fbf?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
                                text: "Riga"
                                on_release:
                                    app.pressPicture(self)

                            MDSmartTileForGrid:
                                mipmap: True
                                source: 'https://images.unsplash.com/photo-1657004681542-ac1cd715b760?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
                                text: "Argun"
                                on_release:
                                    app.pressPicture(self)

                            MDSmartTileForGrid:
                                mipmap: True
                                source: 'https://images.unsplash.com/photo-1657004681284-4dd4bcc58ffd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80'
                                text: "Essentuki"
                                on_release:
                                    app.pressPicture(self)

                            MDSmartTileForGrid:
                                mipmap: True
                                source: 'https://images.unsplash.com/photo-1654192615588-daf256bdfcd4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
                                text: "Winter"
                                on_release:
                                    app.pressPicture(self)

                            MDSmartTileForGrid:
                                mipmap: True
                                source: 'https://images.unsplash.com/photo-1657004681330-9b9846ebeb1c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80'
                                text: "Snail"
                                on_release:
                                    app.pressPicture(self)

            Screen:
                name: 'labels'
                id: labels
                MDTopAppBar:
                    id: idLabelsMenuTitle
                    name: "idLabelsMenuTitle"
                    title: app.messages[app.current_language]["LabelsMenuTitle"] # "Labels. Scroll down to view all labels"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarLabels
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                BoxLayout:
                    orientation: 'vertical'
                    padding: '10sp'
                    spacing: '5sp'
                    pos_hint: {"top": 0.85}

                    ScrollView:
                        do_scroll_x: False
                        BoxLayout:
                            orientation: 'vertical'
                            size_hint_y: None
                            height: dp(1500)
                            padding: '10sp'
                            spacing: '5sp'
                            FloatLayout:
                                size_hint: 1, 0.1
                                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                                MDIcon:
                                    pos_hint: {"center_x": .2, "center_y": .5}
                                    icon: "gmail"
                                MDIcon:
                                    pos_hint: {"center_x": .8, "center_y": .5}
                                    icon: "gmail"
                                    badge_icon: "numeric-10"

                            BoxLayout:
                                adaptive_height: True
                                size_hint_y: 0.1
                                MDLabel:
                                    font_style: 'Body1'
                                    theme_text_color: 'Primary'  
                                    text: "Body1 label"
                                    halign: 'center'
                                MDLabel:
                                    font_style: 'Body2'
                                    theme_text_color: 'Primary'
                                    text: "Body2 label"
                                    halign: 'center'
                            BoxLayout:
                                size_hint_y: 0.1
                                MDLabel:
                                    font_style: 'Caption'
                                    theme_text_color: 'Primary'
                                    text: "Caption label"
                                    halign: 'center'
                                MDLabel:
                                    font_style: 'Subtitle1'
                                    theme_text_color: 'Primary'
                                    text: "Subtitle1 label"
                                    halign: 'center'
                                MDLabel:
                                    font_style: 'Subtitle2'
                                    theme_text_color: 'Primary' 
                                    text: "Subtitle2 label"
                                    halign: 'center'

                            BoxLayout:
                                orientation: 'vertical'
                                size_hint_y: 0.6
                                MDLabel:
                                    font_style: 'H1'
                                    theme_text_color: 'Primary'
                                    text: "H1"
                                    halign: 'center'
                                MDLabel:
                                    font_style: 'H2'
                                    theme_text_color: 'Primary'
                                    text: "H2"
                                    halign: 'center'
                                MDLabel:
                                    font_style: 'H3'
                                    theme_text_color: 'Primary'
                                    text: "H3"
                                    halign: 'center'
                                MDLabel:
                                    font_style: 'H4'
                                    theme_text_color: 'Primary'
                                    text: "H4"
                                    halign: 'center'
                                MDLabel:
                                    font_style: 'H5'
                                    theme_text_color: 'Primary'
                                    text: "H5"
                                    halign: 'center'
                                MDLabel:
                                    font_style: 'H6'
                                    theme_text_color: 'Primary'
                                    text: "H6"
                                    halign: 'center'
                            BoxLayout:
                                size_hint_y: 0.1
                                MDLabel:
                                    font_style: 'Body1'
                                    theme_text_color: 'Primary'
                                    text: "Primary color"
                                    halign: 'center'
                                MDLabel:
                                    font_style: 'Body1'
                                    theme_text_color: 'Secondary'
                                    text: "Secondary color"
                                    halign: 'center'
                            BoxLayout:
                                size_hint_y: 0.1
                                MDLabel:
                                    font_style: 'Body1'
                                    theme_text_color: 'Hint'
                                    text: "Hint color"
                                    halign: 'center'
                                MDLabel:
                                    font_style: 'Body1'
                                    theme_text_color: 'Error'
                                    text: "Error color"
                                    halign: 'center'
                            MDLabel:
                                size_hint_y: 0.1
                                font_style: 'H6'
                                theme_text_color: 'Custom'
                                text_color: (1,0,1,1)
                                text: "Custom"
                                halign: 'center'

                            MDLabel:
                                size_hint_y: 0.1
                                font_style: 'H6'
                                theme_text_color: "ContrastParentBackground"
                                text: "ContrastParentBackground"
                                halign: 'center'

                            MDLabel:
                                size_hint_y: 0.1    

            Screen:
                name: 'menu'
                id: menu
                MDTopAppBar:
                    id: idMenuMenuTitle
                    name: "idMenuMenuTitle"
                    title: app.messages[app.current_language]["MenuMenuTitle"] # "Menu"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarMenu
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                BoxLayout:
                    orientation: 'vertical'
                    padding: '20sp'
                    spacing: '20sp'
                    MDRaisedButton:
                        name: "buttonMenuOpen1"
                        size_hint: None, None
                        pos_hint_x: 0.5
                        size: 3 * dp(48), dp(48)
                        text: 'Open menu 1'
                        opposite_colors: True
                        on_release:
                            app.menu_open(self) 
                    MDRaisedButton:
                        name: "buttonMenuOpen2"
                        size_hint: None, None
                        pos_hint_x: 0.5
                        size: 3 * dp(48), dp(48)
                        text: 'Open menu 2'
                        opposite_colors: True
                        on_release:
                            app.menu_open(self) 
                    MDRaisedButton:
                        name: "buttonMenuOpen3"                    
                        size_hint: None, None
                        pos_hint_x: 0.5
                        size: 3 * dp(48), dp(48)
                        text: 'Open menu 3'
                        opposite_colors: True
                        on_release:
                            app.menu_open(self) 
                    MDRaisedButton:
                        name: "buttonMenuOpen4"                    
                        size_hint: None, None
                        pos_hint_x: 0.5
                        size: 3 * dp(48), dp(48)
                        text: 'Open menu 4'
                        opposite_colors: True
                        on_release:
                            app.menu_open(self) 
                    MDRaisedButton:
                        name: "buttonMenuOpen5"                    
                        size_hint: None, None
                        pos_hint_x: 0.5
                        size: 3 * dp(48), dp(48)
                        text: 'Open menu 5'
                        opposite_colors: True
                        on_release:
                            app.menu_open(self) 

            Screen:
                name: 'list'
                id: list
                MDTopAppBar:
                    id: idListMenuTitle
                    name: "idListMenuTitle"
                    title: app.messages[app.current_language]["ListMenuTitle"] # "List. Click any item of the list"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarList
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                BoxLayout:
                    orientation: 'vertical'
                    padding: '50sp'
                    spacing: '10sp'

                    MDLabel:
                        size_hint_y: 0.1

                    ScrollView:
                        do_scroll_x: False
                        MDList:
                            id: ml
                            OneLineListItem:
                                text: "One-line item"
                                on_release:
                                    app.pressListItem(self)

                            TwoLineListItem:
                                text: "Two-line item"
                                secondary_text: "Secondary text here"
                                on_release:
                                    app.pressListItem(self)

                            ThreeLineListItem:
                                text: "Three-line item"
                                secondary_text: "This is a multi-line label where you can fit more text than usual"
                                on_release:
                                    app.pressListItem(self)

                            OneLineAvatarListItem:
                                text: "Single-line item with avatar"
                                on_release:
                                    app.pressListItem(self)
                                AvatarSampleWidget:
                                    source: './assets/listSign.png'                                

                            TwoLineAvatarListItem:
                                type: "two-line"
                                text: "Two-line item..."
                                secondary_text: "with avatar"
                                on_release:
                                    app.pressListItem(self)
                                AvatarSampleWidget:
                                    source: './assets/listSign.png'                                

                            ThreeLineAvatarListItem:
                                type: "three-line"
                                text: "Three-line item..."
                                secondary_text: "...with avatar..." + '\\n' + "and third line!"
                                on_release:
                                    app.pressListItem(self)
                                AvatarSampleWidget:
                                    source: './assets/listSign.png'                                

                            OneLineIconListItem:
                                text: "Single-line item with left icon"
                                on_release:
                                    app.pressListItem(self)
                                IconLeftSampleWidget:
                                    id: li_icon_1
                                    icon: 'star-circle'

                            TwoLineIconListItem:
                                text: "Two-line item..."
                                secondary_text: "...with left icon"
                                on_release:
                                    app.pressListItem(self)
                                IconLeftSampleWidget:
                                    id: li_icon_2
                                    icon: 'comment-text'

                            ThreeLineIconListItem:
                                text: "Three-line item..."
                                secondary_text: "...with left icon..." + '\\n' + "and third line!"
                                on_release:
                                    app.pressListItem(self)
                                IconLeftSampleWidget:
                                    id: li_icon_3
                                    icon: 'sd'

                            OneLineAvatarIconListItem:
                                text: "Single-line + avatar&icon"
                                on_release:
                                    app.pressListItem(self)
                                AvatarSampleWidget:
                                    source: './assets/check_box_48.png'
                                IconRightSampleWidget:
                                    id: checkboxListItem

                            TwoLineAvatarIconListItem:
                                text: "Two-line item..."
                                secondary_text: "...with avatar&icon"
                                on_release:
                                    app.pressListItem(self)
                                AvatarSampleWidget:
                                    source: './assets/check_box_48.png'
                                IconRightSampleWidget:
                                    id: checkboxListItem

                            ThreeLineAvatarIconListItem:
                                text: "Three-line item..."
                                secondary_text: "...with avatar&icon..." + '\\n' + "and third line!"
                                on_release:
                                    app.pressListItem(self)
                                AvatarSampleWidget:
                                    source: './assets/check_box_48.png'
                                    size: self.texture_size

                                IconRightSampleWidget:
                                    id: checkboxListItem

            Screen:
                name: 'progress'
                id: progress
                MDTopAppBar:
                    id: idProgressMenuTitle
                    name: "idProgressMenuTitle"
                    title: app.messages[app.current_language]["ProgressMenuTitle"] # "Progress"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarProgress
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                MDLabel:
                    pos_hint_y: 0.2    

                FloatLayout:
                    pos_hint_y: 0.8
                    MDCheckbox:
                        id:            chkbox
                        elevation: 4
                        size_hint:    None, None
                        size:        dp(48), dp(48)
                        pos_hint:    {'center_x': 0.5, 'center_y': 0.5}
                        active: True
                    MDSpinner:
                        id: spinner
                        size_hint: None, None
                        size: dp(46), dp(46)
                        elevation: 4
                        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
                        active: True if chkbox.active else False


            Screen:
                name: 'progressbars'
                id: progressbars
                MDTopAppBar:
                    id: idProgressBarsAndSliderMenuTitle
                    name: "idProgressBarsAndSliderMenuTitle"
                    title: app.messages[app.current_language]["ProgressBarsAndSliderMenuTitle"] # "Progress Bars And Slider"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarProgressBar
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                BoxLayout:
                    orientation:'vertical'
                    padding: '8dp'

                    MDLabel:
                        size_hint_y: 0.3

                    MDSlider:
                        id:progress_slider
                        min:0
                        max:100
                        value: 40

                    MDProgressBar:
                        value: progress_slider.value
                    MDProgressBar:
                        reversed: True
                        value: progress_slider.value

                    BoxLayout:
                        MDProgressBar:
                            orientation:"vertical"
                            reversed: True
                            value: progress_slider.value

                        MDProgressBar:
                            orientation:"vertical"
                            value: progress_slider.value

            Screen:
                name: 'selectioncontrols'
                id: selectioncontrols
                MDTopAppBar:
                    id: idSelectionControlsMenuTitle
                    name: "idSelectionControlsMenuTitle"
                    title: app.messages[app.current_language]["SelectionControlsMenuTitle"] # "Selection Controls"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarSelectionControls
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                FloatLayout:
                    MDCheckbox:
                        id:            grp_chkbox_1
                        name:          "grp_chkbox_1"
                        group:        'test'
                        size_hint:    None, None
                        size:        dp(48), dp(48)
                        pos_hint:    {'center_x': 0.2, 'center_y': 0.5}
                        on_release:
                            app.pressCheckbox(self)
                    MDCheckbox:
                        id:            grp_chkbox_2
                        name:         "grp_chkbox_2" 
                        group:        'test'
                        size_hint:    None, None
                        size:        dp(48), dp(48)
                        pos_hint:    {'center_x': 0.4, 'center_y': 0.5}
                        on_release:
                            app.pressCheckbox(self)

                    MDSwitch:
                        id: MDSwitchDemo
                        name: "MDSwitchDemo" 
                        size_hint:    None, None
                        size:        dp(36), dp(48)
                        pos_hint:    {'center_x': 0.75, 'center_y': 0.5}
                        _active:        False
                        on_active:
                            app.pressSwitch(self)
                    MDLabel:
                        text: "One"
                        pos_hint:    {'x': 0.15, 'center_y': 0.6}    
                    MDLabel:
                        text: "Two"
                        pos_hint:    {'x': 0.35, 'center_y': 0.6}    

                    MDLabel:
                        text: "Switch ON"  if MDSwitchDemo.active else "Switch OFF"
                        pos_hint:    {'x': 0.7, 'center_y': 0.6}

                    MDRaisedButton:
                        text: "Change Widget Style"
                        pos_hint:  {'center_x': 0.5, 'center_y': 0.3}
                        on_release:
                            app.changeWidgetStyle()

            Screen:
                name: 'snackbar'
                id: snackbar
                MDTopAppBar:
                    id: idSnackBarMenuTitle
                    name: "idSnackBarMenuTitle"  
                    title: app.messages[app.current_language]["SnackBarMenuTitle"] # "Snack Bar"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarSnackBar
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                FloatLayout:

                    MDRaisedButton:
                        text: "Create simple snackbar"
                        size_hint: None, None
                        size: 4 * dp(48), dp(48)
                        pos_hint: {'center_x': 0.5, 'center_y': 0.75}
                        opposite_colors: True
                        on_release: app.show_example_snackbar('simple')
                    MDRaisedButton:
                        text: "Create snackbar with a lot of text"
                        size_hint: None, None
                        size: 5 * dp(48), dp(48)
                        pos_hint: {'center_x': 0.5, 'center_y': 0.25}
                        opposite_colors: True
                        on_release: app.show_example_snackbar('verylong')

            Screen:
                id: textfields
                name: 'textfields'
                MDTopAppBar:
                    id: idInputTextMenuTitle
                    name: "idInputTextMenuTitle"  
                    title: app.messages[app.current_language]["InputTextMenuTitle"] # "Input text and press [Enter]"
                    elevation: 4
                    pos_hint: {"top": 1}
                    ## md_bg_color: "#e7e4c0"
                    id: MDTopAppBarTextFields
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                BoxLayout:
                    orientation: 'vertical'
                    padding: '5sp'
                    spacing: '5sp'

                    MDLabel:
                        size_hint_y: 0.15

                    ScrollView:
                        size_hint_y: 0.85
                        BoxLayout:
                            orientation: 'vertical'
                            size_hint_y: None
                            height: self.minimum_height
                            padding: dp(48)
                            spacing: 10
                            MDTextField:
                                hint_text: "No helper text"
                                on_text_validate: app.validateInput(self)
                            MDTextField:
                                hint_text: "Helper text on focus"
                                helper_text: "This will disappear when you click off"
                                helper_text_mode: "on_focus"
                                on_text_validate: app.validateInput(self)
                            MDTextField:
                                hint_text: "Persistent helper text"
                                helper_text: "Text is always here"
                                helper_text_mode: "persistent"
                                on_text_validate: app.validateInput(self)
                            MDTextField:
                                id: text_field_error
                                name: "text_field_error"
                                hint_text: "Helper text on error (Hit Enter with two characters here)"
                                helper_text: "Two is my least favorite number"
                                helper_text_mode: "on_error"
                                on_text_validate: app.validateInput(self)
                            MDTextField:
                                id: text_field_error_max_text_length10
                                name: "text_field_error_max_text_length10"
                                hint_text: "Max text length = 10"
                                max_text_length: 10
                                on_text_validate: app.validateInput(self)
                            MDTextField:
                                hint_text: "required = True"
                                required: True
                                helper_text_mode: "on_error"
                                on_text_validate: app.validateInput(self)
                            MDTextField:
                                multiline: True
                                hint_text: "Multi-line text"
                                helper_text: "Messages are also supported here"
                                helper_text_mode: "persistent"
                            MDTextField:
                                hint_text: "color_mode = \'accent\'"
                                color_mode: 'accent'
                                on_text_validate: app.validateInput(self)
                            MDTextField:
                                hint_text: "color_mode = \'custom\'"
                                color_mode: 'custom'
                                helper_text_mode: "on_focus"
                                helper_text: "Color is defined by \'line_color_focus\' property"
                                line_color_focus: self.theme_cls.opposite_bg_normal  # This is the color used by the textfield
                                on_text_validate: app.validateInput(self)
                            MDTextField:
                                hint_text: "disabled = True"
                                disabled: True
                            MDTextField:
                                id: MDTextFieldDateWithoutLimits
                                name: "MDTextFieldDateWithoutLimits"
                                hint_text: "Date dd/mm/yyyy without limits"
                                helper_text: "Enter a valid dd/mm/yyyy date"
                                validator: "date"
                                date_format: "dd/mm/yyyy"
                                on_text_validate: app.validateInputDate(self)
                            MDTextField:
                                id: MDTextFieldDateWithoutLimitsYear
                                name: 'MDTextFieldDateWithoutLimitsYear'
                                hint_text: "Date yyyy/mm/dd without limits"
                                helper_text: "Enter a valid yyyy/mm/dd date"
                                validator: "date"
                                date_format: "yyyy/mm/dd"
                                on_text_validate: app.validateInputDate(self)
                            MDTextField:
                                id:MDTextFieldDateInterval
                                name: 'MDTextFieldDateInterval'
                                hint_text: "Date dd/mm/yyyy in [01/01/1900, 01/01/2100] interval"
                                helper_text: "Enter a valid dd/mm/yyyy date"
                                validator: "date"
                                date_format: "dd/mm/yyyy"
                                date_interval: "01/01/1900", "01/01/2100"
                                on_text_validate: app.validateInputDate(self)
                            MDTextField:
                                id: MDTextFieldDateIntervalUpNone
                                name: 'MDTextFieldDateIntervalUpNone'
                                hint_text: "Date dd/mm/yyyy in [01/01/1900, None] interval"
                                helper_text: "Enter a valid dd/mm/yyyy date"
                                validator: "date"
                                date_format: "dd/mm/yyyy"
                                date_interval: "01/01/1900", None
                                on_text_validate: app.validateInputDate(self)
                            MDTextField:
                                id: MDTextFieldDateIntervalDownNone
                                name: 'MDTextFieldDateIntervalDownNone'
                                hint_text: "Date dd/mm/yyyy in [None, 01/01/2100] interval"
                                helper_text: "Enter a valid dd/mm/yyyy date"
                                validator: "date"
                                date_format: "dd/mm/yyyy"
                                date_interval: None, "01/01/2100"
                                on_text_validate: app.validateInputDate(self)

                            BoxLayout:
                                id: BoxLayoutPassword
                                size_hint_y: None
                                height: text_field_password.height    
                                MDTextField:
                                    id: text_field_password
                                    hint_text: "Input password and press [Enter], please"
                                    text: ""
                                    helper_text: 'It must consists of low & up leters, numbers & spec.chars'
#                                    helper_text: 'The password must consists of numbers,' + chr(13)+chr(10) + 'uppercase and lowercase letters' + chr(13)+chr(10) + 'and special characters'
                                    password: True
                                    required: True
                                    helper_text_mode: "on_error"
                                    icon_left: "key-variant"
                                    on_text_validate: app.validateInputPasswords(self)

                                MDIconButton:
                                    icon: "eye-off"
#                                    pos_hint: {"top": 1}
#                                    pos_hint_y: {"center_y": .5}
#                                    pos_hint_x: None
                                    pos: text_field_password.width - self.width + dp(8), 0
                                    theme_text_color: "Hint"
                                    on_release:
                                        self.icon = "eye" if self.icon == "eye-off" else "eye-off"
                                        text_field_password.password = False if text_field_password.password is True else True       

            Screen:
                name: 'theming'
                id: theming                
                MDTopAppBar:
                    id: idChangeColorMenuTitle
                    name: "idChangeColorMenuTitle" 
                    title: app.messages[app.current_language]["ChangeColorMenuTitle"] # "Change color"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarTheming
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                BoxLayout:
                    orientation: 'vertical'
                    padding: '20sp'
                    spacing: '20sp'
                    size_hint_y: 0.8

                    MDLabel:
                        size_hint_y: 0.2

                    MDRaisedButton:
                        id: color_button
                        size_hint_y: 0.3
                        # center_x: self.parent.center_x
                        text: 'Change color of Button'
                        opposite_colors: True
                        pos_hint: {'center_x': 0.5}
                        on_release: 
                            app.changeColor()

                    MDLabel:
                        text: "Current: " + app.theme_cls.theme_style + ", " + app.theme_cls.primary_palette
                        theme_text_color: 'Custom'
                        text_color: app.theme_cls.primary_color
                        size_hint_y: 0.3
                        pos_hint: {'center_x': 0.5}
                        halign: 'center'

                    MDRaisedButton:
                        id: color_button_app
                        size_hint_y: 0.3
                        # center_x: self.parent.center_x
                        opposite_colors: True
                        pos_hint: {'center_x': 0.5}
                        text: "Change color of App"
                        on_release: 
                            app.changeAppColor()

                    BackgroundLabel:
                        id: ChameleonLabel
                        text: "Chameleon label"
                        size_hint_y: 0.2
                        size_hint_x: 0.5
                        pos_hint: {'center_x': 0.5}
                        halign: 'center'


# In this Kivy file, it didn't work for me. I only did it in the app file 
#                     MDDropDownItem:
#                         id: dropdown_item
#                         text: "Change color of App"
#                         font_style: 'h5'
#                         pos_hint: {'center_x': 0.5}
#                         items: ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray'] 
#                         dropdown_bg: [0.7, 0.7, 0.7, 1]
#                         dropdown_max_height: 200
#                         current_item: app.theme_cls.primary_palette
#                         on_select:
#                             print(self.current_item) 
#                         on_release: 
#                             print("Press item")
#                             print(dir(self))
#                             print(self.items)

                    MDLabel:
                        size_hint_y: 0.15  

            Screen:
                name: 'toolbar'
                id: toolbar                
                MDTopAppBar:
                    id: idToolbarMenuTitle
                    title: app.messages[app.current_language]["ToolbarMenuTitle"] # "Toolbar. Click any icons"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarToolBar
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                BoxLayout:
                    orientation: 'vertical'
                    padding: '20sp'
                    spacing: '20sp'
                    size_hint_y: None

                    MDTopAppBar:
                        id: idSimpleToolbarTitle
                        name: "idSimpleToolbarTitle"
                        title: app.messages[app.current_language]["SimpleToolbarTitle"] # "Simple toolbar"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.75}
                        md_bg_color: get_color_from_hex(colors['Teal']['500'])
                        background_palette: 'Teal'
                        background_hue: '500'
                    MDTopAppBar:
                        id: idToolbarWithRightButtonsTitle
                        name: "idToolbarWithRightButtonsTitle"
                        title: app.messages[app.current_language]["ToolbarWithRightButtonsTitle"] # "Toolbar with right buttons"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                        md_bg_color: get_color_from_hex(colors['Amber']['700'])
                        background_palette: 'Amber'
                        background_hue: '700'
                        right_action_items: [['content-copy',  lambda x: app.pressTool(self,x)]]
                    MDTopAppBar:
                        id: idToolbarWithLeftAndRightButtonsTitle
                        name: "idToolbarWithLeftAndRightButtonsTitle"
                        title: app.messages[app.current_language]["ToolbarWithLeftAndRightButtonsTitle"] # "Toolbar with left and right buttons"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.25}
                        md_bg_color: get_color_from_hex(colors['DeepPurple']['A400'])
                        background_palette: 'DeepPurple'
                        background_hue: 'A400'
                        left_action_items: [['arrow-left', lambda x:  app.pressTool(self,x) ]]
                        right_action_items: [['lock',      lambda x:  app.pressTool(self,x)], \
                                             ['camera',    lambda x:  app.pressTool(self,x)], \
                                             ['play',      lambda x:  app.pressTool(self,x)]]

            Screen:
                name: 'tabs'
                id: tabs                
                MDTopAppBar:
                    title: "Tabs"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarTabs
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                BoxLayout:    
                    orientation: 'vertical'
                    padding: '20sp'
                    spacing: '20sp'
                    pos_hint: {"top": 0.86}
                    size_hint_y: 0.89

                    MDTabs:
                        id: tab_panel
                        tab_display_mode:'text'

                        on_tab_switch:
                            toast.toast(self.get_current_tab().text)

                        Tab:
                            id: music
                            name: 'music'
                            text: 'music'
                            icon: "playlist-play"
                            title: app.messages[app.current_language]["TabsMISICTitle"] # 'MISIC'
                            MDLabel:
                                font_style: 'Body1'
                                theme_text_color: 'Primary'
                                text: "Here is my music list :)"
                                halign: 'center'
                        Tab:
                            id: movies
                            name: 'movies'
                            icon: "movie"
                            text: 'movies'
                            title: app.messages[app.current_language]["TabsMOVIESTitle"] # 'MOVIES'

                            MDLabel:
                                font_style: 'Body1'
                                theme_text_color: 'Primary'
                                text: "Show movies here :)"
                                halign: 'center'

                    BoxLayout:
                        size_hint_y:None
                        height: '48dp'
                        padding: '12dp'
                        MDLabel:
                            font_style: 'Body1'
                            theme_text_color: 'Primary'
                            text: "Change title location"
                            size_hint_x:None
                            width: '256dp'
                        MDCheckbox:
                            id:  checkbox_tabs 
                            on_state: 
                                root.ids.tab_panel.title_icon_mode = "Lead" if self.state == "normal" else "Top" 



            Screen:
                name: 'expansionpanel'
                id: expansionpanel               
                MDTopAppBar:
                    id: idAccordionMenuTitle
                    name: "idAccordionMenuTitle"
                    title: app.messages[app.current_language]["AccordionMenuTitle"] #"Accordion. Click on the lines"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarExpansionPanel
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                MDBoxLayout:
                    orientation: "vertical"
                    pos_hint: {"top": 0.83}
                    size_hint_y: 0.86
                    MDScrollView:
                        MDGridLayout:
                            id: expansionpanel    
                            cols: 1
                            padding: '5sp'
                            spacing: '5sp'
                            adaptive_height: True



        # In this Kivy file, it didn't work for me. I only did it in the app file
        #                    MDExpansionPanel:
        # [MDExpansionPanelOneLine, MDExpansionPanelTwoLine, MDExpansionPanelThreeLine]  
        #                         adaptive_height: True
        #                         id: expansionpanel
        #                                           
        #                         MDExpansionPanelOneLine:
        #                             id: expansionpaneloneline
        #                             text:           "OneLine.Text"
        #                             
        #                         MDExpansionPanelTwoLine:
        #                             id: expansionpaneltwoline
        #                             text:           "TwoLine.Text"
        #                             secondary_text: "TwoLine.Secondary text"
        #                         
        #                         MDExpansionPanelThreeLine:
        #                             id: expansionpanelthreeline
        #                             text:           "ThreeLine.Text"
        #                             secondary_text: "ThreeLine.Secondary text"
        #                             tertiary_text:  "ThreeLine.Tertiary text"

            Screen:
                name: 'backdrop'
                id: backdrop               
                MDTopAppBar:
                    title: app.messages[app.current_language]["BackdropMenuTitle"] # "Backdrop"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarBackDrop
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint_y: 0.89
                    MDBackdrop:
                        id: backdrop
                        name: "backdrop"
                        left_action_items: [['menu', lambda x: self.open()]]
                        title: app.messages[app.current_language]["BackdropMenuTitle"]  # "Example Backdrop"
                        radius_left: "25dp"
                        radius_right: "0dp"
                        header_text: "Menu:"

                        MDBackdropBackLayer:
                            MyBackdropBackLayer:
                                id: backlayer

                        MDBackdropFrontLayer:
                            MyBackdropFrontLayer:
                                backdrop: backdrop    

            Screen:
                name: 'splash'
                id: splash
                MDTopAppBar:
                    id: idSplashMenuTitle
                    name: "idSplashMenuTitle"
                    title: app.messages[app.current_language]["SplashMenuTitle"] #  "KivyMD Demo"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarSplash
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                BoxLayout:
                    orientation: 'vertical'
                    padding: '50sp'
                    spacing: '50sp'

                    MDLabel:
                        size_hint: .8, .1                

                    Image:
                        id: imageLogo
                        size_hint: .8, .8
                        source: os.path.join(images_path, "logo", "kivymd-icon-512.png")
                        pos_hint: {"center_x": .5, "center_y": .6}
                    MDLabel:
                        font_style: 'Caption'
                        size_hint: .8, .1
                        theme_text_color: 'Custom'
                        text_color: self.theme_cls.primary_light if (self.theme_cls.theme_style == 'Dark') else app.theme_cls.primary_dark
                        text: "(C) Ryazanoff V.A."
                        halign: 'left'    


            Screen:
                name: 'banner'
                id: banner
                MDTopAppBar:
                    id: idBannerMenuTitle
                    name: "idBannerMenuTitle"
                    title: app.messages[app.current_language]["BannerMenuTitle"] # "Banner"
                    id: toolbar_top 
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarBanner
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                BoxLayout:
                    orientation: 'vertical'
                    padding: '5sp'
                    spacing: '5sp'
                    size_hint_y: 0.9

                    MDLabel:
                        size_hint_y: 0.5

                    BoxLayout:
                        size_hint_y: 0.5
                        orientation: 'vertical'
                        MDBanner:
                            id: banner
                            text: ["One-line example with no action. Click me"]
# The widget that is under the banner.
# It will be shifted down to the height of the banner.
                            over_widget: screen
# Original location                            
#                            vertical_pad: toolbar.height
                            vertical_pad:  Window.height / 2 + toolbar.height

                        MDTopAppBar:
                            id: toolbar
                            name: "toolbar"
                            title: app.messages[app.current_language]["BannerTitle"] # "Banner. Click on the line bellow"
                            elevation: 4
# Original location                            
#                            pos_hint: {'top': 1}
                            pos_hint: {'top': 0.5 }

                        MDBoxLayout:
                            id: screen
                            orientation: "vertical"
                            size_hint_y: None
                            height: Window.height / 2 - toolbar.height
# Original location                             
#                            height: Window.height - toolbar.height
                            OneLineListItem:
                                text: "Banner without actions"
                                on_release: banner.show()
                            Widget:

            Screen:
                name: 'datepicker'
                id: datepicker
                MDTopAppBar:
                    id: idDate&TimePickersMenuTitle
                    name: "idDate&TimePickersMenuTitle"
                    title: app.messages[app.current_language]["Date&TimePickersMenuTitle"] # "Date & Time Pickers"
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarDatePicker
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                BoxLayout:
                    orientation: 'vertical'
                    padding: '5sp'
                    spacing: '10sp'
                    size_hint_y: 0.9

                    MDLabel:
                        size_hint_y: 0.1

                    MDRaisedButton:
                        id: simpledatepicker
                        text: "Open date picker"
                        pos_hint: {'center_x': 0.5}
                        size_hint_y: 0.1
                        on_release:
                            app.openDatePicker(self)

                    MDRaisedButton:
                        id: setdatedatepicker
                        text: "Open date picker at 2000-01-01"
                        pos_hint: {'center_x': 0.5}
                        size_hint_y: 0.1
                        on_release:
                            app.openDatePicker(self)

                    MDRaisedButton:
                        id: setdaterangedatepicker
                        text: "Open date picker. Date range"
                        pos_hint: {'center_x': 0.5}
                        size_hint_y: 0.1
                        on_release:
                            app.openDatePicker(self)

                    MDRaisedButton:
                        id: selectyeardatepicker                    
                        text: "Open date picker. Select year"
                        pos_hint: {'center_x': 0.5}
                        size_hint_y: 0.1
                        on_release:
                            app.openDatePicker(self)

                    MDRaisedButton:
                        id: selectdaterangedatepicker                    
                        text: "Open date picker. Select a date range"
                        pos_hint: {'center_x': 0.5}
                        size_hint_y: 0.1
                        on_release:
                            app.openDatePicker(self)
                    MDLabel:
                        size_hint_y: 0.1

                    MDRaisedButton:
                        id: timepicker                    
                        text: "Open time picker"
                        pos_hint: {'center_x': 0.5}
                        size_hint_y: 0.1
                        on_release:
                            app.openTimePicker(self)


            Screen:
                name: 'carousel'
                id: carousel
                MDTopAppBar:
                    id: idCarouselMenuTitle
                    name: "idCarouselMenuTitle"
                    title: app.messages[app.current_language]["CarouselMenuTitle"] # "Carousel. Slide it, please "
                    elevation: 4
                    pos_hint: {"top": 1}
                    id: MDTopAppBarCarousel
                    specific_text_color: "#4a4939"
                    left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                BoxLayout:
                    pos_hint: {"top": 0.85}
                    orientation: 'vertical'  
                    size_hint_y: 0.82

                    MDLabel:
                        size_hint_y: 0.05
                    MDFloatLayout:
                        size_hint_y: 0.9

                        MDCarousel:
                            direction: 'right'

                            id: carousel
                            pos_hint: {'center_x': 0.5, 'center_y':0.5}
                            AsyncImage:
                                source: 'https://images.unsplash.com/photo-1658217154685-1ce4c4c861ec?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80'
                            AsyncImage:
                                source: 'https://images.unsplash.com/photo-1658214470482-6985dd444e7a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80'
                            AsyncImage:
                                source: 'https://images.unsplash.com/photo-1658214772258-6630503e5c11?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80'
                            AsyncImage:
                                source: 'https://images.unsplash.com/photo-1658217514856-a0f44fb6da39?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80'


                        MDFloatingActionButton:
                            id: MDFloatingActionButtonMenuRight
                            icon:               'menu-right'
                            opposite_colors:    True
                            elevation_normal:    8
                            pos_hint: {'center_x': 0.92, 'center_y':0.5}
                            disabled: carousel.index == (len(carousel.slides) - 1)
                            on_release:
                                app.shiftCarouselRight()


                        MDFloatingActionButton:
                            id: MDFloatingActionButtonMenuLeft
                            icon:               'menu-left'
                            opposite_colors:    True
                            elevation_normal:    8
                            pos_hint: {'center_x': 0.08, 'center_y':0.5}
                            disabled: carousel.index == 0
                            on_release:
                                app.shiftCarouselLeft()

                    MDLabel:
                        size_hint_y: 0.05             

        MDNavigationDrawer:
            id: nav_drawer
            name: "nav_drawer"
            title: app.messages[app.current_language]["NavigationDrawerMenuTitle"]  # "Navigation Drawer"
            radius: (0, 16, 16, 0)
            close_on_click: True
            enable_swiping: True

            MDNavigationDrawerMenu:
                id: NavigationDrawerMenu

                MDNavigationDrawerHeader:
                    id: idKitchenSink
                    title: app.messages[app.current_language]["MainTitle"] # "Kitchen Sink"
                    title_color: app.theme_cls.primary_color
                    text: app.messages[app.current_language]["SubTitle"]   # "Demo Kivy MD"
                    text_color: app.theme_cls.accent_color
                    spacing: "4dp"
                    padding: "12dp", 0, 0, "56dp"

                DrawerClickableItemColor:
                    id: idChangeAnimation
                    icon: "animation"
                    text_right_color: app.theme_cls.primary_color 
                    focus_color: "#e7e4c0"
                    text_color: "#4a4939"
                    icon_color: "#4a4939"
                    ripple_color: "#c5bdd2"
                    selected_color: app.theme_cls.accent_color
                    text: app.messages[app.current_language]["ChangeAnimation"] # "Change Animation"
                    on_release:
                        app.changeAnimation()
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idChangeOrientation
                    icon: "vector-arrange-above"
                    text_right_color: "#4a4939"
                    text: app.messages[app.current_language]["ChangeOrientation"]  # "Change Orientation"
                    on_release:
                        app.changeOrientation()
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idChangeTheme
                    icon: "theme-light-dark"
                    text_right_color: "#4a4939"
                    text: app.messages[app.current_language]["ChangeTheme"] # "Change theme"
                    on_release:
                        app.changeTheme()
                        root.ids.nav_drawer.set_state("close")

                # DrawerClickableItemColor:
                #     id: idChangeLanguage
                #     icon: "translate"
                #     text_right_color: "#4a4939"
                #     text: app.messages[app.current_language]["ChangeLanguage"] # "Change language"
                #     on_release:
                #         app.changeLanguage()
                #         root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idChangeLanguageNormal
                    icon: "translate"
                    text_right_color: "#4a4939"
                    text: app.messages[app.current_language]["ChangeLanguageNormal"] # "Change language"
                    on_release:
                        app.changeTitleAndText()
                        root.ids.nav_drawer.set_state("close")

                MDNavigationDrawerDivider:

                DrawerLabelItem:
                    id: idDemoSimpleWidgets
                    text: app.messages[app.current_language]["DemoSimpleWidgets"]  # "Demo simple widgets"

                DrawerClickableItemColor:
                    id : idCards
                    icon: 'button-pointer'
                    text: app.messages[app.current_language]["Cards"] # "Cards"
                    on_release:
                        root.ids.manager.current = "cards"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idGrid
                    icon: 'button-pointer'
                    text: app.messages[app.current_language]["Grid"] # "Grid"
                    on_release:
                        root.ids.manager.current = "grid"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idProgress 
                    icon: 'button-pointer'
                    text: app.messages[app.current_language]["Progress"] # "Progress"
                    on_release:
                        root.ids.manager.current = "progress"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idProgressBars&Slider
                    icon: 'button-pointer'
                    text: app.messages[app.current_language]["ProgressBars&Slider"] # "Progress Bars  & Slider"
                    on_release:
                        root.ids.manager.current = "progressbars"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idSelectionControls
                    icon: 'button-pointer'
                    text: app.messages[app.current_language]["SelectionControls"] # "Selection Controls"
                    on_release:
                        root.ids.manager.current = "selectioncontrols"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idSomeButtons
                    icon: 'button-pointer'
                    text: app.messages[app.current_language]["SomeButtons"] #"Some buttons"
                    on_release:
                        root.ids.manager.current = "buttons"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idSomeLabels
                    icon: 'button-pointer'
                    text:  app.messages[app.current_language]["SomeLabels"] # "Some Labels"
                    on_release:
                        root.ids.manager.current = "labels" 
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idSomeTextFields
                    icon: 'button-pointer'
                    text: app.messages[app.current_language]["SomeTextFields"] # "Some Text Fields"
                    on_release:
                        root.ids.manager.current = "textfields"
                        root.ids.nav_drawer.set_state("close")

                MDNavigationDrawerDivider:

                DrawerLabelItem:
                # MDNavigationDrawerLabel:
                    id: idDemoComboWidgets
                    text: app.messages[app.current_language]["DemoComboWidgets"] # "Demo combo widgets"

                DrawerClickableItemColor:
                    id: idBottomSheet
                    icon: 'gesture-tap-button'
                    text: app.messages[app.current_language]["BottomSheet"] # "Bottom sheet"
                    on_release:
                        root.ids.manager.current = "bottomsheet"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idBottomNavigation
                    icon: 'gesture-tap-button'
                    text: app.messages[app.current_language]["BottomNavigation"] # "Bottom Navigation"
                    on_release:
                        root.ids.manager.current = "bottomnavigation"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idDialog
                    icon: 'gesture-tap-button'
                    text: app.messages[app.current_language]["Dialog"] # "Dialog"
                    on_release:
                        root.ids.manager.current = "dialog"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idList
                    icon: 'gesture-tap-button'
                    text: app.messages[app.current_language]["List"] #  "List"
                    on_release:
                        root.ids.manager.current = "list"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idMenu
                    icon: 'gesture-tap-button'
                    text: app.messages[app.current_language]["Menu"] # "Menu"
                    on_release:
                        root.ids.manager.current = "menu"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idSnackBar
                    icon: 'gesture-tap-button'
                    text: app.messages[app.current_language]["SnackBar"] # "Snack Bar"
                    on_release:
                        root.ids.manager.current = "snackbar"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idChangeColors
                    icon: 'gesture-tap-button'
                    text: app.messages[app.current_language]["ChangeColors"] # "Change Colors"
                    on_release:
                        root.ids.manager.current = "theming"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idToolbar
                    icon: 'gesture-tap-button'
                    text: app.messages[app.current_language]["Toolbar"] # "Toolbar"
                    on_release:
                        root.ids.manager.current = "toolbar"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idTabs 
                    icon: 'gesture-tap-button'
                    text: app.messages[app.current_language]["Tabs"] #  "Tabs"
                    on_release:
                        root.ids.manager.current = "tabs"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idExpansionPanel
                    icon: 'gesture-tap-button'
                    text: app.messages[app.current_language]["ExpansionPanel"] # "Expansion panel"
                    on_release:
                        root.ids.manager.current = "expansionpanel"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idBackdrop
                    icon: 'gesture-tap-button'
                    text: app.messages[app.current_language]["Backdrop"] # "Backdrop"
                    on_release:
                        root.ids.manager.current = "backdrop"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idBanner
                    icon: 'gesture-tap-button'
                    text: app.messages[app.current_language]["Banner"] # "Banner"
                    on_release:
                        root.ids.manager.current = "banner"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idDateAndTimePicker
                    icon: 'gesture-tap-button'
                    text: app.messages[app.current_language]["DateAndTimePicker"] # "Date and Time Picker"
                    on_release:
                        root.ids.manager.current = "datepicker"
                        root.ids.nav_drawer.set_state("close")

                DrawerClickableItemColor:
                    id: idCarousel
                    icon: 'gesture-tap-button'
                    text: app.messages[app.current_language]["Carousel"] # "Carousel"
                    on_release:
                        root.ids.manager.current = "carousel"
                        root.ids.nav_drawer.set_state("close")

                MDNavigationDrawerDivider:

                DrawerClickableItemColor:
                    id: idQuit
                    icon: 'exit-run'
                    text: app.messages[app.current_language]["Quit"] # "Quit"
                    on_release:
                        root.ids.nav_drawer.set_state("close")
                        app.quit()
"""


# The following empty classes are required to link to the definitions in the Kivy files
class Tab(FloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    pass


class ContentPanel(MDBoxLayout):
    '''Custom content.'''
    pass


class Content(BoxLayout):
    pass


class MyPopup(Popup):
    pass


class AvatarSampleWidget(ILeftBody, Image):
    pass


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class IconRightSampleWidget(IRightBodyTouch, MDCheckbox):
    pass


def windows_on_keyboard_handler(instance, key, scancode, codepoint, modifiers):
    """ Fixed keyboard handler for changing application orientation and other hotkey functions """
    # other keyboard modifiers must be removed
    CAPSLOCK = 'capslock'
    NUMLOCK = 'numlock'

    mod = modifiers.copy()
    if (CAPSLOCK in mod):
        mod.remove(CAPSLOCK)
    if (NUMLOCK in mod):
        mod.remove(NUMLOCK)

    app = MDApp.get_running_app()

    if key == 293 and mod == []:  # F12
        instance.screenshot()
    elif key == 292 and mod == []:  # F11
        instance.rotation += 90
    elif key == 292 and mod == ['shift']:  # Shift + F11
        # the platform must be in lower case and only the first characters must be used
        plat = platform()
        plat = plat[0:3].lower()
        if plat in ('win', 'lin', 'mac'):
            instance.rotation = 0
            w, h = instance.size
            w, h = h, w
            instance.size = (w, h)
    elif key == 289 and mod == ['shift']:  # Shift + F8
        app.changeTheme()
        app.root.ids.manager.current = "splash"
    elif key == 288 and mod == ['shift']:  # Shift + F7
        app.changeLanguage()
        app.root.ids.manager.current = "splash"
    elif key == 287 and mod == ['shift']:  # Shift + F6
        app.changeAnimation()
    elif key == 286 and mod == ['shift']:  # Shift + F5
        app.changeAppColor()


# This is the main class for the application
class DemoKivyMD(MDApp):
    color_items = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green',
                   'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
    current_language = 'English'
    languages = ['English', 'Русский']

    keys = {"idKitchenSink": {"title": "MainTitle", "text": "SubTitle"},
            "idChangeAnimation": {"text": "ChangeAnimation"},
            "idChangeOrientation": {"text": "ChangeOrientation"},
            "idChangeTheme": {"text": "ChangeTheme"},
            "idChangeLanguage": {"text": "ChangeLanguage"},
            "idChangeLanguageNormal": {"text": "ChangeLanguageNormal"},
            "idDemoSimpleWidgets": {"text": "DemoSimpleWidgets"},
            "idCards": {"text": "Cards"},
            "idGrid": {"text": "Grid"},
            "idProgress": {"text": "Progress"},
            "idProgressBars&Slider": {"text": "ProgressBars&Slider"},
            "idSelectionControls": {"text": "SelectionControls"},
            "idSomeButtons": {"text": "SomeButtons"},
            "idSomeLabels": {"text": "SomeLabels"},
            "idSomeTextFields": {"text": "SomeTextFields"},
            "idDemoComboWidgets": {"text": "DemoComboWidgets"},
            "idBottomSheet": {"text": "BottomSheet"},
            "idBottomNavigation": {"text": "BottomNavigation"},
            "idDialog": {"text": "Dialog"},
            "idList": {"text": "List"},
            "idMenu": {"text": "Menu"},
            "idSnackBar": {"text": "SnackBar"},
            "idChangeColors": {"text": "ChangeColors"},
            "idToolbar": {"text": "Toolbar"},
            "idTabs": {"text": "Tabs"},
            "idExpansionPanel": {"text": "ExpansionPanel"},
            "idBackdrop": {"text": "Backdrop"},
            "idBanner": {"text": "Banner"},
            "idDateAndTimePicker": {"text": "DateAndTimePicker"},
            "idCarousel": {"text": "Carousel"},
            "idQuit": {"text": "Quit"},
            "idMyPopup": {"title": "PopupExit"},
            "idMainMenuTitle": {"title": "MainMenuTitle"},
            "idButtonsMenuTitle": {"title": "ButtonsMenuTitle"},
            "idBottomSheetMenuTitle": {"title": "BottomSheetMenuTitle"},
            "idBottomNavigationMenuTitle": {"title": "BottomNavigationMenuTitle"},
            "idCardsMenuTitle": {"title": "CardsMenuTitle"},
            "idDialogsMenuTitle": {"title": "DialogsMenuTitle"},
            "idGridMenuTitle": {"title": "GridMenuTitle"},
            "idLabelsMenuTitle": {"title": "LabelsMenuTitle"},
            "idMenuMenuTitle": {"title": "MenuMenuTitle"},
            "idListMenuTitle": {"title": "ListMenuTitle"},
            "idProgressMenuTitle": {"title": "ProgressMenuTitle"},
            "idProgressBarsAndSliderMenuTitle": {"title": "ProgressBarsAndSliderMenuTitle"},
            "idSelectionControlsMenuTitle": {"title": "SelectionControlsMenuTitle"},
            "idSnackBarMenuTitle": {"title": "SnackBarMenuTitle"},
            "idInputTextMenuTitle": {"title": "InputTextMenuTitle"},
            "idChangeColorMenuTitle": {"title": "ChangeColorMenuTitle"},
            "idToolbarMenuTitle": {"title": "ToolbarMenuTitle"},
            "idSimpleToolbarTitle": {"title": "SimpleToolbarTitle"},
            "idToolbarWithRightButtonsTitle": {"title": "ToolbarWithRightButtonsTitle"},
            "idToolbarWithLeftAndRightButtonsTitle": {"title": "ToolbarWithLeftAndRightButtonsTitle"},
            "music": {"title": "TabsMISICTitle"},
            "movies": {"title": "TabsMOVIESTitle"},
            "idAccordionMenuTitl": {"title": "AccordionMenuTitle"},
            "backdrop": {"title": "BackdropMenuTitle"},
            "idBannerMenuTitle": {"title": "BannerMenuTitle"},
            "idDate&TimePickersMenuTitle": {"title": "Date&TimePickersMenuTitle"},
            "idCarouselMenuTitle": {"title": "CarouselMenuTitle"},
            "nav_drawer": {"title": "NavigationDrawerMenuTitle"},
            "idSplashMenuTitle": {"title": "SplashMenuTitle"},
            "toolbar": {"title": "BannerTitle"}
            }
    messages = {'English': {
        "MainTitle": "Kitchen Sink",
        "SubTitle": "Demo Kivy MD",
        "ChangeAnimation": "Change Animation",
        "ChangeOrientation": "Change Orientation",
        "ChangeTheme": "Change theme",
        "ChangeLanguage": "Change language Reload",
        "ChangeLanguageNormal": "Change language",
        "DemoSimpleWidgets": "Demo simple widgets",
        "Cards": "Cards",
        "Grid": "Grid",
        "Progress": "Progress",
        "ProgressBars&Slider": "Progress Bars  & Slider",
        "SelectionControls": "Selection Controls",
        "SomeButtons": "Some buttons",
        "SomeLabels": "Some Labels",
        "SomeTextFields": "Some Text Fields",
        "DemoComboWidgets": "Demo combo widgets",
        "BottomSheet": "Bottom sheet",
        "BottomNavigation": "Bottom Navigation",
        "Dialog": "Dialog",
        "List": "List",
        "Menu": "Menu",
        "SnackBar": "Snack Bar",
        "ChangeColors": "Change Colors",
        "Toolbar": "Toolbar",
        "Tabs": "Tabs",
        "ExpansionPanel": "Expansion panel",
        "Backdrop": "Backdrop",
        "Banner": "Banner",
        "DateAndTimePicker": "Date and Time Picker",
        "Carousel": "Carousel",
        "Quit": "Quit",
        "PopupExit": "Press <Esc> or Float button for exit",
        "MainMenuTitle": "Navigation Drawer",
        "ButtonsMenuTitle": "Some buttons. Please click on all of them",
        "BottomSheetMenuTitle": "Bottom sheet",
        "BottomNavigationMenuTitle": "BottomNavigation",
        "CardsMenuTitle": "Cards",
        "DialogsMenuTitle": "Dialogs",
        "GridMenuTitle": "Grid. You can click on any picture",
        "LabelsMenuTitle": "Labels. Scroll down to view all labels",
        "MenuMenuTitle": "Menu",
        "ListMenuTitle": "List. Click any item of the list",
        "ProgressMenuTitle": "Progress",
        "ProgressBarsAndSliderMenuTitle": "Progress Bars And Slider",
        "SelectionControlsMenuTitle": "Selection Controls",
        "SnackBarMenuTitle": "Snack Bar",
        "InputTextMenuTitle": "Input text and press [Enter]",
        "ChangeColorMenuTitle": "Change color",
        "ToolbarMenuTitle": "Toolbar. Click any icons",
        "SimpleToolbarTitle": "Simple toolbar",
        "ToolbarWithRightButtonsTitle": "Toolbar with right buttons",
        "ToolbarWithLeftAndRightButtonsTitle": "Toolbar with left and right buttons",
        "TabsMISICTitle": 'MISIC',
        "TabsMOVIESTitle": 'MOVIES',
        "AccordionMenuTitle": "Accordion. Click on the lines",
        "BackdropMenuTitle": "Example Backdrop",
        "BannerMenuTitle": "Banner. Click on the line bellow",
        "Date&TimePickersMenuTitle": "Date & Time Pickers",
        "CarouselMenuTitle": "Carousel. Slide it, please ",
        "NavigationDrawerMenuTitle": "Navigation Drawer",
        "TabsMenuTitle": "Demo Tabs",
        "SplashMenuTitle": "KivyMD Demo",
        "BannerTitle": "Banner. Click on the line bellow"
    },
        'Русский': {
            "MainTitle": "Кухонная раковина",
            "SubTitle": "Демо Kivy MD",
            "ChangeAnimation": "Изменить анимацию",
            "ChangeOrientation": "Изменить ориентацию",
            "ChangeTheme": "Изменить тему",
            "ChangeLanguage": "Изменить язык Перезапуск",
            "ChangeLanguageNormal": "Изменить язык",
            "DemoSimpleWidgets": "Демо простых виджетов",
            "Cards": "Карточки",
            "Grid": "Таблица",
            "Progress": "Прогресс",
            "ProgressBars&Slider": "Индикаторы и слайдер",
            "SelectionControls": "Селекторы",
            "SomeButtons": "Кнопки",
            "SomeLabels": "Метки",
            "SomeTextFields": "Текстовые поля",
            "DemoComboWidgets": "Демо комбо-виджетов",
            "BottomSheet": "Нижний лист",
            "BottomNavigation": "Нижний навигатор",
            "Dialog": "Диалог",
            "List": "Список",
            "Menu": "Меню",
            "SnackBar": "Снэкбар",
            "ChangeColors": "Изменить цвета",
            "Toolbar": "Инструментальная панель",
            "Tabs": "Закладки",
            "ExpansionPanel": "Раздвижные панели",
            "Backdrop": "Шторка",
            "Banner": "Банер",
            "DateAndTimePicker": "Выбор даты и времени",
            "Carousel": "Карусель",
            "Quit": "Выход",
            "PopupExit": "Для выхода нажми <Esc> или FAB",
            "MainMenuTitle": "Навигатор",
            "ButtonsMenuTitle": "Несколько кнопок. Можете нажать любую",
            "BottomSheetMenuTitle": "Нижний лист",
            "BottomNavigationMenuTitle": "Нижний навигатор",
            "CardsMenuTitle": "Карточки",
            "DialogsMenuTitle": "Диалоги",
            "GridMenuTitle": "Таблица. Можете нажать на любую картинку",
            "LabelsMenuTitle": "Метки. Скролируйте вниз, чтобы увидеть все ",
            "MenuMenuTitle": "Контекстное меню",
            "ListMenuTitle": "Список. Можете нажать на любой элемент",
            "ProgressMenuTitle": "Прогресс",
            "ProgressBarsAndSliderMenuTitle": "Индикаторы и 'движок'",
            "SelectionControlsMenuTitle": "Переключатели",
            "SnackBarMenuTitle": "'Вывеска над баром'",
            "InputTextMenuTitle": "Введите текст и нажмите [Enter]",
            "ChangeColorMenuTitle": "Изменение цветов",
            "ToolbarMenuTitle": "Панель. Нажимайте на любую иконку",
            "SimpleToolbarTitle": "Простая панель",
            "ToolbarWithRightButtonsTitle": "Панель с правыми кнопками",
            "ToolbarWithLeftAndRightButtonsTitle": "Панель с правыми и левыми кнопками",
            "TabsMISICTitle": 'МУЗЫКА',
            "TabsMOVIESTitle": 'ФИЛЬМЫ',
            "AccordionMenuTitle": "Аккордеон. Нажимайте на строки",
            "BackdropMenuTitle": "Пример 'шторки'",
            "BannerMenuTitle": "Банер. Нажмите на нижнюю строку",
            "Date&TimePickersMenuTitle": "Выбор даты и времени",
            "CarouselMenuTitle": "Карусель, сдвигайте фото",
            "NavigationDrawerMenuTitle": "Навигатор",
            "TabsMenuTitle": "Демо Закладок",
            "SplashMenuTitle": "KivyMD Демо",
            "BannerTitle": "Банер. Нажмите на строку ниже "

        }}

    def menu_callback(self, menu_item_text):
        toast("Pressed Menu item: '" + menu_item_text + "' from:" + self.md.caller.name)
        self.md.dismiss()

    def build(self):
        # need for reload and Change Languages
        super()

        # Create menu items
        menu_items = [
            {"text": f"Item {i}",
             "viewclass": "OneLineListItem",
             "on_release": lambda x=f"Item {i}": self.menu_callback(x),
             } for i in range(7)
        ]

        # self.current_language = 'Русский'
        self.current_language = 'English'

        main_widget = Builder.load_string(define_classes + main_widget_kv)

        app = MDApp.get_running_app()
        # need for reload and Change Languages
        app.state = "First"

        # Change application title
        self.changeAppTitle()

        # Change application icon
        app.icon = './assets/KitchenSink.png'

        self.theme_cls.primary_palette = "Indigo"
        self.changeAppColor()

        # Create menu
        self.md = MDDropdownMenu(items=menu_items, width_mult=4, max_height=dp(300))
        self.md.elevation = 4

        self.current_transition = 1

        self.theme_cls.device_orientation = "portrait"

        # For change Orientation by Shift-F11
        # This is standard way with a little bugs
        #         keybinding.start(Window, main_widget)
        # This is my way. It works.
        Window.bind(on_keyboard=windows_on_keyboard_handler)

        return main_widget

    def printIDS(self):
        """ This is a service procedure to print all item identifiers """
        for item in self.root.ids:
            print(item)

    def on_click_button(self, button):
        if (len(button.icon) == 0):
            text = button.text
        else:
            text = button.icon
        toast("You pressed '" + text + "'")

    def changeShadowForChild(self, widget, color):
        if (hasattr(widget, "shadow_color")):
            widget.shadow_color = color
        if hasattr(widget, "children"):
            if (len(widget.children) > 0):
                for child in widget.children:
                    self.changeShadowForChild(child, color)

    def changeShadow(self, color):
        for item in self.root.ids.values():
            if (hasattr(item, "shadow_color")):
                item.shadow_color = color

        self.changeShadowForChild(self.root, color)

    def changeTheme(self):
        if (self.theme_cls.theme_style == 'Dark'):
            self.theme_cls.theme_style = 'Light'
        else:
            self.theme_cls.theme_style = 'Dark'

        self.reloadApp()

        if (self.theme_cls.theme_style == 'Dark'):
            self.changeShadow([1, 1, 1, 0.6])
        else:
            self.changeShadow([0, 0, 0, 0.6])

        self.createExpansionPanels()

    def show_example_bottom_sheet(self):
        bs = MDListBottomSheet()
        bs.add_item("Here's an item with text only", lambda x: self.callback_for_bottom_sheet_items(x))
        bs.add_item("Here's an item with an icon", lambda x: self.callback_for_bottom_sheet_items(x),
                    icon='clipboard-account')
        bs.add_item("Here's another!", lambda x: self.callback_for_bottom_sheet_items(x), icon='nfc')
        bs.open()

    def show_example_grid_bottom_sheet(self):
        bs = MDGridBottomSheet()
        bs.theme_cls.theme_style = 'Light'
        bs.add_item("Facebook", lambda x: self.callback_for_grid_bottom_sheet_items(x),
                    icon_src='./assets/facebook-box.png')
        bs.add_item("YouTube", lambda x: self.callback_for_grid_bottom_sheet_items(x),
                    icon_src='./assets/youtube-play.png')
        bs.add_item("Twitter", lambda x: self.callback_for_grid_bottom_sheet_items(x),
                    icon_src='./assets/twitter.png')
        bs.add_item("Da Cloud", lambda x: self.callback_for_grid_bottom_sheet_items(x),
                    icon_src='./assets/cloud-upload.png')
        bs.add_item("Camera", lambda x: self.callback_for_grid_bottom_sheet_items(x),
                    icon_src='./assets/camera.png')
        bs.open()

    def callback_for_grid_bottom_sheet_items(self, *args):
        toast("You pressed '" + args[0].caption + "'")

    def callback_for_bottom_sheet_items(self, *args):
        toast("You pressed '" + args[0].text + "'")

    def show_example_dialog(self):
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text="This is a dialog with a title and some text. "
                               "That's pretty awesome right!",
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title="This is a test dialog",
                               type="custom",
                               content_cls=content,
                               size_hint=(.8, None),
                               height=dp(200),
                               buttons=[
                                   MDFlatButton(
                                       text="CANCEL", text_color=self.theme_cls.primary_color,
                                       on_release=self.closeDialog
                                   ),
                                   MDFlatButton(
                                       text="OK", text_color=self.theme_cls.primary_color, on_release=self.grabText
                                   ),
                               ]
                               )
        self.dialog.open()

    def show_example_long_dialog(self):
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text="Lorem ipsum dolor sit amet, consectetur \n"
                               + "adipiscing elit, sed do eiusmod tempor \n"
                               + "incididunt ut labore et dolore magna aliqua.\n"
                               + "Ut enim ad minim veniam, quis nostrud \n"
                               + "exercitation ullamco laboris nisi ut aliquip \n"
                               + "ex ea commodo consequat. Duis aute irure \n"
                               + "dolor in reprehenderit in voluptate velit \n"
                               + "esse cillum dolore eu fugiat nulla pariatur. \n"
                               + "Excepteur sint occaecat cupidatat non \n"
                               + "proident, sunt in culpa qui officia deserunt \n"
                                 "mollit anim id est laborum.",
                          size_hint_y=None,
                          valign='top')

        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title="This is a long test dialog",
                               type="custom",
                               content_cls=content,
                               size_hint=(.8, None),
                               height=dp(600),
                               buttons=[
                                   MDFlatButton(
                                       text="CANCEL", text_color=self.theme_cls.primary_color,
                                       on_release=self.closeDialog
                                   ),
                                   MDFlatButton(
                                       text="OK", text_color=self.theme_cls.primary_color, on_release=self.grabText
                                   ), ]
                               )

        self.dialog.open()

    def show_example_input_dialog(self):
        self.dialog = MDDialog(
            title="Address:",
            type="custom",
            content_cls=Content(),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.closeDialog
                ),
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.grabText
                ),
            ],
        )
        self.dialog.open()

    def show_example_snackbar(self, snack_type):
        if snack_type == 'simple':
            Snackbar(text="This is a snackbar!").open()
        elif snack_type == 'verylong':
            Snackbar(text="This is a very very very very very very very long snackbar!").open()

    def grabText(self, inst):
        text = ""
        for obj in self.dialog.content_cls.children:

            if isinstance(obj, MDTextField):
                if (len(obj.text) > 0):
                    text = text + obj.hint_text + ":" + obj.text + "\n"

        if (len(text) > 0):
            toast(text)
        else:
            toast("You pressed 'OK'")
        self.dialog.dismiss()

    def closeDialog(self, inst):
        toast("You pressed 'Cancel'")
        self.dialog.dismiss()

    def pressPicture(self, picture):
        popup = MyPopup()
        popup.ids.popupImage.source = picture.source
        popup.ids.OneLineListItemCaption.text = "[color=#ffffff][b]" + picture.text + "[/b][/color]"
        popup.open()
        toast(picture.text)

    def pressListItem(self, item):
        state = ""
        for child in item.children:
            if hasattr(child, 'children'):
                for ch in child.children:
                    if (hasattr(ch, "state")):
                        state = ch.state
        text = item.text
        if (hasattr(item, "secondary_text")):
            text = text + "\n" + item.secondary_text
        if (len(state) > 0):
            text = text + " state:" + state
        toast("You pressed: " + text)

    def changeAnimation(self):
        transition_name = ''
        if (self.current_transition == 0):
            transition = MDSlideTransition()
            transition_name = 'MDSlideTransition'
            self.current_transition = 1
        elif (self.current_transition == 1):
            transition = MDSwapTransition()
            transition_name = 'MDSwapTransition'
            self.current_transition = 2
        elif (self.current_transition == 2):
            transition = MDFadeSlideTransition()
            transition_name = 'MDFadeSlideTransition'
            self.current_transition = 0
        self.root.ids.manager.transition = transition
        toast("Changed animation to " + transition_name)

    def validateInput(self, input_box):
        if input_box.name == "text_field_error":
            input_box.error = False
            if (len(input_box.text) == 2):
                input_box.error = True
                return
        if input_box.name == "text_field_error_max_text_length10":
            input_box.error = False
            if (len(input_box.text) > 10):
                input_box.error = True
                input_box.text = input_box.text[0:10]

        toast("You input this line :'" + input_box.text + "'\n" \
              + "Object:" + input_box.hint_text)

    def validateInputPasswords(self, input_box):
        regex_A_Z = "[A-Z]"
        regex_a_z = "[a-z]"
        regex_0_9 = "[0-9]"
        regex_special = "[!-/:-@[-`{-~]"
        self.root.ids.text_field_password.error = True
        pattern = re.compile(regex_A_Z)
        if (pattern.search(input_box.text) is None):
            return
        pattern = re.compile(regex_a_z)
        if (pattern.search(input_box.text) is None):
            return
        pattern = re.compile(regex_0_9)
        if (pattern.search(input_box.text) is None):
            return
        pattern = re.compile(regex_special)
        if (pattern.search(input_box.text) is None):
            return
        self.root.ids.text_field_password.error = False
        toast("You input this line :'" + input_box.text + "'\n" \
              + "Object:" + input_box.hint_text)

    def validateInputDate(self, input_box):
        # input_box.error = True
        # date_pattern = '%Y/%m/%d'
        # if (input_box.date_format == "dd/mm/yyyy"):
        #     date_pattern = '%d/%m/%Y'
        # try:
        #     date_object = datetime.strptime(input_box.text, date_pattern)
        # except ValueError as ve:
        #     return
        # if not ("WithoutLimits" in input_box.name):
        #     if not input_box.date_interval[0] is None:
        #         date_low_bound = input_box.date_interval[0]
        #         if date_object.date() < date_low_bound:
        #             return
        #     if not input_box.date_interval[1] is None:
        #         date_high_bound = input_box.date_interval[1]
        #         if date_object.date() > date_high_bound:
        #             return
        # input_box.error = False
        if (not input_box.error):
            toast("You input this line :'" + input_box.text + "'\n" \
                  + "Object:" + input_box.hint_text)

    def twiceTap(self, input_box):
        toast("Pressed twice !!!")

    def tripleTap(self, input_box):
        toast("Pressed three !!!")

    def fourTap(self, input_box):
        toast("Pressed four !!!")

    def menu_open(self, caller):
        # Position may be in the list ["top", "auto", "center", "bottom"]
        # But I don't understand how it works
        self.md.position = "auto"
        if (caller.name == "buttonMenuOpen1"):
            self.md.position = "bottom"
        if (caller.name == "buttonMenuOpen2"):
            self.md.position = "center"
        if (caller.name == "buttonMenuOpen3"):
            self.md.position = "top"

        self.md.caller = caller
        self.md.open()

    def pressCheckbox(self, checkbox):
        toast("Pressed '" + checkbox.name + "'")

    def pressSwitch(self, checkbox):
        toast("Turn '" + checkbox.name + "' state:" + str(checkbox.active))

    def changeColor(self):
        mcp = MDColorPicker()
        mcp.open()
        mcp.bind(
            on_select_color=self.on_select_color,
            on_release=self.change_color, )

    def on_select_color(self, instance_gradient_tab, color: list) -> None:
        ''' Called when a gradient image is clicked. '''
        pass

    def change_color(self,
                     instance_color_picker: MDColorPicker,
                     type_color: str,
                     selected_color: Union[list, str], ):
        instance_color_picker.dismiss()
        if not (selected_color is None):
            self.root.ids.color_button.md_bg_color = selected_color

    def changeAppColor(self):
        length = len(self.color_items)
        current_color = self.theme_cls.primary_palette
        index_color = self.color_items.index(current_color)
        index_color = index_color + 1
        if (index_color >= length):
            index_color = 0
        self.theme_cls.primary_palette = self.color_items[index_color]
        toast("Change Aplication color to " + self.color_items[index_color])

    def pressTool(self, parent, toolbar):
        toast(parent.title + " --> " + toolbar.icon)

    def generateRandomPhoneNumber(self) -> str:
        return "+7(" \
            + str(randrange(10)) + str(randrange(10)) + str(randrange(10)) + ") " \
            + str(randrange(10)) + str(randrange(10)) + str(randrange(10)) + "-" \
            + str(randrange(10)) + str(randrange(10)) + "-" \
            + str(randrange(10)) + str(randrange(10))

    def callback_timer(self, timer):
        self.root.ids.currentdate.text = self.getCurrentDate()
        self.root.ids.currenttime.text = self.getCurrentTime()

    def getCurrentDate(self) -> str:
        return date.today().strftime("%d.%m.%Y")

    def getCurrentTime(self) -> str:
        return datetime.now().strftime('%H:%M:%S')

    def createExpansionPanels(self):
        for i in range(10):
            content = ContentPanel()
            content.id = "expansionpanel" + str(i)
            content.ids.infopanel.text = self.generateRandomPhoneNumber()
            content.bind(on_touch_up=self.on_touch_up)
            md = MDExpansionPanel(
                icon='arrow-expand-down',
                content=content,
                panel_cls=MDExpansionPanelThreeLine(
                    text="Person " + str(i),
                    secondary_text="Country " + str(i),
                    tertiary_text="City " + str(i),
                ),
            )
            md.id = "Person " + str(i)
            md.bind(on_open=self.on_panel_open)
            md.bind(on_close=self.on_panel_close)
            self.root.ids.expansionpanel.add_widget(md)

    def on_start(self):
        super()
        # set timer
        Clock.schedule_interval(self.callback_timer, 0.5)

        # create Accordion (Expension panels)
        self.createExpansionPanels()

        # go to start screen
        self.root.ids.manager.current = "splash"

    # def on_panel_open(self, *args):
    def on_panel_open(self, instance_panel):
        # Alas, changing the icon doesn't work.... why?
        instance_panel.icon = 'arrow-expand-up'
        toast("Open  " + str(instance_panel.content.id))

    def on_panel_close(self, instance_panel):
        # Alas, changing the icon doesn't work.... why?
        instance_panel.icon = 'arrow-expand-down'
        toast("Close " + str(instance_panel.content.id))

    def on_touch_up(self, *args):
        toast("Call to: " + args[0].ids.infopanel.text)

    def openDatePicker(self, button):
        if (button.text == "Open date picker at 2000-01-01"):
            date_dialog = MDDatePicker(year=2000, month=1, day=1)
        elif (button.text == "Open date picker. Date range"):
            toast("You can only select a seven-day period in advance")
            date_dialog = MDDatePicker(min_date=date.today(),
                                       max_date=date.today() + timedelta(days=7))
        elif (button.text == "Open date picker. Select year"):
            current_year = date.today().year
            toast("You can only select a ten-year period in advance")
            date_dialog = MDDatePicker(min_year=date.today().year, max_year=current_year + 10)
        elif (button.text == "Open date picker. Select a date range"):
            date_dialog = MDDatePicker(mode="range")
        else:
            date_dialog = MDDatePicker()

        date_dialog.id = "Button." + button.text
        date_dialog.bind(on_save=self.onSaveDatePicker, on_cancel=self.onCancelDatePicker)
        date_dialog.open()

    def onSaveDatePicker(self, instance, value, date_range):
        text = str(value)
        if (len(date_range) > 0):
            text = "From " + str(date_range[0]) + " to " + str(date_range[len(date_range) - 1])
        toast("Select date is " + text + " \n from " + instance.id)

    def onCancelDatePicker(self, instance, value):
        toast("Cancel date selection")

    def openTimePicker(self, button):
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.onSaveTimeOicker, on_cancel=self.onCancelTimePicker)
        time_dialog.open()

    def onSaveTimeOicker(self, instance, time):
        toast("Selected time is " + str(time))

    def onCancelTimePicker(self, instance, value):
        toast("Cancel time selection")

    def changeOrientation(self):
        size = [0, 0]
        size[0] = Window.size[1]
        size[1] = Window.size[0]
        Window.size = size
        if (self.theme_cls.device_orientation == "portrait"):
            self.theme_cls.device_orientation == "landscape"
        else:
            self.theme_cls.device_orientation == "portrait"

    def shiftCarouselRight(self):
        index = self.root.ids.carousel.index
        if (index < (len(self.root.ids.carousel.slides) - 1)):
            self.root.ids.carousel.index = index + 1

    def shiftCarouselLeft(self):
        index = self.root.ids.carousel.index
        if (index > 0):
            self.root.ids.carousel.index = index - 1

    def changeWidgetStyle(self):
        styles = ["android", "ios", "desktop"]
        style = self.root.ids.grp_chkbox_1.widget_style
        if (style == "ios"):
            style = "desktop"
        elif (style == "desktop"):
            style = "android"
        else:
            style = "ios"
        self.root.ids.grp_chkbox_1.widget_style = style
        self.root.ids.grp_chkbox_2.widget_style = style
        self.root.ids.MDSwitchDemo.widget_style = style
        toast("Changed widget style to " + style)

    def quit(self):
        # self.root_window.close()
        exit(0)

    def changeLanguage(self):
        index_language = self.languages.index(self.current_language)
        index_language = index_language + 1
        if (index_language >= len(self.languages)):
            index_language = 0
        self.current_language = self.languages[index_language]
        self.changeAppTitle()
        self.rebuild()
        if self.languages.index(self.current_language) == 'Русский':
            toast("Изменено на русский язык")
        else:
            toast("Changed to English")

    def build_app(self, first=False):
        """ This method is needed to reload and Change Languages"""
        super()
        if not first:
            self.root.clear_widgets
            return Builder.load_string(main_widget_kv)

    def changeItemLanguage(self, key, id):
        """ Not used"""
        if ('title' in key):
            name_key = key['title']
            id.title = self.messages[self.current_language][name_key]
            print("id.title", id.title)
        if ('text' in key):
            name_key = key['text']
            id.text = self.messages[self.current_language][name_key]
            print("id.text", id.text)

    def lookForChild(self, widget):
        """ Not used"""
        if (hasattr(widget, "name")):
            if (widget.name in self.keys):
                key = self.keys[widget.name]
                self.changeItemLanguage(key, widget)
                print("Change", widget.name)
        if hasattr(widget, "children"):
            if (len(widget.children) > 0):
                for child in widget.children:
                    self.lookForChild(child)

    def changeAppTitle(self):
        app = MDApp.get_running_app()
        if self.current_language == "English":
            app.title = "KitchenSink"
        else:
            app.title = "КухоннаяРаковина"

    def reloadApp(self):
        Window.clear()
        Window.remove_widget(self.root)
        self.root = Builder.load_string(main_widget_kv)
        Window.add_widget(self.root)

    def changeTitleAndText(self):
        index_language = self.languages.index(self.current_language)
        index_language = index_language + 1
        if (index_language >= len(self.languages)):
            index_language = 0
        self.current_language = self.languages[index_language]

        self.reloadApp()
        self.changeAppTitle()

        # create Accordion (Expension panels)
        self.createExpansionPanels()

        # go to start screen
        self.root.ids.manager.current = "splash"

        # for item in self.root.ids:
        #     id = self.root.ids[item]
        #     if (item in self.keys):
        #         key = self.keys[item]
        #         self.changeItemLanguage(key, id)
        #
        # self.lookForChild(app.root)


if __name__ == '__main__':
    DemoKivyMD().run()

