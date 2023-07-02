const Gpio = require('onoff').Gpio;

const pinNumber = 17;
const gpioPin = new Gpio(pinNumber, 'in');

gpioPin.unexport();
