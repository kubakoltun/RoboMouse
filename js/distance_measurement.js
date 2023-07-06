const pigpio = require('pigpio-client')().then((pi) => {
  const trigRight = 5
  const echoRight = 6

  pi.gpio(trigRight).modeSet('output');
  pi.gpio(echoRight).modeSet('input');

  console.log('Distance measurement is in progress...');

  pi.gpio(trigRight).digitalWrite(0);
  console.log('Sensor settles');
  setTimeout(() => {
    pi.gpio(trigRight).digitalWrite(1);
    setTimeout(() => {
      pi.gpio(trigRight).digitalWrite(0);

      let pulseStart;
      while (pi.gpio(echoRight).digitalRead() === 0) {
        pulseStart = process.hrtime.bigint();
      }

      let pulseEnd;
      while (pi.gpio(echoRight).digitalRead() === 1) {
        pulseEnd = process.hrtime.bigint();
      }

      const pulseDuration = Number(pulseEnd - pulseStart) / 1e6;
      const distance = pulseDuration * 17150;
      console.log(`Distance: ${distance.toFixed(2)} cm`);

      pi.end();
    }, 10);
  }, 2000);
});
