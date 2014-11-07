# Model

from gi.repository import Clutter, Mx, Mash, Toggle

class Model(Toggle.Model):
    def __init__(self, ui, filename):   
        super(Model, self).__init__()    
        model = ui.get_object("model")
        self.filename = filename
        model.load_from_file(0, "/usr/share/models/ply/"+filename+".ply")
        model.set_color(Clutter.Color.from_string("#55A94BFF")[1])

        #Set up the light
        self.light_set = Mash.LightSet()
        light_point = Mash.PointLight()
        light_directional = Mash.DirectionalLight()
        light_spot = Mash.SpotLight()
    
        self.light_set.add_light(light_point)
        self.light_set.add_light(light_directional)
        self.light_set.add_light(light_spot)

        # Add the model the lights to the volume viewport
        ui.get_object("volume-viewport").add_child(light_point);
        ui.get_object("volume-viewport").add_child(light_directional);
        ui.get_object("volume-viewport").add_child(light_spot);

        model.set_light_set(self.light_set)
        model.set_reactive(True)
        model.connect("button-press-event", self.click)
        stage = ui.get_object("stage")
        stage.connect("motion-event", self.move)
        stage.connect("button-release-event", self.release)
        self.clicked = False
        self.last_x = 0
        self.last_y = 0

    def click(self, actor, event):
        self.last_x = event.x
        self.last_y = event.y
        self.clicked = True

    def release(self, actor, event):
        self.clicked = False

    def move(self, actor, event):
        delta_x = event.x-self.last_x
        delta_y = self.last_y-event.y
        self.last_x = event.x
        #self.last_y = event.y
        if self.clicked:
            self.move_by(delta_x, 0)
            self.set_z_position(100+delta_y)

