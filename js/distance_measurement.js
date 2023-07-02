const pigpio = require('pigpio-client')().then((pi) => {
  const TRIGEVEN = 29;
  const ECHOEVEN = 31;
  const TRIGODD = 33;
  const ECHOODD = 35;

  pi.gpio(TRIGEVEN).modeSet('output');
  pi.gpio(ECHOEVEN).modeSet('input');

  console.log('Distance measurement is in progress...');

  pi.gpio(TRIGEVEN).digitalWrite(0);
  console.log('Sensor settles');
  setTimeout(() => {
    pi.gpio(TRIGEVEN).digitalWrite(1);
    setTimeout(() => {
      pi.gpio(TRIGEVEN).digitalWrite(0);

      let pulseStart;
      while (pi.gpio(ECHOEVEN).digitalRead() === 0) {
        pulseStart = process.hrtime.bigint();
      }

      let pulseEnd;
      while (pi.gpio(ECHOEVEN).digitalRead() === 1) {
        pulseEnd = process.hrtime.bigint();
      }

      const pulseDuration = Number(pulseEnd - pulseStart) / 1e6;
      const distance = pulseDuration * 17150;
      console.log(`Distance: ${distance.toFixed(2)} cm`);

      pi.end();
    }, 10);
  }, 2000);
});
