const Gpio = require('onoff').Gpio;
const sleep = require('util').promisify(setTimeout);

// right wheel
const in1A = new Gpio(25, 'out');
const in2A = new Gpio(23, 'out');
const enA = new Gpio(12, 'out');
// left wheel
const in3B = new Gpio(17, 'out');
const in4B = new Gpio(27, 'out');
const enB = new Gpio(13, 'out');
// sensor
const trig_right = new Gpio(5, 'out');
const echo_right = new Gpio(6, 'in');

const distance_measurement = async () => {
  console.log("Distance measurement is in progress...");
  trig_right.writeSync(0);
  console.log("Sensor settles");
  await sleep(2000);
  trig_right.writeSync(1);
  await sleep(0.00001);
  trig_right.writeSync(0);

  let pulse_start;
  let pulse_end;

  while (echo_right.readSync() === 0) {
    pulse_start = process.hrtime();
  }

  while (echo_right.readSync() === 1) {
    pulse_end = process.hrtime();
  }

  const pulse_duration = getDurationInSeconds(pulse_start, pulse_end);
  const distance = pulse_duration * 17150;
  return distance.toFixed(2);
};

const getDurationInSeconds = (start, end) => {
  const [startSeconds, startNanoseconds] = start;
  const [endSeconds, endNanoseconds] = end;
  const seconds = endSeconds - startSeconds;
  const nanoseconds = endNanoseconds - startNanoseconds;
  return seconds + nanoseconds * 1e-9;
};

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

(async () => {
  while (true) {
    try {
      const distance = await distance_measurement();
      console.log(`Distance: ${distance} cm`);

      if (distance > 30) {
        console.log("Moving forward");
        move_forward();
      } else {
        console.log("Stopping");
        stop();
        await sleep(1000);

        console.log("Turning left");
        turn_left();
        await sleep(2000);
      }

      await sleep(100);
    } catch (error) {
      console.error(error);
    }
  }
})();
