from streamlit_javascript import st_javascript

def play_both():
    # st_javascript("console.log('You pressed the button');")
    st_javascript("""new Promise((resolve, reject) => {
 console.log('You pressed the play button');

  const parentDocument = window.parent.document;

  // Define playButtons at the beginning
  const playButtons = parentDocument.querySelectorAll('g.updatemenu-button text');

  let buttonFound = false;

  // Create an array to hold the click events to dispatch later
  let clickEvents = [];

  // Loop through all found play buttons
  playButtons.forEach(button => {
    if (button.textContent.trim() === '▶') {
      console.log("Queueing click on button");
      const clickEvent = new MouseEvent('click', {
        view: window,
        bubbles: true,
        cancelable: true
      });

      // Store the click event in the array
      clickEvents.push(button.parentElement);
      buttonFound = true;
    }
  });

  // If at least one button is found, dispatch all events
  if (buttonFound) {
    console.log('Dispatching click events');
    clickEvents.forEach(element => {
      element.dispatchEvent(new MouseEvent('click', {
        view: window,
        bubbles: true,
        cancelable: true
      }));
    });

    resolve('All buttons clicked successfully');
  } else {
    reject('No play buttons found');
  }
})
.then((message) => {
  console.log(message);
  return 'Play clicks completed';
})
.catch((error) => {
  console.log(error);
  return 'Operation failed';
})
.then((finalMessage) => {
  console.log(finalMessage);
});

""")


def pause_both():
    # st_javascript("console.log('You pressed the button');")
    st_javascript("""new Promise((resolve, reject) => {
  console.log('You pressed the pause button');

  const parentDocument = window.parent.document;

  // Define playButtons at the beginning
  const playButtons = parentDocument.querySelectorAll('g.updatemenu-button text');

  let buttonFound = false;

  // Create an array to hold the click events to dispatch later
  let clickEvents = [];

  // Loop through all found play buttons
  playButtons.forEach(button => {
    if (button.textContent.trim() === '▶') {
      console.log("Queueing click on button");
      const clickEvent = new MouseEvent('click', {
        view: window,
        bubbles: true,
        cancelable: true
      });

      // Store the click event in the array
      clickEvents.push(button.parentElement);
      buttonFound = true;
    }
  });

  // If at least one button is found, dispatch all events
  if (buttonFound) {
    console.log('Dispatching click events');
    clickEvents.forEach(element => {
      element.dispatchEvent(new MouseEvent('click', {
        view: window,
        bubbles: true,
        cancelable: true
      }));
    });

    resolve('All buttons clicked successfully');
  } else {
    reject('No pause buttons found');
  }
})
.then((message) => {
  console.log(message);
  return 'Pause clicks completed';
})
.catch((error) => {
  console.log(error);
  return 'Operation failed';
})
.then((finalMessage) => {
  console.log(finalMessage);
});


""")

def troubleshoot_js():
    # st_javascript("console.log('You pressed the button');")
    st_javascript("""new Promise((resolve, reject) => {
  console.log('You pressed the button');

  const parentDocument = window.parent.document;

  // Select all <div> elements on the page
  const divs = parentDocument.querySelectorAll('div');

  // Log the total number of <div> elements
  console.log('Total number of divs on the page:', divs.length);

  console.log(document.body.innerHTML);

  // Define playButtons at the beginning
  const playButtons = parentDocument.querySelectorAll('g.updatemenu-button text');

  // Log the number of buttons found for debugging
  console.log('Number of buttons found:', playButtons.length);

  let buttonFound = false;

  // Create an array to hold the click events to dispatch later
  let clickEvents = [];

  // Loop through all found play buttons
  playButtons.forEach(button => {
    if (button.textContent.trim() === '▶') {
      console.log("Queueing click on button");
      const clickEvent = new MouseEvent('click', {
        view: window,
        bubbles: true,
        cancelable: true
      });

      // Store the click event in the array
      clickEvents.push(button.parentElement);
      buttonFound = true;
    }
  });

  // If at least one button is found, dispatch all events
  if (buttonFound) {
    console.log('Dispatching click events');
    clickEvents.forEach(element => {
      element.dispatchEvent(new MouseEvent('click', {
        view: window,
        bubbles: true,
        cancelable: true
      }));
    });

    resolve('All buttons clicked successfully');
  } else {
    reject('No button found');
  }
})
.then((message) => {
  console.log(message);
  return 'Operation completed';
})
.catch((error) => {
  console.log(error);
  return 'Operation failed';
})
.then((finalMessage) => {
  console.log(finalMessage);
});

""")
