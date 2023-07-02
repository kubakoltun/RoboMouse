const { Board, Led, Motor } = require('johnny-five');
const board = new Board();

board.on('ready', () => {
  // Define the GPIO pins for the wheels
  const leftWheelPin1 = new Led(13);
  const leftWheelPin2 = new Led(15);
  const rightWheelPin1 = new Led(16);
  const rightWheelPin2 = new Led(18);

  // Function to move forward
  function moveForward() {
    leftWheelPin1.on();
    leftWheelPin2.off();
    rightWheelPin1.on();
    rightWheelPin2.off();
  }

  // Function to move backward
  function moveBackward() {
    leftWheelPin1.off();
    leftWheelPin2.on();
    rightWheelPin1.off();
    rightWheelPin2.on();
  }

  // Function to make a left turn
  function turnLeft() {
    leftWheelPin1.off();
    leftWheelPin2.on();
    rightWheelPin1.on();
    rightWheelPin2.off();
  }

  // Function to make a right turn
  function turnRight() {
    leftWheelPin1.on();
    leftWheelPin2.off();
    rightWheelPin1.off();
    rightWheelPin2.on();
  }

  // Function to stop
  function stop() {
    leftWheelPin1.off();
    leftWheelPin2.off();
    rightWheelPin1.off();
    rightWheelPin2.off();
  }

  moveForward();
  board.wait(2000, () => {
    stop();
    board.wait(1000, () => {
      turnLeft();
      board.wait(1000, () => {
        stop();
        board.wait(1000, () => {
          turnRight();
          board.wait(1000, () => {
            stop();
            board.wait(1000, () => {
              moveBackward();
              board.wait(2000, () => {
                stop();
                board.wait(1000, () => {
                  // Cleanup GPIO pins
                  board.io.reset();
                  process.exit(0);
                });
              });
            });
          });
        });
      });
    });
  });
});
