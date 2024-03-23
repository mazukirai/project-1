from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from plyer import gps, call
from geopy.geocoders import Nominatim

class ScreenOne(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        buttons = ["Fire", "Earthquake", "Flood", "Medical Assistance", "Accidents", "Map"]
        
        for text in buttons:
            button = Button(text=text, size_hint=(1, None), height=50)
            if text == "Map":
                button.bind(on_press=self.switch_screen)
            else:
                button.bind(on_press=self.make_call)
            layout.add_widget(button)
        
        self.add_widget(layout)
    
    def switch_screen(self, instance):
        self.manager.current = 'screen_two'
    
    def make_call(self, instance):
        incident_type = instance.text.lower()
        emergency_numbers = {
            "fire": "09451493797",  
            "earthquake": "09451493797",
            "flood": "09451493797",
            "medical assistance": "09451493797",
            "accidents": "09451493797"
        }
        if incident_type in emergency_numbers:
            try:
                call.makecall(emergency_numbers[incident_type])
            except NotImplementedError:
                print("Executed but device is not compatible")
                raise

class ScreenTwo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        
        return_button = Button(text="Return to Screen One", size_hint=(None, None), size=(200, 50))
        return_button.bind(on_press=self.switch_screen)
        
        location_button = Button(text="Get Current Location", size_hint=(None, None), size=(200, 50))
        location_button.bind(on_press=self.get_location)
        
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        button_layout.add_widget(return_button)
        button_layout.add_widget(location_button)
        
        layout.add_widget(button_layout)
        self.add_widget(layout)
    
    def switch_screen(self, instance):
        self.manager.current = 'screen_one'

    def get_location(self, instance):
        gps.configure(on_location=self.on_location)
        gps.start()

    def on_location(self, **kwargs):
        latitude = kwargs['lat']
        longitude = kwargs['lon']
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        print("Current Location:", location.address)

class MyApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(ScreenOne(name='screen_one'))
        screen_manager.add_widget(ScreenTwo(name='screen_two'))
        return screen_manager

if __name__ == '__main__':
    MyApp().run()
