from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
from homeassistant.components import rpi_gpio
import time
from datetime import datetime
import logging

DEFAULT_I2C_ADDRESS = 0x29
DEFAULT_I2C_BUS = 1
DEFAULT_RANGE = 2
DEFAULT_XSHUT = 16

REQUIREMENTS = ['smbus2==0.2.2', 'VL53L1X2==0.1.4']

DEPENDENCIES = ['rpi_gpio']

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the VL53L1X ToF Sensor from ST."""
    import smbus # pylint: disable=import-error
    from VL53L1X2 import VL53L1X # pylint: disable=import-error

    rpi_gpio.setup_output(DEFAULT_XSHUT)
    
    rpi_gpio.write_output(DEFAULT_XSHUT, 0)
    time.sleep(0.01)
    rpi_gpio.write_output(DEFAULT_XSHUT, 1)
    time.sleep(0.01)

    sensor_id = 1111

    tof = VL53L1X()
    tof.open() # Initialise the i2c bus and configure the sensor
    tof.add_sensor(sensor_id, DEFAULT_I2C_ADDRESS) # add a VL53L1X device
    tof.start_ranging(sensor_id, 2) # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range

    for _ in range(0,3):
        distance_mm = tof.get_distance(sensor_id)  # Grab the range in mm
        _LOGGER.warning("Time: {}\tVL53L1X: {} mm".format(datetime.utcnow().strftime("%S.%f"), distance_mm))
        time.sleep(0.01)

    tof.stop_ranging(sensor_id) 
    add_devices([TofSensor()])


class TofSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""

        self._state = None        

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'VL53L1X'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = 23
        