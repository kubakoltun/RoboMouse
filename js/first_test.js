const Gpio = require('onoff').Gpio;
const sleep = require('util').promisify(setTimeout);

// right wheel
const in1A = new Gpio(24, 'out');
const in2A = new Gpio(23, 'out');
const enA = new Gpio(25, 'out');
// left wheel
const in3B = new Gpio(17, 'out');
const in4B = new Gpio(27, 'out');
const enB = new Gpio(22, 'out');

const move_forward = () => {
  in1A.writeSync(1);
  in2A.writeSync(0);
  in3B.writeSync(1);
  in4B.writeSync(0);
};

const move_backward = () => {
  in1A.writeSync(0);
  in2A.writeSync(1);
  in3B.writeSync(0);
  in4B.writeSync(1);
};

const turn_left = () => {
  in1A.writeSync(1);
  in2A.writeSync(0);
  in3B.writeSync(0);
  in4B.writeSync(1);
};

const turn_right = () => {
  in1A.writeSync(0);
  in2A.writeSync(1);
  in3B.writeSync(1);
  in4B.writeSync(0);
};

const stop = () => {
  in1A.writeSync(0);
  in2A.writeSync(0);
  in3B.writeSync(0);
  in4B.writeSync(0);
};

console.log("forward");
move_forward();
sleep(2000)
  .then(() => {
    console.log("backwards");
    move_backward();
    return sleep(2000);
  })
  .then(() => sleep(1000))
  .then(() => {
    console.log("left");
    turn_left();
    return sleep(2000);
  })
  .then(() => sleep(1000))
  .then(() => {
    console.log("right");
    turn_right();
    return sleep(2000);
  })
  .then(() => {
    stop();
    in1A.unexport();
    in2A.unexport();
    in3B.unexport();
    in4B.unexport();
    enA.unexport();
    enB.unexport();
  })
  .catch(console.error);
