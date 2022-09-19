from panda3d.core import InputDevice


class ConfigControls:
    TYPE_KEYBOARD = 1
    TYPE_GAMEPAD = 2
    DIRECTION_LEFT = 'left'
    DIRECTION_RIGHT = 'right'
    DIRECTION_UP = 'up'
    DIRECTION_DOWN = 'down'
    BUTTON_CONFIRM = 'confirm'
    BUTTON_CANCEL = 'cancel'

    def __init__(self):
        self.gamepad = None
        self.axis_threshold = 0.5
        self.axis_threshold_negative = 0 - self.axis_threshold
        self.control_type = self.TYPE_KEYBOARD
        self.controlList = [
            # TYPE_KEYBOARD
            ["arrow_left", self.setDirection,  [
                self.DIRECTION_LEFT, True], self.TYPE_KEYBOARD, "Arrow Left"],
            ["arrow_right", self.setDirection, [
                self.DIRECTION_RIGHT, True], self.TYPE_KEYBOARD, "Arrow Right"],
            ["arrow_up", self.setDirection,    [
                self.DIRECTION_UP, True], self.TYPE_KEYBOARD, "Arrow Up"],
            ["arrow_down", self.setDirection,  [
                self.DIRECTION_DOWN, True], self.TYPE_KEYBOARD, "Arrow Down"],
            ["arrow_left-up", self.setDirection,
                [self.DIRECTION_LEFT, False], self.TYPE_KEYBOARD, None],
            ["arrow_right-up", self.setDirection,
                [self.DIRECTION_RIGHT, False], self.TYPE_KEYBOARD, None],
            ["arrow_up-up", self.setDirection,
                [self.DIRECTION_UP, False], self.TYPE_KEYBOARD, None],
            ["arrow_down-up", self.setDirection,
                [self.DIRECTION_DOWN, False], self.TYPE_KEYBOARD, None],
            ["space", self.setCommand,  [self.BUTTON_CONFIRM, True],
                self.TYPE_KEYBOARD, "Spacebar"],
            ["space-up", self.setCommand,  [self.BUTTON_CONFIRM, False],
                self.TYPE_KEYBOARD, None],
            ["enter", self.setCommand,  [self.BUTTON_CONFIRM, True],
                self.TYPE_KEYBOARD, "Enter"],
            ["enter-up", self.setCommand,  [self.BUTTON_CONFIRM, False],
                self.TYPE_KEYBOARD, None],
            ["z", self.setCommand,  [self.BUTTON_CANCEL, True],
                self.TYPE_KEYBOARD, "Z Key"],
            ["z-up", self.setCommand,  [self.BUTTON_CANCEL, False],
                self.TYPE_KEYBOARD, None],
            ["x", self.setCommand,  [self.BUTTON_CONFIRM, True],
                self.TYPE_KEYBOARD, "X Key"],
            ["x-up", self.setCommand,  [self.BUTTON_CONFIRM, False],
                self.TYPE_KEYBOARD, None],
            ["escape", self.setCommand,  [self.BUTTON_CANCEL, True],
                self.TYPE_KEYBOARD, "Escape"],
            ["escape-up", self.setCommand,
                [self.BUTTON_CANCEL, False], self.TYPE_KEYBOARD, None],
            ["backspace", self.setCommand,  [self.BUTTON_CANCEL, True],
                self.TYPE_KEYBOARD, "Backspace"],
            ["backspace-up", self.setCommand,
                [self.BUTTON_CANCEL, False], self.TYPE_KEYBOARD, None],
            # TYPE_GAMEPAD
            ["gamepad-dpad_right", self.setDirection,
                [self.DIRECTION_RIGHT, True], self.TYPE_GAMEPAD, "D-pad Right"],
            ["gamepad-dpad_right-up", self.setDirection,
                [self.DIRECTION_RIGHT, False], self.TYPE_GAMEPAD, None],
            ["gamepad-dpad_left", self.setDirection,
                [self.DIRECTION_LEFT, True], self.TYPE_GAMEPAD, "D-pad Left"],
            ["gamepad-dpad_left-up", self.setDirection,
                [self.DIRECTION_LEFT, False], self.TYPE_GAMEPAD, None],
            ["gamepad-dpad_up", self.setDirection,
                [self.DIRECTION_UP, True], self.TYPE_GAMEPAD, "D-pad Up"],
            ["gamepad-dpad_up-up", self.setDirection,
                [self.DIRECTION_UP, False], self.TYPE_GAMEPAD, None],
            ["gamepad-dpad_down", self.setDirection,
                [self.DIRECTION_DOWN, True], self.TYPE_GAMEPAD, "D-pad Down"],
            ["gamepad-dpad_down-up", self.setDirection,
                [self.DIRECTION_DOWN, False], self.TYPE_GAMEPAD, None],
            ["gamepad-face_a", self.setCommand,
                [self.BUTTON_CONFIRM, True], self.TYPE_GAMEPAD, "A Button"],
            ["gamepad-face_a-up", self.setCommand,
                [self.BUTTON_CONFIRM, False], self.TYPE_GAMEPAD, None],
            ["gamepad-back", self.setCommand,
                [self.BUTTON_CANCEL, True], self.TYPE_GAMEPAD, "Back Button"],
            ["gamepad-back-up", self.setCommand,
                [self.BUTTON_CANCEL, False], self.TYPE_GAMEPAD, None],
            ["gamepad-start", self.setCommand,
                [self.BUTTON_CONFIRM, True], self.TYPE_GAMEPAD, "Start Button"],
            ["gamepad-start-up", self.setCommand,
                [self.BUTTON_CONFIRM, False], self.TYPE_GAMEPAD, None],
        ]
        self.initController()
        self.resetButtons()

    def initController(self):
        self.disableController()

        for control in self.controlList:
            base.accept(control[0], control[1], control[2])

        # Accept device dis-/connection events
        base.accept("connect-device", self.connect)
        base.accept("disconnect-device", self.disconnect)

    def connect(self, device):
        # gamepads = base.devices.getDevices(InputDevice.DeviceClass.gamepad)
        if device.device_class == InputDevice.DeviceClass.gamepad and not self.gamepad:
            self.gamepad = device
            base.attachInputDevice(device, prefix="gamepad")
            self.control_type = self.TYPE_GAMEPAD

    def disconnect(self, device):
        if self.gamepad != device:
            return
        base.detachInputDevice(device)
        self.gamepad = None
        self.control_type = self.TYPE_KEYBOARD

    def resetButtons(self):
        self.resetDirections()
        self.commandMap = {
            self.BUTTON_CONFIRM: False,
            self.BUTTON_CANCEL: False
        }

    def resetDirections(self):
        self.directionMap = {
            self.DIRECTION_LEFT: False,
            self.DIRECTION_RIGHT: False,
            self.DIRECTION_DOWN: False,
            self.DIRECTION_UP: False
        }

    def setDirection(self, key, value):
        self.directionMap[key] = value

    def setCommand(self, key, value):
        self.commandMap[key] = value

    def disableController(self):
        self.resetButtons()

        base.ignore("connect-device")
        base.ignore("disconnect-device")

        for control in self.controlList:
            base.ignore(control[0])

    def read_axis_left(self):
        if not self.gamepad:
            return {'x': 0, 'y': 0}

        left_x = self.gamepad.findAxis(InputDevice.Axis.left_x)
        left_y = self.gamepad.findAxis(InputDevice.Axis.left_y)
        return {'x': left_x.value, 'y': left_y.value}

    def read_axis_right(self):
        if not self.gamepad:
            return {'x': 0, 'y': 0}
        right_x = self.gamepad.findAxis(InputDevice.Axis.right_x)
        right_y = self.gamepad.findAxis(InputDevice.Axis.right_y)
        return {'x': right_x.value, 'y': right_y.value}

    def getKeysPressedTotal(self):
        keysPressed = sum(base.directionMap.values())
        # if base.control_type == base.TYPE_GAMEPAD and 0 == keysPressed:
        #     base.move_from_axis(True)
        #     keysPressed = sum(base.directionMap.values())

        # if 0 == keysPressed:
        #     self.resetDirections()

        return keysPressed

    def move_from_axis(self, is_left_axis):
        axis_obj = self.read_axis_left() if is_left_axis else self.read_axis_right()
        if axis_obj['x'] <= self.axis_threshold_negative:
            self.setDirection(self.DIRECTION_LEFT, True)
        else:
            self.setDirection(self.DIRECTION_LEFT, False)
        if axis_obj['x'] >= self.axis_threshold:
            self.setDirection(self.DIRECTION_RIGHT, True)
        else:
            self.setDirection(self.DIRECTION_RIGHT, False)

        if axis_obj['y'] <= self.axis_threshold_negative:
            self.setDirection(self.DIRECTION_DOWN, True)
        else:
            self.setDirection(self.DIRECTION_DOWN, False)
        if axis_obj['y'] >= self.axis_threshold:
            self.setDirection(self.DIRECTION_UP, True)
        else:
            self.setDirection(self.DIRECTION_UP, False)
