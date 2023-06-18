const pigpio = require('pigpio-client')().then((pi) => {
  const TRIG = 23;
  const ECHO = 24;

  pi.gpio(TRIG).modeSet('output');
  pi.gpio(ECHO).modeSet('input');

  console.log('Distance measurement is in progress...');

  pi.gpio(TRIG).digitalWrite(0);
  console.log('Sensor settles');
  setTimeout(() => {
    pi.gpio(TRIG).digitalWrite(1);
    setTimeout(() => {
      pi.gpio(TRIG).digitalWrite(0);

      let pulseStart;
      while (pi.gpio(ECHO).digitalRead() === 0) {
        pulseStart = process.hrtime.bigint();
      }

      let pulseEnd;
      while (pi.gpio(ECHO).digitalRead() === 1) {
        pulseEnd = process.hrtime.bigint();
      }

      const pulseDuration = Number(pulseEnd - pulseStart) / 1e6;
      const distance = pulseDuration * 17150;
      console.log(`Distance: ${distance.toFixed(2)} cm`);

      pi.end();
    }, 10);
  }, 2000);
});
