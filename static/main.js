console.log('JS Is Running');

// Note: ES6 is preferred when applicable. Its just clean and I don't get to use it at work ;).
// Make sure to use let and const over var, that's the main thing.
// https://codeburst.io/es6-tutorial-for-beginners-5f3c4e7960be
// Also note that hard refresh is necessary when modifying js.

/*
TODO: function possibleMoves
    Triggered by clicking on a map hex.
    -> Asks server what moves are possible in a specific location.
    Sets up a callback for the response.
 */
function requestPossibleMoves(x, y) {}

/*
TODO: function initializeMovesMenu
    Callback after response from possibleMoves API.
    Location does not need to be returned by the API. We know it when the callback is initialized.
    -> Display menu for selecting moves.
    -> Store relevant info for tracking moves locally.
 */
function initializeMovesMenu(response, x, y) {}

/*
TODO: function build
    Triggered by completing necessary moves menu items.
    Actually build the mine
    -> Add temporary building to map and to state object.
    -> Modify temp state to indicate change in player resources.
    -> (Eventually) Trigger power leeching.
 */

 function build(x, y) {}

// Setting up click events.

$('.hex').click(function() {
    console.log(this);
    alert("You clicked a hex!");
});

$('.planet').click(function() {
    console.log(this);
    alert("You clicked a planet!");
});