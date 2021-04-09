


class VectorObjectAdder:
    """
    Created by :class:`DebugTab.DebugTab`.

    Deprecated, and should be removed in a future version.
    """
    def __init__(self, window, parent_frame):
        """
        Constructor

        Will call .grid() on parent_frame
        """
        self.window = window
        self.frame = parent_frame
        self.add_button = ttk.Button(self.frame, text='add massless vector object', command=self.add_button_press)
        x_label = ttk.Label(self.frame, text='x')
        y_label = ttk.Label(self.frame, text='y')
        width_label = ttk.Label(self.frame, text='width')
        height_label = ttk.Label(self.frame, text='height')
        color_label = ttk.Label(self.frame, text='color')

        registered_validator_id = self.frame.register(Utility.validate_number_input)

        self.x_variable = StringVar(value='0')
        self.y_variable = StringVar(value='0')
        self.width_variable = StringVar(value='20')
        self.height_variable = StringVar(value='20')
        self.x_entry = ttk.Entry(self.frame, textvariable=self.x_variable, width=5, validate='all', validatecommand=(registered_validator_id, '%S'))
        self.y_entry = ttk.Entry(self.frame, textvariable=self.y_variable, width=5, validate='all', validatecommand=(registered_validator_id, '%S'))
        self.width_entry = ttk.Entry(self.frame, textvariable=self.width_variable, width=5, validate='all', validatecommand=(registered_validator_id, '%S'))
        self.height_entry = ttk.Entry(self.frame, textvariable=self.height_variable, width=5, validate='all', validatecommand=(registered_validator_id, '%S'))

        self.color_button = Button(self.frame, text='blue', command=self.select_color)

        self.add_button.grid(column=0, row=1)
        x_label.grid(column=1, row=0)
        self.x_entry.grid(column=1, row=1)
        y_label.grid(column=2, row=0)
        self.y_entry.grid(column=2, row=1)
        width_label.grid(column=3, row=0)
        self.width_entry.grid(column=3, row=1)
        height_label.grid(column=4, row=0)
        self.height_entry.grid(column=4, row=1)
        color_label.grid(column=5, row=0)
        self.color_button.grid(column=5, row=1)
        self.frame.grid()

    def select_color(self):
        result = colorchooser.askcolor(color=self.color_button['text'])
        self.color_button['text'] = result[1]

    def add_button_press(self):
        # self, x = 0, y = 0, width = 5, height = 5, velocity = 0, acceleration = 0, color = 'blue')
        x = float(self.x_variable.get())
        y = float(self.y_variable.get())
        width = float(self.width_variable.get())
        height = float(self.height_variable.get())
        color = self.color_button['text']

        physics_object = Physics.VectorObject()
        pc = self.window.physics_canvas
        if x > pc.max_x:  # objects placed beyond canvas size get moved to edge
            x = pc.max_x
        elif x < pc.min_x:
            x = pc.min_x
        if y > pc.max_y:
            x = pc.max_y
        elif y < pc.min_y:
            x = pc.min_y
        displacement_vector = Physics.Vector.make_vector_from_components(x, y)
        physics_object.displacement = displacement_vector
        physics_object.acceleration = Physics.Vector.make_directional_vector('S', -9.8)
        physics_object.width = width
        physics_object.height = height
        physics_object.calculate_sides_from_width_height()

        pc.add_physics_object(physics_object)


class MassObjectAdder:
    """
    Created by :class:`DebugTab.DebugTab`.

    Deprecated, and should be removed in a future version.
    """
    def __init__(self, window, parent_frame):
        """
        Will call .grid() on parent frame
        """
        self.window = window
        self.frame = parent_frame
        self.add_button = ttk.Button(self.frame, text='add object with mass', command=self.add_button_press)
        material_label = ttk.Label(self.frame, text='material')
        mass_label = ttk.Label(self.frame, text='mass')

        self.listbox = ttk.Spinbox(self.frame, value=list(Substance.MATERIALS.keys()), state='readonly', width=11 )
        self.listbox.set(list(Substance.MATERIALS.keys())[0])

        registered_validator_id = self.frame.register(Utility.validate_number_input)
        self.mass_variable = StringVar(value=str(Options['default mass']))
        self.mass_entry = ttk.Entry(self.frame, textvariable=self.mass_variable, validate='all', validatecommand=(registered_validator_id, '%S'))

        self.add_button.grid(column=0, row=1)
        material_label.grid(column=1, row=0)
        self.listbox.grid(column=1,row=1)
        mass_label.grid(column=2,row=0)
        self.mass_entry.grid(column=2,row=1)
        self.frame.grid()

    def add_button_press(self):
        material = Substance.MATERIALS[self.listbox.get()]
        mass = float(self.mass_variable.get())
        mass_object = Physics.MassObject(material, mass)
        self.window.physics_canvas.add_physics_object(mass_object)