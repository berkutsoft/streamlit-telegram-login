// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

function sendValue(value) {
    Streamlit.setComponentValue(value);
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event) {
    // Only run the render code the first time the component is loaded.
    if (!window.rendered) {
        const {args} = event.detail;
        const script = document.createElement('script');

        script.src = "https://telegram.org/js/telegram-widget.js?22";
        script.async = true;
        script.setAttribute("data-telegram-login", args.bot_username);
        script.setAttribute("data-size", args.button_style);
        script.setAttribute("data-onauth", "onTelegramAuth(user)");
        script.setAttribute("data-userpic", args.userpic);
        if (args.request_access) {
            script.setAttribute("data-request-access", "write");
        }
        if (args.corner_radius !== null) {
            script.setAttribute("data-radius", args.corner_radius);
        }

        document.body.appendChild(script);

        window.onTelegramAuth = (user) => {
            alert('Logged in as ' + user.first_name + ' ' + user.last_name + ' (' + user.id + (user.username ? ', @' + user.username : '') + ')');
            sendValue(user);
        };
        // You most likely want to get the data passed in like this
        // const {input1, input2, input3} = event.detail.args

        // You'll most likely want to pass some data back to Python like this
        // sendValue({output1: "foo", output2: "bar"})
        window.rendered = true;
    }
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady();
// Render with the correct height, if this is a fixed-height component
Streamlit.setFrameHeight(100);
